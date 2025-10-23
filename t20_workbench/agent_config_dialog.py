from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QDialogButtonBox
import os

class AgentConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Agents")
        layout = QVBoxLayout(self)

        self.agent_list = QListWidget()
        layout.addWidget(self.agent_list)

        self.populate_agents()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_agent)
        layout.addWidget(self.edit_button)

    def populate_agents(self):
        agents_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agents'))
        if os.path.isdir(agents_dir):
            for filename in os.listdir(agents_dir):
                if filename.endswith('.yaml'):
                    self.agent_list.addItem(filename)

    def edit_agent(self):
        selected_item = self.agent_list.currentItem()
        if selected_item:
            agent_filename = selected_item.text()
            # Open a new dialog to edit the file
            # I will implement this later
            pass
