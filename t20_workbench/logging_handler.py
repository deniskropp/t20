import logging
from PySide6.QtCore import QObject, Signal

class QtLogHandler(logging.Handler, QObject):
    """
    A custom logging handler that emits a Qt signal for each log record.
    This allows log messages from any thread to be safely displayed in the GUI.
    Inherits from QObject to handle signals and slots correctly.
    """
    new_log_message = Signal(str)

    def __init__(self, *args, **kwargs):
        # Initialize both parent classes
        logging.Handler.__init__(self, *args, **kwargs)
        QObject.__init__(self)

    def emit(self, record):
        """
        Formats the log record and emits the new_log_message signal.
        This method is thread-safe as it's called by the logging framework.
        """
        try:
            msg = self.format(record)
            self.new_log_message.emit(msg)
        except Exception:
            # Handle exceptions in logging itself, e.g., if GUI is closed
            self.handleError(record)
