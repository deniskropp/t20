# Widget for browsing and managing artifacts

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QFileDialog, QListWidgetItem
from PyQt6.QtCore import QDir, QUrl, Qt
from PyQt6.QtGui import QDesktopServices
import os

class ArtifactBrowserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("artifactBrowserWidget")
        self.layout = QVBoxLayout(self)

        self.artifact_list = QListWidget()
        self.artifact_list.setSortingEnabled(True)
        self.artifact_list.itemDoubleClicked.connect(self.open_selected_artifact)
        self.layout.addWidget(self.artifact_list)

        self.button_layout = QHBoxLayout()
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_selected_artifact)
        self.save_button = QPushButton("Save As...")
        self.save_button.clicked.connect(self.save_selected_artifact_as)

        self.button_layout.addWidget(self.open_button)
        self.button_layout.addWidget(self.save_button)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.current_session_path = None
        self.artifacts_map = {}

    def display_artifacts(self, artifacts_data, session_path=""):
        self.artifact_list.clear()
        self.current_session_path = session_path
        self.artifacts_map = {}

        if not artifacts_data:
            item = QListWidgetItem("No artifacts found for this session.")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable) # Make non-selectable
            self.artifact_list.addItem(item)
            return

        for artifact_info in artifacts_data:
            # Assuming artifact_info is a dict like {'name': 'output.txt', 'path': '/path/to/session/output.txt'}
            item = QListWidgetItem(artifact_info['name'])
            item.setData(Qt.ItemDataRole.UserRole, artifact_info['path']) # Store full path using Qt.UserRole
            self.artifact_list.addItem(item)
            self.artifacts_map[artifact_info['name']] = artifact_info['path']

    def get_selected_artifact_path(self):
        selected_item = self.artifact_list.currentItem()
        if selected_item:
            return selected_item.data(Qt.ItemDataRole.UserRole)
        return None

    def open_selected_artifact(self):
        artifact_path = self.get_selected_artifact_path()
        if artifact_path and os.path.exists(artifact_path):
            try:
                QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(artifact_path)))
            except Exception as e:
                print(f"Error opening artifact {artifact_path}: {e}") # Log error
        elif artifact_path:
            print(f"Artifact path not found: {artifact_path}")
        else:
            print("No artifact selected.")

    def save_selected_artifact_as(self):
        artifact_path = self.get_selected_artifact_path()
        if artifact_path and os.path.exists(artifact_path):
            # Suggest original filename, but allow user to change
            suggested_filename = os.path.basename(artifact_path)
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Artifact As",
                suggested_filename,
                "All Files (*);;Text Files (*.txt);;Code Files (*.py *.html *.css *.js);;JSON Files (*.json);;Markdown Files (*.md)"
            )
            if save_path:
                try:
                    shutil.copy2(artifact_path, save_path)
                    print(f"Artifact saved to {save_path}")
                except Exception as e:
                    print(f"Error saving artifact {artifact_path} to {save_path}: {e}")
        else:
            print("No artifact selected or path is invalid.")

    def clear_artifacts(self):
        self.artifact_list.clear()
        self.current_session_path = None
        self.artifacts_map = {}
