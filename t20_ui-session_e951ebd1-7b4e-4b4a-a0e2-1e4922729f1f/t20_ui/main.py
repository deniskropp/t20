# Entry point for the PyQt6 application

import sys
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSplitter, QLabel, QPushButton, QTextEdit, QComboBox, QSpinBox, QLineEdit, QListWidget, QProgressBar, QHBoxLayout, QGridLayout, QFileDialog
from PyQt6.QtCore import Qt, QProcess, QObject, pyqtSignal, QUrl, QDir
from PyQt6.QtGui import QDesktopServices
import shutil

# Import necessary components from the local modules
from ui.main_window import MainWindow
from runtime.executor import RuntimeExecutor
from runtime.cli_handler import parse_gui_args, get_runtime_args_for_subprocess

# --- Stylesheets --- (Ideally imported from styles.py)
PRIMARY_COLOR = "#1A237E"    # Indigo 900
SECONDARY_COLOR = "#424242"   # Grey 700
ACCENT_COLOR = "#00ACC1"     # Cyan 500 (Teal)
ACCENT_HOVER_COLOR = "#00838F" # Darker Teal for hover
TEXT_LIGHT = "#F5F5F5"       # Off-white
TEXT_DARK = "#212121"        # Dark Grey
ERROR_COLOR = "#FF0000"
SUCCESS_COLOR = "#00FF00"
FONT_FAMILY = "Roboto, Open Sans, Lato"

MAIN_STYLESHEET = f"""
QWidget {{
    background-color: {SECONDARY_COLOR};
    color: {TEXT_LIGHT};
    font-family: "{FONT_FAMILY}";
    font-size: 11pt;
}}

QMainWindow {{
    background-color: {SECONDARY_COLOR};
    color: {TEXT_LIGHT};
}}

QSplitter::handle {{
    background-color: {PRIMARY_COLOR};
    width: 3px;
}}

QLabel {{
    color: {TEXT_LIGHT};
    font-weight: bold;
}}

QPushButton {{
    background-color: {ACCENT_COLOR};
    color: {TEXT_DARK};
    border: none;
    padding: 8px 15px;
    border-radius: 4px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {ACCENT_HOVER_COLOR};
}}

QPushButton#runButton {{
    background-color: {SUCCESS_COLOR};
    color: {TEXT_DARK};
    font-size: 14pt;
    padding: 10px;
}}

QPushButton#runButton:hover {{
    background-color: #00CC00;
}}

QTextEdit, QLineEdit, QComboBox, QSpinBox {{
    background-color: #374747; /* Darker Grey */
    color: {TEXT_LIGHT};
    border: 1px solid #616161;
    border-radius: 4px;
    padding: 5px;
}}

QTextEdit:read-only {{
    background-color: #303030; /* Slightly different dark for read-only */
    border: 1px solid #555555;
}}

QProgressBar {{
    border: 2px solid {ACCENT_COLOR};
    border-radius: 5px;
    text-align: center;
    color: {TEXT_LIGHT};
}}

QProgressBar::chunk {{
    background-color: {ACCENT_COLOR};
    width: 20px;  /* adjust as needed */
    margin: 0.5px;
}}

QListWidget {{
    border: 1px solid #616161;
    border-radius: 4px;
    padding: 5px;
    background-color: #374747;
}}

QListWidget::item {{
    padding: 5px;
}}

QListWidget::item:selected {{
    background-color: {ACCENT_COLOR};
    color: {TEXT_DARK};
}}

/* Specific overrides for status log */
#statusLogWidget QTextEdit {{ 
    font-family: "{FONT_FAMILY}";
    font-size: 10pt;
    background-color: #263238; /* Blue Grey 900 */
    border: 1px solid #455A64;
}}

/* Specific overrides for output display */
#outputDisplayWidget QTextEdit {{ 
    font-family: "{FONT_FAMILY}";
    font-size: 11pt;
    background-color: #263238; /* Blue Grey 900 */
    border: 1px solid #455A64;
}}

"""

def main():
    app = QApplication(sys.argv)

    # Parse arguments relevant to the GUI itself (e.g., theme)
    gui_args = parse_gui_args(sys.argv)
    
    # Apply theme based on parsed arguments (basic example)
    if gui_args.theme == 'dark':
        app.setStyleSheet(MAIN_STYLESHEET)
    # Add else for light theme or other customizations

    main_win = MainWindow()
    
    # Initialize the runtime executor
    runtime_executor = RuntimeExecutor()
    
    # Connect signals and slots between UI and executor
    main_win.connect_runtime_signals(runtime_executor)
    
    # Example of connecting the 'run_requested' signal from ConfigWidget
    main_win.config_area.run_requested.connect(lambda:
        runtime_executor.run_task(
            main_win.task_input.get_task_goal(),
            main_win.config_area.get_runtime_config()
        )
    )
    
    # Connect executor signals to update UI elements
    runtime_executor.log_message.connect(main_win.status_log.append_log)
    runtime_executor.progress_update.connect(main_win.progress_bar.update_progress)
    runtime_executor.task_output.connect(main_win.output_display.display_output)
    runtime_executor.artifacts_found.connect(main_win.artifact_browser.display_artifacts)
    runtime_executor.task_finished.connect(lambda: main_win.progress_bar.reset_progress())
    runtime_executor.error_occurred.connect(lambda msg: main_win.status_log.append_log(f"[CRITICAL ERROR] {msg}"))

    main_win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
