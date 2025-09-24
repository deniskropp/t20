# Widget for task goal input

from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

class TaskInputWidget(QWidget):
    goal_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("taskInputWidget")
        self.layout = QVBoxLayout(self)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter your primary task goal here...")
        self.text_edit.setMinimumHeight(80)
        self.text_edit.textChanged.connect(self.emit_goal_changed)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)

    def get_task_goal(self):
        return self.text_edit.toPlainText().strip()

    def set_task_goal(self, goal):
        self.text_edit.setPlainText(goal)

    def clear_input(self):
        self.text_edit.clear()

    def emit_goal_changed(self):
        self.goal_changed.emit(self.get_task_goal())
