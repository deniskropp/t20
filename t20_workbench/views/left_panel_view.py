from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QListView,
    QComboBox,
    QLineEdit,
    QLabel,
)
from PySide6.QtCore import QStringListModel

class LeftPanelView(QWidget):
    """A widget that contains the configuration and controls for the T20 Workbench."""

    def __init__(self, file_list_model: QStringListModel, parent=None):
        super().__init__(parent)

        self.file_list_model = file_list_model

        self._setup_ui()

    def _setup_ui(self):
        """Initializes and arranges all UI widgets."""
        layout = QVBoxLayout(self)

        self.goal_input = QTextEdit()
        self.goal_input.setPlaceholderText("Enter the high-level goal for the agents...")

        self.orchestrator_combo = QComboBox()

        self.llm_provider_combo = QComboBox()
        self.model_name_input = QLineEdit()
        self.model_name_input.setPlaceholderText("Enter model name (e.g., gemini-1.5-pro)")

        self.file_list_view = QListView()
        self.file_list_view.setModel(self.file_list_model)

        file_buttons_layout = QHBoxLayout()
        self.add_files_button = QPushButton("Add File(s)")
        self.remove_file_button = QPushButton("Remove")
        file_buttons_layout.addWidget(self.add_files_button)
        file_buttons_layout.addWidget(self.remove_file_button)

        self.start_button = QPushButton("Start Workflow")
        self.stop_button = QPushButton("Stop Workflow")
        self.configure_agents_button = QPushButton("Configure Agents")

        layout.addWidget(QLabel("Goal"))
        layout.addWidget(self.goal_input, stretch=2)
        layout.addWidget(QLabel("Orchestrator"))
        layout.addWidget(self.orchestrator_combo)
        layout.addWidget(QLabel("LLM Provider"))
        layout.addWidget(self.llm_provider_combo)
        layout.addWidget(QLabel("Model Name"))
        layout.addWidget(self.model_name_input)
        layout.addWidget(QLabel("Context Files"))
        layout.addWidget(self.file_list_view, stretch=3)
        layout.addLayout(file_buttons_layout)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.configure_agents_button)
