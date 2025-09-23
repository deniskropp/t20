"""This module configures and sets up the logging for the application.

It defines the log format, level, and handlers (console, file, JSONL),
providing a centralized and consistent logging setup.
"""

import logging
import os
import re
import json
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style

# --- Configuration ---
LOG_LEVEL = "INFO"
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
        'DEBUG': Fore.YELLOW,
        'INFO': Fore.CYAN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA,
        'RESET': Style.RESET_ALL
    }

    # Regex-based coloring rules (pattern, color)
    REGEX_RULES_MESSAGES = [
        (re.compile(r"Agent instance created:"), Fore.YELLOW),
        (re.compile(r"Agent '.*' system prompt updated."), Fore.GREEN),
        (re.compile(r"Agent '.*' is executing task"), Fore.GREEN),
        (re.compile(r"Agent '.*' completed task"), Fore.GREEN),
        (re.compile(r"Warning: Agent output is not in expected AgentOutput format."), Fore.YELLOW),
        (re.compile(r"System Runtime"), Fore.CYAN),
        (re.compile(r"Error: No agents could be instantiated."), Fore.RED),
        (re.compile(r"Session created:"), Fore.GREEN),
        (re.compile(r"Artifact '.*' saved in session .*"), Fore.LIGHTBLUE_EX),
        (re.compile(r"Error saving artifact '.*'"), Fore.RED),
        (re.compile(r"Files provided:"), Fore.MAGENTA),
        (re.compile(r"Error reading file .*"), Fore.RED),
        (re.compile(r"Generated plan:"), Fore.WHITE),
        (re.compile(r"Orchestration failed: Could not generate a valid plan."), Fore.RED),
        (re.compile(r"Orchestrator .* is generating a plan for"), Fore.BLUE),
        (re.compile(r"Orchestrator .* is starting workflow round"), Fore.CYAN),
        (re.compile(r"Orchestrator has completed workflow round"), Fore.CYAN),
        (re.compile(r"Agent .* provided new prompts."), Fore.LIGHTGREEN_EX),
        (re.compile(r"Target agent '.*' not found for prompt update."), Fore.YELLOW),
        (re.compile(r"Error generating or validating plan for .*"), Fore.RED),
    ]

    COLORS_NAMES = {
        'runtime.orchestrator': Fore.LIGHTYELLOW_EX,
        'runtime.agent': Fore.GREEN,
        'runtime.sysmain': Fore.LIGHTRED_EX,
        'runtime.core': Fore.LIGHTBLUE_EX,
        'runtime.bootstrap': Fore.LIGHTRED_EX,
        'runtime.loader': Fore.LIGHTRED_EX,
        'runtime.llm': Fore.LIGHTMAGENTA_EX,
        'runtime.util': Fore.GREEN,
        'runtime.factory': Fore.LIGHTRED_EX,
        'runtime.paths': Fore.BLUE,
        'runtime.custom_types': Fore.CYAN,
    }

    def format(self, record):
        """
        Formats the log record with the appropriate color.
        """
        log_message = super().format(record)

        # Check for regex-based coloring first
        for pattern, color in self.REGEX_RULES_MESSAGES:
            if pattern.search(record.getMessage()):
                return f"{color}{log_message}{self.COLORS['RESET']}"

        # Check for logger name-based coloring
        for name_prefix, color in self.COLORS_NAMES.items():
            if record.name.startswith(name_prefix):
                return f"{color}{log_message}{self.COLORS['RESET']}"

        # Fallback to level-based coloring
        return f"{self.COLORS.get(record.levelname, self.COLORS['RESET'])}{log_message}{self.COLORS['RESET']}"

# --- Setup ---
def setup_logging(level: str = LOG_LEVEL):
    """
    Sets up logging for the application.
    """
    # Create log directory if it doesn't exist
    if not os.path.exists(LOG_FILE_DIR):
        os.makedirs(LOG_FILE_DIR)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # --- Console Handler ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # --- File Handler ---
    file_handler = RotatingFileHandler(
        LOG_FILE_PATH,
        maxBytes=MAX_FILE_SIZE,
        backupCount=BACKUP_COUNT
    )
    file_handler.setLevel(level)

    # --- Formatters ---
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "timestamp": self.formatTime(record, self.datefmt),
                "name": record.name,
                "level": record.levelname,
                "message": record.getMessage(),
                "pathname": record.pathname,
                "lineno": record.lineno,
                "funcName": record.funcName,
                "process": record.process,
                "thread": record.thread,
                "threadName": record.threadName,
            }
            if record.exc_info:
                log_record["exc_info"] = self.formatException(record.exc_info)
            if record.stack_info:
                log_record["stack_info"] = self.formatStack(record.stack_info)
            return json.dumps(log_record)

    # --- Add Formatter to Handlers ---
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    # --- Add Handlers to Logger ---
    # Avoid adding handlers multiple times
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        # --- JSONL File Handler ---
        jsonl_file_handler = RotatingFileHandler(
            os.path.join(LOG_FILE_DIR, "app.jsonl"),
            maxBytes=MAX_FILE_SIZE,
            backupCount=BACKUP_COUNT
        )
        jsonl_file_handler.setLevel(level)
        jsonl_file_handler.setFormatter(JsonFormatter())
        logger.addHandler(jsonl_file_handler)

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
