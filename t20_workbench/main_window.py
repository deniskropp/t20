import sys
import os
import re
import logging
from PySide6.QtCore import (
    Qt,
    QThread,
    Signal,
    Slot,
    QStringListModel,
    QModelIndex,
    QPoint,
    QItemSelection,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QListView,
    QTreeView,
    QSplitter,
    QSplitter,
    QTabWidget,
    QPlainTextEdit,
    QFileSystemModel,
    QMessageBox,
    QLabel,
    QHeaderView,
    QComboBox,
    QLineEdit,
    QMenu,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont, QAction
import yaml

from worker import Worker
from runtime.custom_types import Plan, Task
from runtime.llm import _provider_registry
from agent_config_dialog import AgentConfigDialog
from views.left_panel_view import LeftPanelView
from views.center_panel_view import CenterPanelView
from views.bottom_panel_view import BottomPanelView

# --- Constants for Plan View ---
STATUS_COLUMN = 0
TASK_COLUMN = 1
AGENT_COLUMN = 2

STATUS_PENDING = "⚪"
STATUS_RUNNING = "🟡"
STATUS_SUCCESS = "🟢"
STATUS_ERROR = "🔴"

class MainWindow(QMainWindow):
    """Main application window for the T20 Workbench."""

    # Signal to start the workflow in the worker thread
    start_workflow_signal = Signal(str, str, list, str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("T20 Workbench")
        self.setGeometry(100, 100, 1400, 900)

        self.file_list_model = QStringListModel()
        self.plan_model = QStandardItemModel()
        self.fs_model = QFileSystemModel()

        self._setup_ui()
        self._populate_orchestrators()
        self._setup_worker_thread()
        self._setup_connections()

        self._reset_ui_state()

    def _setup_ui(self):
        """Initializes and arranges all UI widgets."""
        self.left_panel = LeftPanelView(self.file_list_model)
        self.center_panel = CenterPanelView(self.plan_model)
        self.bottom_panel = BottomPanelView(self.fs_model)

        self.left_panel.llm_provider_combo.addItems(sorted(_provider_registry.keys()))

        # --- Splitter Layout ---
        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        top_splitter.addWidget(self.left_panel)
        top_splitter.addWidget(self.center_panel)
        top_splitter.setStretchFactor(0, 1)
        top_splitter.setStretchFactor(1, 3)

        main_splitter = QSplitter(Qt.Orientation.Vertical)
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(self.bottom_panel)
        main_splitter.setStretchFactor(0, 2)
        main_splitter.setStretchFactor(1, 1)

        self.setCentralWidget(main_splitter)

    def _populate_orchestrators(self):
        """Scans the agents directory and populates the orchestrator combo box."""
        from config_manager import ConfigManager

        config = ConfigManager()
        agents_dir_path = config.get('paths.agents_dir', '../agents')
        try:
            agents_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), agents_dir_path))
            if not os.path.isdir(agents_dir):
                print("[UI-ERROR] Agents directory not found.")
                return

            orchestrators = []
            for filename in os.listdir(agents_dir):
                if filename.endswith('.yaml'):
                    file_path = os.path.join(agents_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # A simple, safe way to get the name without parsing full YAML
                        doc = yaml.safe_load(f)
                        if doc and doc.get('role') == 'Orchestrator':
                            orchestrators.append(doc.get('name', filename.replace('.yaml', '')))
            self.left_panel.orchestrator_combo.addItems(sorted(orchestrators))
        except FileNotFoundError:
            print(f"[UI-ERROR] Agents directory not found at expected path.")
        except yaml.YAMLError as e:
            print(f"[UI-ERROR] Error parsing YAML in agents directory: {e}")
        except Exception as e:
            print(f"[UI-ERROR] An unexpected error occurred while loading orchestrators: {e}")

    def _setup_worker_thread(self):
        """Creates and configures the worker thread for background processing."""
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        # Worker thread communication
        self.start_workflow_signal.connect(self.worker.run_workflow)
        self.worker.plan_generated.connect(self._update_plan_view)
        self.worker.log_message.connect(self._append_log_message)
        self.worker.task_status_updated.connect(self._update_task_status)
        self.worker.workflow_finished.connect(self._on_workflow_finished)
        self.worker.error_occurred.connect(self._on_error)

        self.thread.start()

    def _setup_connections(self):
        """Connects all signals and slots for the application."""
        # UI controls
        self.left_panel.start_button.clicked.connect(self._on_start_workflow)
        self.left_panel.stop_button.clicked.connect(self.worker.stop)
        self.left_panel.add_files_button.clicked.connect(self._add_files)
        self.left_panel.remove_file_button.clicked.connect(self._remove_selected_file)
        self.left_panel.file_list_view.selectionModel().selectionChanged.connect(self._update_button_states)
        self.center_panel.plan_view.customContextMenuRequested.connect(self._show_plan_context_menu)
        self.left_panel.configure_agents_button.clicked.connect(self._open_agent_config)
        self.bottom_panel.artifact_view.selectionModel().selectionChanged.connect(self._preview_artifact)

    @Slot(QItemSelection, QItemSelection)
    def _preview_artifact(self, selected, deselected):
        if not selected.indexes():
            return
        index = selected.indexes()[0]
        file_path = self.fs_model.filePath(index)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.bottom_panel.artifact_preview.setText(content)
            except Exception as e:
                self.bottom_panel.artifact_preview.setText(f"Error reading file: {e}")

    @Slot()
    def _open_agent_config(self):
        dialog = AgentConfigDialog(self)
        dialog.exec()

    @Slot()
    def _on_start_workflow(self):
        """Handles the 'Start Workflow' button click event."""
        goal = self.left_panel.goal_input.toPlainText().strip()
        if not goal:
            QMessageBox.warning(self, "Warning", "The goal cannot be empty.")
            return

        # Clear previous run's results
        self.bottom_panel.log_view.clear()
        self.plan_model.clear()
        self.plan_model.setHorizontalHeaderLabels(["Status", "Task", "Agent"])
        self.fs_model.setRootPath("") # Clear artifact view

        # Update UI state to 'running'
        self.left_panel.start_button.setText("Running...")
        self.left_panel.start_button.setEnabled(False)
        self.left_panel.stop_button.setEnabled(True)
        self.left_panel.goal_input.setEnabled(False)
        self.left_panel.orchestrator_combo.setEnabled(False)

        orchestrator = self.left_panel.orchestrator_combo.currentText()
        files = self.file_list_model.stringList()
        llm_provider = self.left_panel.llm_provider_combo.currentText()
        model_name = self.left_panel.model_name_input.text().strip()
        self.start_workflow_signal.emit(goal, orchestrator, files, llm_provider, model_name)

    @Slot(Plan)
    def _update_plan_view(self, plan: Plan):
        """Populates the plan QTreeView with tasks from the generated plan."""
        if not plan:
            return
        for task in plan.tasks:
            status_item = QStandardItem(STATUS_PENDING)
            status_item.setEditable(False)
            task_item = QStandardItem(f"{task.id}: {task.description}")
            task_item.setEditable(False)
            agent_item = QStandardItem(task.agent)
            agent_item.setEditable(False)
            exec_time_item = QStandardItem()
            exec_time_item.setEditable(False)
            error_item = QStandardItem()
            error_item.setEditable(False)
            # Store task.id in the status item for easy lookup
            status_item.setData(task.id, Qt.ItemDataRole.UserRole)
            self.plan_model.appendRow([status_item, task_item, agent_item, exec_time_item, error_item])

    @Slot(str)
    def _append_log_message(self, message: str):
        """Appends a message to the log view and parses it for status updates."""
        self.bottom_panel.log_view.appendPlainText(message.strip())

    @Slot(str, str, str, float)
    def _update_task_status(self, task_id: str, status: str, error_message: str, execution_time: float):
        """Finds a task by its ID in the plan view and updates its status icon."""
        for row in range(self.plan_model.rowCount()):
            item = self.plan_model.item(row, STATUS_COLUMN)
            if item and item.data(Qt.ItemDataRole.UserRole) == task_id:
                if status == "running":
                    item.setText(STATUS_RUNNING)
                elif status == "success":
                    item.setText(STATUS_SUCCESS)
                    self.plan_model.item(row, 3).setText(f"{execution_time:.2f}s")
                elif status == "error":
                    item.setText(STATUS_ERROR)
                    self.plan_model.item(row, 4).setText(error_message)
                return

    @Slot(str)
    def _on_workflow_finished(self, session_path: str):
        """Handles the completion of a workflow."""
        QMessageBox.information(self, "Success", "Workflow completed successfully.")
        self._reset_ui_state()
        self.fs_model.setRootPath(session_path)
        self.bottom_panel.artifact_view.setRootIndex(self.fs_model.index(session_path))
        self.bottom_panel.tabs.setCurrentIndex(1) # Switch to artifacts tab

    @Slot(str)
    def _on_error(self, error_message: str):
        """Displays an error message and resets the UI."""
        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_message}")
        self._reset_ui_state()

    @Slot()
    def _add_files(self):
        """Opens a file dialog to add files to the context list."""
        from PySide6.QtWidgets import QFileDialog
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Context Files")
        if file_paths:
            current_files = self.file_list_model.stringList()
            for path in file_paths:
                if path not in current_files:
                    current_files.append(path)
            self.file_list_model.setStringList(current_files)

    @Slot()
    def _remove_selected_file(self):
        """Removes the currently selected file from the context list."""
        selected_indexes = self.left_panel.file_list_view.selectedIndexes()
        if not selected_indexes:
            return
        row_to_remove = selected_indexes[0].row()
        self.file_list_model.removeRow(row_to_remove)

    @Slot()
    def _update_button_states(self):
        """Enables or disables the 'Remove' button based on selection."""
        self.left_panel.remove_file_button.setEnabled(len(self.left_panel.file_list_view.selectedIndexes()) > 0)

    @Slot(QPoint)
    def _show_plan_context_menu(self, pos):
        index = self.center_panel.plan_view.indexAt(pos)
        if not index.isValid():
            return

        menu = QMenu()
        view_details_action = menu.addAction("View Task Details")
        mark__complete_action = menu.addAction("Mark as Complete")
        reschedule_action = menu.addAction("Reschedule")

        action = menu.exec(self.center_panel.plan_view.viewport().mapToGlobal(pos))

        if action == view_details_action:
            self._view_task_details(index)
        elif action == mark_complete_action:
            self._mark_task_complete(index)
        elif action == reschedule_action:
            self._reschedule_task(index)

    def _view_task_details(self, index):
        row = index.row()
        task_id = self.plan_model.item(row, STATUS_COLUMN).data(Qt.ItemDataRole.UserRole)
        task_description = self.plan_model.item(row, TASK_COLUMN).text()
        task_agent = self.plan_model.item(row, AGENT_COLUMN).text()
        task_status = self.plan_model.item(row, STATUS_COLUMN).text()
        task_exec_time = self.plan_model.item(row, 3).text()
        task_error = self.plan_model.item(row, 4).text()

        details = f"""
        Task ID: {task_id}
        Description: {task_description}
        Agent: {task_agent}
        Status: {task_status}
        Execution Time: {task_exec_time}
        Error: {task_error}
        """
        QMessageBox.information(self, "Task Details", details)

    def _mark_task_complete(self, index):
        row = index.row()
        task_id = self.plan_model.item(row, STATUS_COLUMN).data(Qt.ItemDataRole.UserRole)
        self.worker.mark_task_as_complete(task_id)

    def _reschedule_task(self, index):
        pass

    def _reset_ui_state(self):
        """Resets the UI controls to their initial, idle state."""
        self.left_panel.start_button.setText("Start Workflow")
        self.left_panel.start_button.setEnabled(True)
        self.left_panel.stop_button.setEnabled(False)
        self.left_panel.goal_input.setEnabled(True)
        self.left_panel.orchestrator_combo.setEnabled(True)
        self._update_button_states()

    def closeEvent(self, event):
        """Ensures the worker thread is properly shut down on exit."""
        self.thread.quit()
        self.thread.wait()
        event.accept()