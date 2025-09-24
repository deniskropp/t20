# Widget for displaying task progress

from PyQt6.QtWidgets import QWidget, QProgressBar, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class ProgressWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("progressWidget")
        self.layout = QVBoxLayout(self)

        self.status_label = QLabel("Idle")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #B0C4DE;") # LightSteelBlue

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%v/%m steps | %p%") # Shows current, max, and percentage

        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.progress_bar)
        self.setLayout(self.layout)

    def update_progress(self, current_step, total_steps):
        if total_steps > 0:
            percentage = int((current_step / total_steps) * 100)
            self.progress_bar.setMaximum(total_steps)
            self.progress_bar.setValue(current_step)
            self.status_label.setText(f"Executing Step {current_step}/{total_steps}")
        else:
            # Handle cases where total_steps might not be known initially or is 0
            self.progress_bar.setValue(current_step) # Assume current_step is a progress value
            self.status_label.setText(f"Processing step {current_step}")
        self.progress_bar.setTextVisible(True)

    def set_status_text(self, text):
        self.status_label.setText(text)

    def reset_progress(self):
        self.progress_bar.setValue(0)
        self.progress_bar.setRange(0, 100)
        self.status_label.setText("Idle")
