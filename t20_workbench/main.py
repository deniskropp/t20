import sys
import os
from PySide6.QtWidgets import QApplication

# Add runtime to the path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main_window import MainWindow
from styles import APP_STYLE

def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
