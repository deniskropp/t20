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
    QTabWidget,
    QPlainTextEdit,
    QFileSystemModel,
    QMessageBox,
    QLabel,
    QHeaderView,
    QComboBox,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont
import yaml

from worker import Worker
from runtime.custom_types import Plan, Task

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
    start_workflow_signal = Signal(str, str, list)

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
        # --- Left Panel: Configuration & Controls ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self.goal_input = QTextEdit()
        self.goal_input.setPlaceholderText("Enter the high-level goal for the agents...")

        self.orchestrator_combo = QComboBox()

        self.file_list_view = QListView()
        self.file_list_view.setModel(self.file_list_model)

        file_buttons_layout = QHBoxLayout()
        self.add_files_button = QPushButton("Add File(s)")
        self.remove_file_button = QPushButton("Remove")
        file_buttons_layout.addWidget(self.add_files_button)
        file_buttons_layout.addWidget(self.remove_file_button)

        self.start_button = QPushButton("Start Workflow")
        self.stop_button = QPushButton("Stop Workflow")

        left_layout.addWidget(QLabel("Goal"))
        left_layout.addWidget(self.goal_input, stretch=2)
        left_layout.addWidget(QLabel("Orchestrator"))
        left_layout.addWidget(self.orchestrator_combo)
        left_layout.addWidget(QLabel("Context Files"))
        left_layout.addWidget(self.file_list_view, stretch=3)
        left_layout.addLayout(file_buttons_layout)
        left_layout.addWidget(self.start_button)
        left_layout.addWidget(self.stop_button)

        # --- Center Panel: Plan Visualization ---
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        self.plan_view = QTreeView()
        self.plan_view.setModel(self.plan_model)
        self.plan_model.setHorizontalHeaderLabels(["Status", "Task", "Agent"])
        self.plan_view.header().setSectionResizeMode(TASK_COLUMN, QHeaderView.ResizeMode.Stretch)
        self.plan_view.setColumnWidth(STATUS_COLUMN, 50)
        self.plan_view.setColumnWidth(AGENT_COLUMN, 150)
        center_layout.addWidget(QLabel("Execution Plan"))
        center_layout.addWidget(self.plan_view)

        # --- Bottom Panel: Logs & Artifacts ---
        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout(bottom_panel)
        self.tabs = QTabWidget()

        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setFont(QFont("Courier New", 10))

        self.artifact_view = QTreeView()
        self.artifact_view.setModel(self.fs_model)
        self.fs_model.setRootPath(os.path.expanduser("~"))

        self.tabs.addTab(self.log_view, "Logs")
        self.tabs.addTab(self.artifact_view, "Artifacts")
        bottom_layout.addWidget(self.tabs)

        # --- Splitter Layout ---
        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        top_splitter.addWidget(left_panel)
        top_splitter.addWidget(center_panel)
        top_splitter.setStretchFactor(0, 1)
        top_splitter.setStretchFactor(1, 3)

        main_splitter = QSplitter(Qt.Orientation.Vertical)
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(bottom_panel)
        main_splitter.setStretchFactor(0, 2)
        main_splitter.setStretchFactor(1, 1)

        self.setCentralWidget(main_splitter)

    def _populate_orchestrators(self):
        """Scans the agents directory and populates the orchestrator combo box."""
        try:
            agents_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agents'))
            if not os.path.isdir(agents_dir):
                self.log_message.emit("[UI-ERROR] Agents directory not found.")
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
            self.orchestrator_combo.addItems(sorted(orchestrators))
        except FileNotFoundError:
            self.log_message.emit(f"[UI-ERROR] Agents directory not found at expected path.")
        except yaml.YAMLError as e:
            self.log_message.emit(f"[UI-ERROR] Error parsing YAML in agents directory: {e}")
        except Exception as e:
            self.log_message.emit(f"[UI-ERROR] An unexpected error occurred while loading orchestrators: {e}")

    def _setup_worker_thread(self):
        """Creates and configures the worker thread for background processing."""
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.start()

    def _setup_connections(self):
        """Connects all signals and slots for the application."""
        # UI controls
        self.start_button.clicked.connect(self._on_start_workflow)
        self.add_files_button.clicked.connect(self._add_files)
        self.remove_file_button.clicked.connect(self._remove_selected_file)
        self.file_list_view.selectionModel().selectionChanged.connect(self._update_button_states)
        # Note: Stop button logic is more complex (thread termination) and is omitted for now.

        # Worker thread communication
        self.start_workflow_signal.connect(self.worker.run_workflow)
        self.worker.plan_generated.connect(self._update_plan_view)
        self.worker.log_message.connect(self._append_log_message)
        self.worker.task_status_updated.connect(self._update_task_status)
        self.worker.workflow_finished.connect(self._on_workflow_finished)
        self.worker.error_occurred.connect(self._on_error)

    @Slot()
    def _on_start_workflow(self):
        """Handles the 'Start Workflow' button click event."""
        goal = self.goal_input.toPlainText().strip()
        if not goal:
            QMessageBox.warning(self, "Warning", "The goal cannot be empty.")
            return

        # Clear previous run's results
        self.log_view.clear()
        self.plan_model.clear()
        self.plan_model.setHorizontalHeaderLabels(["Status", "Task", "Agent"])
        self.fs_model.setRootPath("") # Clear artifact view

        # Update UI state to 'running'
        self.start_button.setText("Running...")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.goal_input.setEnabled(False)
        self.orchestrator_combo.setEnabled(False)

        orchestrator = self.orchestrator_combo.currentText()
        files = self.file_list_model.stringList()
        self.start_workflow_signal.emit(goal, orchestrator, files)

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
            # Store task.id in the status item for easy lookup
            status_item.setData(task.id, Qt.ItemDataRole.UserRole)
            self.plan_model.appendRow([status_item, task_item, agent_item])

    @Slot(str)
    def _append_log_message(self, message: str):
        """Appends a message to the log view and parses it for status updates."""
        self.log_view.appendPlainText(message.strip())
        # Regex to find task execution messages
        match = re.search(r"executing step .*? '([T]\d+):", message)
        if match:
            task_id = match.group(1)
            self._update_task_status(task_id, "running")
        
        match_complete = re.search(r"Agent '(.*)' completed task: (.*)", message)
        if match_complete:
            # A bit of a hack: find task by description since ID isn't in log
            # A better implementation would have the runtime log the task ID on completion
            desc_fragment = match_complete.group(2)
            for row in range(self.plan_model.rowCount()):
                task_item = self.plan_model.item(row, TASK_COLUMN)
                status_item = self.plan_model.item(row, STATUS_COLUMN)
                if task_item and desc_fragment in task_item.text():
                    task_id = status_item.data(Qt.ItemDataRole.UserRole)
                    self._update_task_status(task_id, "success")
                    break

    @Slot(str, str)
    def _update_task_status(self, task_id: str, status: str):
        """Finds a task by its ID in the plan view and updates its status icon."""
        for row in range(self.plan_model.rowCount()):
            item = self.plan_model.item(row, STATUS_COLUMN)
            if item and item.data(Qt.ItemDataRole.UserRole) == task_id:
                if status == "running":
                    item.setText(STATUS_RUNNING)
                elif status == "success":
                    item.setText(STATUS_SUCCESS)
                elif status == "error":
                    item.setText(STATUS_ERROR)
                return

    @Slot(str)
    def _on_workflow_finished(self, session_path: str):
        """Handles the completion of a workflow."""
        QMessageBox.information(self, "Success", "Workflow completed successfully.")
        self._reset_ui_state()
        self.fs_model.setRootPath(session_path)
        self.artifact_view.setRootIndex(self.fs_model.index(session_path))
        self.tabs.setCurrentIndex(1) # Switch to artifacts tab

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
        selected_indexes = self.file_list_view.selectedIndexes()
        if not selected_indexes:
            return
        row_to_remove = selected_indexes[0].row()
        self.file_list_model.removeRow(row_to_remove)

    @Slot()
    def _update_button_states(self):
        """Enables or disables the 'Remove' button based on selection."""
        self.remove_file_button.setEnabled(len(self.file_list_view.selectedIndexes()) > 0)

    def _reset_ui_state(self):
        """Resets the UI controls to their initial, idle state."""
        self.start_button.setText("Start Workflow")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.goal_input.setEnabled(True)
        self.orchestrator_combo.setEnabled(True)
        self._update_button_states()

    def closeEvent(self, event):
        """Ensures the worker thread is properly shut down on exit."""
        self.thread.quit()
        self.thread.wait()
        event.accept()