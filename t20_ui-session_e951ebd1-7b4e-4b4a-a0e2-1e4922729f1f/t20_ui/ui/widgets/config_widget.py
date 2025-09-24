# Widget for runtime configuration

from PyQt6.QtWidgets import QWidget, QComboBox, QLineEdit, QPushButton, QGridLayout, QLabel, QSpinBox
from PyQt6.QtCore import pyqtSignal

class ConfigWidget(QWidget):
    run_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("configWidget")
        self.layout = QGridLayout(self)

        # Orchestrator selection
        self.orchestrator_label = QLabel("Orchestrator:")
        self.orchestrator_combo = QComboBox()
        # Populate with agents known to be orchestrators or commonly used
        self.orchestrator_combo.addItems(["LaCogito", "MetaAI", "Qwen3-WebDev", "LaMetta", "LaTask", "LaTASe"])
        self.layout.addWidget(self.orchestrator_label, 0, 0)
        self.layout.addWidget(self.orchestrator_combo, 0, 1)

        # Model selection
        self.model_label = QLabel("Model:")
        self.model_combo = QComboBox()
        self.model_combo.addItems(["gemini-1.5-flash-latest", "gpt-4o", "ollama/llama3", "gpt-3.5-turbo"])
        self.layout.addWidget(self.model_label, 1, 0)
        self.layout.addWidget(self.model_combo, 1, 1)

        # Rounds
        self.rounds_label = QLabel("Rounds:")
        self.rounds_spinbox = QSpinBox()
        self.rounds_spinbox.setRange(1, 100)
        self.rounds_spinbox.setValue(5)
        self.layout.addWidget(self.rounds_label, 2, 0)
        self.layout.addWidget(self.rounds_spinbox, 2, 1)

        # Files input
        self.files_label = QLabel("Files:")
        self.files_input = QLineEdit()
        self.files_input.setPlaceholderText("Optional: path/to/file.txt ...")
        self.layout.addWidget(self.files_label, 3, 0)
        self.layout.addWidget(self.files_input, 3, 1)

        # Run Button
        self.run_button = QPushButton("Run Task")
        self.run_button.setObjectName("runButton") # For styling
        self.run_button.clicked.connect(self.emit_run_requested)
        self.layout.addWidget(self.run_button, 4, 0, 1, 2) # Span across two columns

        self.setLayout(self.layout)

    def get_runtime_config(self):
        return {
            "orchestrator": self.orchestrator_combo.currentText(),
            "model": self.model_combo.currentText(),
            "rounds": self.rounds_spinbox.value(),
            "files": [f.strip() for f in self.files_input.text().split() if f.strip()]
        }

    def set_runtime_config(self, config):
        if config.get("orchestrator") in [self.orchestrator_combo.itemText(i) for i in range(self.orchestrator_combo.count())]:
            self.orchestrator_combo.setCurrentText(config["orchestrator"])
        if config.get("model") in [self.model_combo.itemText(i) for i in range(self.model_combo.count())]:
            self.model_combo.setCurrentText(config["model"])
        self.rounds_spinbox.setValue(config.get("rounds", 5))
        self.files_input.setText(" ".join(config.get("files", [])))

    def emit_run_requested(self):
        self.run_requested.emit()

    def clear_config(self):
        self.orchestrator_combo.setCurrentIndex(0)
        self.model_combo.setCurrentIndex(0)
        self.rounds_spinbox.setValue(5)
        self.files_input.clear()
