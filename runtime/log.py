"""Logging configuration for the runtime."""

import logging
import json
import sys
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init()

class JsonFormatter(logging.Formatter):
    """Formats log records as JSON."""
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(log_record)

class ConsoleFormatter(logging.Formatter):
    """A logging formatter that adds colors to the output."""

    def format(self, record):
        color = {
            logging.DEBUG: Style.DIM + Fore.WHITE,
            logging.INFO: Fore.WHITE,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.RED + Style.BRIGHT,
        }.get(record.levelno, Fore.WHITE)
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"

def setup_logging(log_level=logging.INFO, json_logging=False):
    """Configures the root logger for the runtime package."""
    logger = logging.getLogger("runtime")
    logger.setLevel(log_level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = JsonFormatter() if json_logging else ConsoleFormatter('%(message)s')
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
