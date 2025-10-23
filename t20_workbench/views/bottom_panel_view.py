import os
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QPlainTextEdit,
    QTreeView,
    QSplitter,
    QTextEdit,
    QFileSystemModel,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class BottomPanelView(QWidget):
    """A widget that contains the logs and artifacts for the T20 Workbench."""

    def __init__(self, fs_model: QFileSystemModel, parent=None):
        super().__init__(parent)

        self.fs_model = fs_model

        self._setup_ui()

    def _setup_ui(self):
        """Initializes and arranges all UI widgets."""
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()

        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setFont(QFont("Courier New", 10))

        self.artifact_view = QTreeView()
        self.artifact_view.setModel(self.fs_model)
        self.fs_model.setRootPath(os.path.expanduser("~"))

        self.artifact_preview = QTextEdit()
        self.artifact_preview.setReadOnly(True)

        artifact_splitter = QSplitter(Qt.Orientation.Horizontal)
        artifact_splitter.addWidget(self.artifact_view)
        artifact_splitter.addWidget(self.artifact_preview)

        self.tabs.addTab(self.log_view, "Logs")
        self.tabs.addTab(artifact_splitter, "Artifacts")
        layout.addWidget(self.tabs)
