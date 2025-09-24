# Placeholder for custom Qt signals if needed for complex inter-thread communication.
# Currently, signals are defined directly within RuntimeExecutor.

from PyQt6.QtCore import QObject, pyqtSignal

class RuntimeSignals(QObject):
    # This class can be used to centralize signal definitions if they grow complex
    # or are shared across multiple components beyond RuntimeExecutor.
    pass
