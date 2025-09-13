## Detailed Implementation Plan for Python Service Orchestrator

This document outlines the implementation plan for the Python script responsible for managing and respawning services, building upon the refined conceptual design.

**1. Module Breakdown:**

The script will be modularized to promote reusability, testability, and maintainability. Key modules include:

*   **`main.py` (Orchestrator Core):**
    *   Entry point of the script.
    *   Initializes logging, configuration, and service manager.
    *   Contains the main control loop for monitoring services.
    *   Handles signal processing for graceful shutdown.
    *   Manages the lifecycle of the Orchestrator itself (e.g., initiating self-restart if designed).

*   **`config_manager.py`:**
    *   Loads and validates service configurations from a specified file (e.g., JSON, YAML).
    *   Provides methods to access service configurations (command, restart policy, dependencies, etc.).
    *   Handles potential configuration file errors.

*   **`service_manager.py`:**
    *   Manages individual service processes.
    *   `start_service(service_config)`: Uses `subprocess.Popen` to launch a service.
    *   `stop_service(service_name)`: Sends SIGTERM to a service process.
    *   `restart_service(service_name)`: Stops and then starts a service.
    *   `get_service_status(service_name)`: Checks if a process is running using `Popen.poll()` or `psutil`.
    *   Maintains a registry of running service Popen objects and their states.

*   **`monitor.py`:**
    *   Contains the logic for the main monitoring loop.
    *   Periodically checks the status of all managed services.
    *   Detects unexpected service terminations.
    *   Triggers respawn actions via the `service_manager` based on defined policies.
    *   May incorporate dependency checking before respawning.

*   **`logger_config.py`:**
    *   Sets up the logging configuration (format, level, output handlers - e.g., file, console).
    *   Ensures consistent logging across all modules.

*   **`utils.py` (Optional):**
    *   Helper functions, e.g., for path manipulation, argument parsing, or specific OS interactions.

**2. Data Structures:**

*   **Service Configuration:** A dictionary or list of dictionaries, loaded from the configuration file. Each service entry should contain:
    *   `name`: Unique identifier for the service.
    *   `command`: The command to execute (list of strings).
    *   `working_dir`: Optional working directory.
    *   `environment`: Optional environment variables.
    *   `restart_policy`: (e.g., `always`, `on-failure`, `never`).
    *   `max_retries`: Maximum respawn attempts within a time window.
    *   `retry_delay`: Initial delay before first retry.
    *   `dependencies`: List of service names that must be running before this service starts.
    *   `timeout_start`: Maximum time to wait for service to start.
    *   `timeout_stop`: Maximum time to wait for service to stop.

*   **Service State Registry:** A dictionary within `service_manager.py` to track the state of each managed service:
    *   Key: `service_name`
    *   Value: A dictionary containing:
        *   `process`: The `subprocess.Popen` object.
        *   `status`: (e.g., `PENDING`, `STARTING`, `RUNNING`, `STOPPING`, `STOPPED`, `FAILED`, `RESTARTING`).
        *   `pid`: Process ID.
        *   `start_time`: Timestamp of last successful start.
        *   `retry_count`: Current number of respawn attempts.
        *   `last_exit_code`: Exit code of the last termination.

*   **Global State:** Potentially a small object or dictionary in `main.py` to hold global settings or flags (e.g., `is_shutting_down`).

**3. Control Flow:**

*   **Initialization:**
    1.  `main.py` starts.
    2.  `logger_config.py` initializes logging.
    3.  `config_manager.py` loads and validates the service configuration file.
    4.  `service_manager.py` initializes its internal state registry (empty).
    5.  `monitor.py` is initialized.
    6.  Orchestrator registers itself with its own supervisor (if applicable).

*   **Service Startup Sequence:**
    1.  The Orchestrator (in `main.py` or `monitor.py`) iterates through the loaded service configurations.
    2.  For each service, it checks dependencies. If dependencies are not met, it waits and retries.
    3.  Once dependencies are met (or if none exist), it calls `service_manager.start_service()`.
    4.  `start_service` uses `subprocess.Popen`, captures the `Popen` object, updates the state registry to `STARTING`, and potentially logs the start event.
    5.  The initial status check might confirm if it's `RUNNING` or immediately `FAILED`.

*   **Monitoring Loop (in `monitor.py`):**
    1.  Runs periodically (e.g., every 5-10 seconds).
    2.  Iterates through the `service_state_registry` in `service_manager.py`.
    3.  For each `RUNNING` service:
        *   Check `process.poll()`.
        *   If `poll()` returns an exit code (process terminated):
            *   Record the exit code and update status to `FAILED` or `STOPPED`.
            *   Evaluate `restart_policy`.
            *   If restart is required and `max_retries` not exceeded, schedule a restart (potentially with a delay).
            *   Call `service_manager.restart_service()`.
    4.  For services marked for restart:
        *   Perform dependency checks.
        *   Call `service_manager.restart_service()` which calls `stop_service` then `start_service`.
    5.  Handle new services added dynamically (if supported).
    6.  Log any status changes or detected issues.

*   **Graceful Shutdown (Signal Handling in `main.py`):**
    1.  Catch SIGINT/SIGTERM signals.
    2.  Set a global flag `is_shutting_down = True`.
    3.  Iterate through all managed services in the `service_state_registry`.
    4.  For each running service, call `service_manager.stop_service()`.
    5.  `stop_service` sends SIGTERM to the `Popen` object and waits for a defined `timeout_stop`.
    6.  If a service doesn't stop within the timeout, send SIGKILL.
    7.  Once all managed services are stopped, the Orchestrator exits.

*   **Self-Restart/Reload (Advanced - Optional):**
    *   If the script needs to reload its own code or restart itself:
        *   Use `os.exec*` to replace the current process with a new instance, passing necessary state or configuration.
        *   This requires careful handling to ensure services are shut down correctly before the replacement.
        *   Often better managed by an external supervisor like `systemd`.