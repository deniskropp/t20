# Placeholder for the main application window

import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QSplitter
from PyQt6.QtCore import Qt

from .widgets.task_input_widget import TaskInputWidget
from .widgets.config_widget import ConfigWidget
from .widgets.status_log_widget import StatusLogWidget
from .widgets.progress_widget import ProgressWidget
from .widgets.output_display_widget import OutputDisplayWidget
from .widgets.artifact_browser_widget import ArtifactBrowserWidget
from . import styles

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("T20 Multi-Agent System UI")
        self.setGeometry(100, 100, 1200, 800) # x, y, width, height

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        # --- Top Section: Control & Configuration ---
        self.control_config_splitter = QSplitter(Qt.Orientation.Vertical)
        self.control_widget = QWidget()
        self.control_layout = QVBoxLayout(self.control_widget)

        self.task_input = TaskInputWidget()
        self.config_area = ConfigWidget()

        self.control_layout.addWidget(QLabel("Task Goal:"))
        self.control_layout.addWidget(self.task_input)
        self.control_layout.addWidget(QLabel("Runtime Configuration:"))
        self.control_layout.addWidget(self.config_area)

        self.control_config_splitter.addWidget(self.control_widget)

        # --- Middle Section: Status & Progress ---
        self.status_progress_widget = QWidget()
        self.status_progress_layout = QVBoxLayout(self.status_progress_widget)

        self.status_log = StatusLogWidget()
        self.progress_bar = ProgressWidget()

        self.status_progress_layout.addWidget(self.status_log)
        self.status_progress_layout.addWidget(self.progress_bar)

        self.control_config_splitter.addWidget(self.status_progress_widget)

        # --- Right Section: Output & Artifacts ---
        self.output_artifacts_splitter = QSplitter(Qt.Orientation.Vertical)
        self.output_display = OutputDisplayWidget()
        self.artifact_browser = ArtifactBrowserWidget()

        self.output_artifacts_splitter.addWidget(self.output_display)
        self.output_artifacts_splitter.addWidget(self.artifact_browser)

        # --- Main Layout Assembly using QSplitter for resizability ---
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.addWidget(self.control_config_splitter)
        self.main_splitter.addWidget(self.output_artifacts_splitter)

        self.main_layout.addWidget(self.main_splitter)

        self.central_widget.setLayout(self.main_layout)

        self.load_stylesheet()

    def load_stylesheet(self):
        # Apply stylesheet
        self.setStyleSheet(styles.MAIN_STYLESHEET)

    # Add methods to connect signals and slots for runtime integration
    def connect_runtime_signals(self, executor):
        # Example: Connect run button signal to executor
        self.config_area.run_button.clicked.connect(lambda:
            executor.run_task(
                self.task_input.get_task_goal(),
                self.config_area.get_runtime_config()
            )
        )
        # Connect executor signals to update UI widgets
        executor.log_message.connect(self.status_log.append_log)
        executor.progress_update.connect(self.progress_bar.update_progress)
        executor.task_output.connect(self.output_display.display_output)
        executor.artifacts_found.connect(self.artifact_browser.display_artifacts)

