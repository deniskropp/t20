# Widget for displaying real-time logs

from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class StatusLogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statusLogWidget") # For stylesheet targeting
        self.layout = QVBoxLayout(self)
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setPlaceholderText("System logs and agent activities will appear here...")
        self.log_display.document().setDefaultFont(QFont("Roboto, Open Sans, Lato", 10))
        self.layout.addWidget(self.log_display)
        self.setLayout(self.layout)

    def append_log(self, message):
        # Basic coloring example - could be expanded based on message type
        formatted_message = message
        if "[ERROR]" in message or "ERROR:" in message:
            formatted_message = f"<font color=\"#FF0000\">{message}</font>"
        elif "[INFO]" in message or "INFO:" in message or "[SUCCESS]" in message or "COMPLETE" in message.upper():
            formatted_message = f"<font color=\"#00FF00\">{message}</font>"
        elif "[STDERR]" in message:
            formatted_message = f"<font color=\"#FFA500\">{message}</font>" # Orange for stderr
        elif "[UI ERROR]" in message:
             formatted_message = f"<font color=\"#FF4500\">{message}</font>" # Orangered for UI specific errors
        else:
            formatted_message = f"<font color=\"#B0C4DE\">{message}</font>" # LightSteelBlue for general messages

        self.log_display.append(formatted_message)
        self.log_display.verticalScrollBar().setValue(self.log_display.verticalScrollBar().maximum())

    def clear_log(self):
        self.log_display.clear()
