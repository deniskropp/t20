"""This module serves as the main entry point for the command-line interface.

It parses command-line arguments and initiates the system bootstrap process,
acting as the primary interface for running the multi-agent system.
"""

import os
import argparse
import logging
from typing import Optional

from runtime.core import Session
from runtime.bootstrap import system_runtime_bootstrap
from runtime.loader import load_config
from runtime.log import setup_logging

logger = logging.getLogger(__name__)

def parse_command_line_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments for the runtime system.

    Returns:
        An argparse.Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Run the Gemini agent runtime.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    general_group = parser.add_argument_group("General Settings")
    general_group.add_argument("-p", "--plan-only", action="store_true", help="Generate only the plan without executing tasks.")
    general_group.add_argument("-r", "--rounds", type=int, default=1, help="The number of rounds to execute the workflow.")
    general_group.add_argument("-f", "--files", nargs='*', help="List of files to be used in the task.", default=[])

    orchestrator_group = parser.add_argument_group("Orchestrator Settings")
    orchestrator_group.add_argument("-o", "--orchestrator", type=str, help="The name of the orchestrator to use.", default="Meta-AI")
    orchestrator_group.add_argument("-m", "--model", type=str, help="Default LLM model to use.", default="gemini-2.5-flash-lite")

    parser.add_argument("task", type=str, help="The initial task for the orchestrator to perform.")

    args = parser.parse_args()

    if args.rounds < 1:
        parser.error("Number of rounds must be at least 1.")
    if not args.task:
        parser.error("The task argument is required.")

    return args

def setup_application_logging(log_level: str = "INFO") -> None:
    """
    Sets up the global logging configuration for the application.

    Args:
        log_level: The desired logging level (e.g., "DEBUG", "INFO", "WARNING").
    """
    try:
        setup_logging(level=log_level)
        logger.info(f"Logging initialized with level: {log_level}")
    except ValueError as e:
        logger.error(f"Invalid log level '{log_level}': {e}")
        raise

def load_system_configuration(project_root: str) -> dict:
    """
    Loads the system configuration from the config file.

    Args:
        project_root: The root directory of the project.

    Returns:
        A dictionary containing the system configuration.

    Raises:
        FileNotFoundError: If the config file is not found.
        Exception: For other errors during configuration loading.
    """
    config_path = os.path.join(project_root, 'config', 'runtime.yaml')
    try:
        config = load_config(config_path)
        logger.info(f"System configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {config_path}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading configuration: {e}")
        raise

class SystemRuntime:
    """
    Encapsulates the runtime state and logic for the system.
    """
    def __init__(self, project_root: str, args: argparse.Namespace) -> None:
        """
        Initializes the SystemRuntime.

        Args:
            project_root: The root directory of the project.
            args: The parsed command-line arguments.
        """
        self.project_root: str = project_root
        self.args: argparse.Namespace = args
        self.config: dict = {}
        self.session: Optional[Session] = None
        logger.debug(f"SystemRuntime initialized with project_root: {self.project_root}")
        logger.debug(f"Parsed arguments: {self.args}")

    def initialize(self) -> None:
        """
        Initializes the runtime environment, including logging and configuration.
        """
        # Attempt to use config for initial log level if available, else default to INFO
        initial_log_level = self.config.get("logging_level", "INFO") if self.config else "INFO"
        try:
            setup_application_logging(log_level=initial_log_level)
            self.config = load_system_configuration(self.project_root)
            
            # Re-setup logging if config provides a different level
            dynamic_log_level = self.config.get("logging_level", initial_log_level)
            if dynamic_log_level != initial_log_level:
                logger.info(f"Updating log level from config: {dynamic_log_level}")
                setup_application_logging(log_level=dynamic_log_level)

            logger.info("System initialization complete.")
        except (FileNotFoundError, KeyError, ValueError) as e:
            logger.error(f"Initialization error: {e}")
            raise
        except Exception as e:
            logger.exception(f"An unexpected error occurred during initialization: {e}")
            raise

    def run(self) -> None:
        """
        Initiates the core system bootstrap process.
        """
    #def system_runtime_bootstrap(root_dir: str, initial_task: str, plan_only: bool = False, rounds: int = 1, files: List[str] = [], orchestrator_name: Optional[str] = None, default_model: str = "Olli"):
        try:
            logger.info("Starting system runtime bootstrap...")
            system_runtime_bootstrap(
                root_dir=self.project_root,
                initial_task=self.args.task,
                plan_only=self.args.plan_only,
                rounds=self.args.rounds,
                files=self.args.files,
                orchestrator_name=self.args.orchestrator,
                default_model=self.args.model
            )
            logger.info("System runtime bootstrap finished.")
        except Exception as e:
            logger.exception(f"An error occurred during system runtime bootstrap: {e}")
            raise

def system_main():
    """
    Main entry point for the runtime system.
    Parses arguments, sets up logging and configuration, and runs the system.
    """
    try:
        args = parse_command_line_arguments()
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        runtime = SystemRuntime(project_root=project_root, args=args)
        runtime.initialize()
        runtime.run()

    except (FileNotFoundError, KeyError, ValueError) as e:
        logger.error(f"Critical configuration or initialization error: {e}")
        exit(1)
    except Exception as e:
        logger.exception(f"An unexpected error occurred during system main execution: {e}")
        exit(1)


if __name__ == "__main__":
    system_main()
