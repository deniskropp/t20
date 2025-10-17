import logging
import os
from PySide6.QtCore import QObject, Signal, Slot

from runtime import System
from runtime.custom_types import Plan, File
from logging_handler import QtLogHandler

class Worker(QObject):
    """Handles long-running T20 runtime tasks in a separate thread."""
    plan_generated = Signal(Plan)
    log_message = Signal(str)
    task_status_updated = Signal(str, str) # task_id, status ('running', 'success', 'error')
    workflow_finished = Signal(str) # session_directory_path
    error_occurred = Signal(str)

    @Slot(str, str, list)
    def run_workflow(self, goal: str, orchestrator_name: str, file_paths: list):
        """The main entry point for running a T20 workflow."""
        try:
            # 1. Instantiate `runtime.System`
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            system = System(root_dir=project_root, default_model='mistral:mistral-small-latest')

            # 2. Call `system.setup()`
            system.setup(orchestrator_name=orchestrator_name)

            # 3. Set up the custom logging handler
            log_handler = QtLogHandler()
            log_handler.new_log_message.connect(self.log_message)
            logging.getLogger().addHandler(log_handler)
            # Set level to INFO to capture runtime messages
            logging.getLogger().setLevel(logging.INFO)

            # Convert file paths to File objects
            file_objects = []
            for path in file_paths:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    file_objects.append(File(path=path, content=content))
                except Exception as e:
                    self.log_message.emit(f"[WORKER-ERROR] Failed to read file {path}: {e}")

            # 4. Call `system.start()` to get the plan.
            self.log_message.emit("[WORKER] Generating execution plan...")
            plan = system.start(high_level_goal=goal, files=file_objects)
            if not plan:
                 raise RuntimeError("Failed to generate a valid plan.")

            # 5. Emit `plan_generated` signal.
            self.plan_generated.emit(plan)
            self.log_message.emit("[WORKER] Plan generated. Starting workflow execution...")

            # 6. Call `system.run()`. This is the blocking call.
            system.run(plan=plan, rounds=1, files=file_objects)

            # 7. After it completes, emit `workflow_finished`.
            self.log_message.emit("[WORKER] Workflow execution finished.")
            self.workflow_finished.emit(system.session.session_dir)

        except Exception as e:
            # 8. Use a try...except block to catch all exceptions.
            logging.exception("Error in worker thread")
            self.error_occurred.emit(str(e))
        finally:
            # Clean up the handler to prevent duplicate messages on next run
            if 'log_handler' in locals():
                logging.getLogger().removeHandler(log_handler)
