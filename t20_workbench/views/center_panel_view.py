from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeView,
    QLabel,
    QHeaderView,
)
from PySide6.QtGui import QStandardItemModel
from PySide6.QtCore import Qt

# --- Constants for Plan View ---
STATUS_COLUMN = 0
TASK_COLUMN = 1
AGENT_COLUMN = 2

class CenterPanelView(QWidget):
    """A widget that contains the plan visualization for the T20 Workbench."""

    def __init__(self, plan_model: QStandardItemModel, parent=None):
        super().__init__(parent)

        self.plan_model = plan_model

        self._setup_ui()

    def _setup_ui(self):
        """Initializes and arranges all UI widgets."""
        layout = QVBoxLayout(self)

        self.plan_view = QTreeView()
        self.plan_view.setModel(self.plan_model)
        self.plan_model.setHorizontalHeaderLabels(["Status", "Task", "Agent", "Execution Time", "Error Message"])
        self.plan_view.header().setSectionResizeMode(TASK_COLUMN, QHeaderView.ResizeMode.Stretch)
        self.plan_view.setColumnWidth(STATUS_COLUMN, 50)
        self.plan_view.setColumnWidth(AGENT_COLUMN, 150)
        self.plan_view.setColumnWidth(3, 100)
        self.plan_view.setColumnWidth(4, 200)
        self.plan_view.setContextMenuPolicy(Qt.CustomContextMenu)

        layout.addWidget(QLabel("Execution Plan"))
        layout.addWidget(self.plan_view)
