import logging
import os
import re
from logging.handlers import RotatingFileHandler

# --- Configuration ---
LOG_LEVEL = logging.DEBUG
LOG_FILE_DIR = "logs"
LOG_FILE_NAME = "app.log"
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME)
MAX_FILE_SIZE = 1024 * 1024  # 1 MB
BACKUP_COUNT = 5

# --- Colored Formatter ---
class ColoredFormatter(logging.Formatter):
    """
    A custom logging formatter that adds colors to the log messages.
    It can color based on log level, or on regex matching of the message.
    """
    # ANSI escape codes for colors
    COLORS = {
        'DEBUG': '[94m',    # Blue
        'INFO': '[92m',     # Green
        'WARNING': '[93m',  # Yellow
        'ERROR': '[91m',    # Red
        'CRITICAL': '[95m', # Magenta
        'RESET': '[0m'      # Reset color
    }

    # Regex-based coloring rules (pattern, color)
    REGEX_RULES = [
        (re.compile(r"Agent instance created:"), '[93m'),  # Yellow
        (re.compile(r"Agent .*'s system prompt updated."), '[97m'),  # White
        (re.compile(r"Agent .* is executing task"), '[92m'),  # Green
        (re.compile(r"Warning: Agent output is not in expected AgentOutput format."), '[91m'), # Red
        (re.compile(r"--- System Runtime Bootstrap ---"), '[94m'),  # Light Blue
        (re.compile(r"Error: No agents could be instantiated."), '[91m'), # Red
        (re.compile(r"Session created:"), '[92m'),  # Green
        (re.compile(r"Artifact '.*' saved in session .*"), '[94m'),  # Blue
        (re.compile(r"Error saving artifact '.*'"), '[91m'), # Red
        (re.compile(r"Files provided:"), '[96m'),  # Cyan
        (re.compile(r"Error reading file .*"), '[91m'), # Red
        (re.compile(r"Generated plan:"), '[96m'),  # Cyan
        (re.compile(r"Orchestration failed: Could not generate a valid plan."), '[91m'), # Red
        (re.compile(r"Orchestrator .* is generating a plan for"), '[95m'),  # Magenta
    ]

    def format(self, record):
        """
        Formats the log record with the appropriate color.
        """
        log_message = super().format(record)
        
        # Check for regex-based coloring first
        for pattern, color in self.REGEX_RULES:
            if pattern.search(record.getMessage()):
                return f"{color}{log_message}{self.COLORS['RESET']}"

        # Fallback to level-based coloring
        return f"{self.COLORS.get(record.levelname, self.COLORS['RESET'])}{log_message}{self.COLORS['RESET']}"

# --- Setup ---
def setup_logging():
    """
    Sets up logging for the application.
    """
    # Create log directory if it doesn't exist
    if not os.path.exists(LOG_FILE_DIR):
        os.makedirs(LOG_FILE_DIR)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    # --- Console Handler ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)

    # --- File Handler ---
    file_handler = RotatingFileHandler(
        LOG_FILE_PATH,
        maxBytes=MAX_FILE_SIZE,
        backupCount=BACKUP_COUNT
    )
    file_handler.setLevel(LOG_LEVEL)

    # --- Formatters ---
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # --- Add Formatter to Handlers ---
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    # --- Add Handlers to Logger ---
    # Avoid adding handlers multiple times
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

# --- Main Application Logger ---
# It's good practice to use a named logger instead of the root logger directly
app_logger = logging.getLogger(__name__)

# --- Example Usage ---
if __name__ == '__main__':
    setup_logging()
    app_logger.info("Logging setup complete.")
    app_logger.debug("This is a debug message.")
    app_logger.warning("This is a warning message.")
    app_logger.error("This is an error message.")
