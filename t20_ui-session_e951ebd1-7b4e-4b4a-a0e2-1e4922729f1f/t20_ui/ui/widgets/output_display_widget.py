# Widget for displaying final task output

from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class OutputDisplayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("outputDisplayWidget") # For stylesheet targeting
        self.layout = QVBoxLayout(self)
        self.output_text_edit = QTextEdit()
        self.output_text_edit.setReadOnly(True)
        self.output_text_edit.setPlaceholderText("Final task output will be displayed here...")
        self.output_text_edit.document().setDefaultFont(QFont("Roboto, Open Sans, Lato", 11))
        self.layout.addWidget(self.output_text_edit)
        self.setLayout(self.layout)

    def display_output(self, output_content):
        # Basic check if content is already HTML, otherwise treat as plain text
        if output_content.strip().startswith('<'):
            self.output_text_edit.setHtml(output_content)
        else:
            self.output_text_edit.setPlainText(output_content)
        self.output_text_edit.verticalScrollBar().setValue(0) # Scroll to top

    def clear_output(self):
        self.output_text_edit.clear()
