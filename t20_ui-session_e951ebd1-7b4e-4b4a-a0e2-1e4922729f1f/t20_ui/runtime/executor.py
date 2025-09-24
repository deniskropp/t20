# Module to interact with the T20 runtime package

import subprocess
import threading
import json
import os
from PyQt6.QtCore import QObject, pyqtSignal, QProcess, QIODevice, QStandardPaths

class RuntimeExecutor(QObject):
    # Signals to communicate with the UI thread
    log_message = pyqtSignal(str)
    progress_update = pyqtSignal(int, int) # current_step, total_steps
    task_output = pyqtSignal(str)
    artifacts_found = pyqtSignal(list, str) # list of artifact dicts, session_path
    task_finished = pyqtSignal()
    error_occurred = pyqtSignal(str) # Signal for critical errors

    def __init__(self, parent=None):
        super().__init__(parent)
        self.process = None
        self.session_path = None
        self.output_buffer = ""
        self.error_buffer = ""

    def run_task(self, task_goal, config):
        if self.process and self.process.state() == QProcess.ProcessState.Running:
            self.error_occurred.emit("A task is already running.")
            return

        # Construct the command
        command = ["t20-system", task_goal]
        command.append("-o")
        command.append(config.get("orchestrator", "LaCogito"))
        command.append("-m")
        command.append(config.get("model", "gemini-1.5-flash-latest"))
        command.append("-r")
        command.append(str(config.get("rounds", 5)))
        
        files = config.get("files", [])
        if files:
            command.append("-f")
            command.extend(files)

        self.log_message.emit(f"Executing command: {' '.join(command)}")

        self.process = QProcess(self)
        # Connect signals for process output and state changes
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.handle_finished)
        self.process.errorOccurred.connect(self.handle_error)

        # Start the process
        self.process.start(command[0], command[1:])

    def handle_stdout(self):
        if self.process is None: return
        
        # Read all available data and append to buffer
        # Use readAllStandardOutput() and decode to string
        stdout_data = self.process.readAllStandardOutput().data().decode('utf-8', errors='replace')
        self.output_buffer += stdout_data

        # Process lines from the buffer
        while '\n' in self.output_buffer:
            line, self.output_buffer = self.output_buffer.split('\n', 1)
            self.process_log_line(line.strip())
        
        # Emit the remaining buffer if it looks like a final output (heuristic)
        # This part is tricky and depends heavily on t20-system's output format.
        # For now, we'll primarily rely on structured JSON for artifacts and final output.

    def handle_stderr(self):
        if self.process is None: return

        stderr_data = self.process.readAllStandardError().data().decode('utf-8', errors='replace')
        self.error_buffer += stderr_data

        while '\n' in self.error_buffer:
            line, self.error_buffer = self.error_buffer.split('\n', 1)
            self.log_message.emit(f"[STDERR] {line.strip()}")

    def process_log_line(self, line):
        if not line: return

        try:
            # Attempt to parse as JSON, expecting structured output for artifacts
            data = json.loads(line)
            if isinstance(data, dict) and "artifacts" in data and "session_path" in data:
                artifacts = data.get("artifacts", [])
                session_path = data.get("session_path", "")
                self.session_path = session_path
                self.artifacts_found.emit(artifacts, session_path)
                self.log_message.emit(f"[INFO] Artifacts detected in session: {session_path}")
            elif isinstance(data, dict) and "final_output" in data:
                 # If the JSON contains a specific key for final output
                 final_output = data["final_output"]
                 self.task_output.emit(final_output)
                 self.log_message.emit("[INFO] Final output received.")
            else:
                # If it's JSON but not recognized structured data, log it as is
                self.log_message.emit(f"[JSON] {line}")
        except json.JSONDecodeError:
            # If not JSON, treat as a regular log message or potentially final output
            self.log_message.emit(line)
            # Heuristic: If it's the last line and the process is about to finish, assume it's final output
            # This requires careful handling and might need a specific signal from t20-system
            # For now, we'll emit it as task_output, which might overwrite previous outputs
            self.task_output.emit(line)
        except Exception as e:
            self.log_message.emit(f"[UI ERROR] Unexpected error processing line: {e} - Line: {line}")

    def handle_finished(self, exit_code, exit_status):
        # Process any remaining data in buffers
        if self.output_buffer:
            self.process_log_line(self.output_buffer)
            self.output_buffer = ""
        if self.error_buffer:
            self.log_message.emit(f"[STDERR] {self.error_buffer.strip()}")
            self.error_buffer = ""

        self.log_message.emit(f"Task process finished. Exit code: {exit_code}, Status: {exit_status}")
        if exit_code != 0:
            self.error_occurred.emit(f"Task failed with exit code {exit_code}.")
        
        self.task_finished.emit()
        self.process = None # Reset for next task

    def handle_error(self, error):
        error_string = "Unknown error"
        if error == QProcess.ProcessError.FailedToStart:
            error_string = "Failed to start process. Is 't20-system' in your PATH?"
        elif error == QProcess.ProcessError.Timedout:
            error_string = "Process timed out."
        elif error == QProcess.ProcessError.WriteError:
            error_string = "Error writing to process."
        elif error == QProcess.ProcessError.ReadError:
            error_string = "Error reading from process."
        
        self.log_message.emit(f"[PROCESS ERROR] {error_string} (Code: {error})")
        self.error_occurred.emit(error_string)
        self.task_finished.emit() # Ensure UI is updated even on error
        self.process = None

    def stop_task(self):
        if self.process and self.process.state() == QProcess.ProcessState.Running:
            self.log_message.emit("Attempting to stop the running task...")
            self.process.terminate() # Sends SIGTERM
            if not self.process.waitForFinished(3000): # Wait up to 3 seconds
                self.log_message.emit("Task did not terminate gracefully, killing...")
                self.process.kill() # Sends SIGKILL
                self.process.waitForFinished(1000)
            self.log_message.emit("Task stopped.")
            self.process = None
        else:
            self.log_message.emit("No task is currently running.")

    def get_session_path(self):
        return self.session_path

