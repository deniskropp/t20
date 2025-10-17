APP_STYLE = """
QMainWindow {
    background-color: #2D2D2D;
    color: #E0E0E0;
}

QWidget {
    font-family: Inter, Segoe UI, Arial, sans-serif;
    font-size: 10pt;
}

QTextEdit, QPlainTextEdit, QListView, QTreeView {
    background-color: #252526;
    color: #CCCCCC;
    border: 1px solid #3E3E42;
    border-radius: 4px;
    padding: 4px;
}

QTextEdit:focus, QPlainTextEdit:focus, QListView:focus, QTreeView:focus {
    border: 1px solid #007ACC;
}

QPushButton {
    background-color: #007ACC;
    color: #FFFFFF;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #008AE6;
}

QPushButton:pressed {
    background-color: #006AB1;
}

QPushButton:disabled {
    background-color: #4A4A4A;
    color: #888888;
}

QTabWidget::pane {
    border-top: 2px solid #3E3E42;
}

QTabBar::tab {
    background: #252526;
    color: #CCCCCC;
    border: 1px solid #3E3E42;
    border-bottom: none;
    padding: 8px 16px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background: #2D2D2D;
    color: #FFFFFF;
    border-color: #007ACC;
}

QTabBar::tab:!selected:hover {
    background: #3E3E42;
}

QSplitter::handle {
    background-color: #3E3E42;
}

QSplitter::handle:horizontal {
    height: 3px;
}

QSplitter::handle:vertical {
    width: 3px;
}

QHeaderView::section {
    background-color: #3E3E42;
    color: #CCCCCC;
    padding: 4px;
    border: 1px solid #2D2D2D;
    font-weight: bold;
}

QLabel {
    color: #E0E0E0;
    font-weight: bold;
    margin-bottom: 4px;
}

QMessageBox {
    background-color: #2D2D2D;
}
"""
