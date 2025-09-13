# Python Service Manager Script Documentation

## Functionality

The script acts as a robust service manager with self-healing capabilities. Its primary functions include:

1.  **Service Management:** It can start, stop, and monitor a list of services defined in a configuration file (`services_config.json`).
2.  **Automatic Respawning:** If a managed service crashes or terminates unexpectedly, the script automatically attempts to restart it up to a defined maximum number of retries.
3.  **State Preservation:** Critical state information (like service status and retry counts) is periodically saved using `pickle` to a state file (`script_state.pkl`). This allows the script to resume its state across restarts or self-respawns, ensuring continuity.
4.  **Self-Loading/Respawning:** The script can replace itself with a new instance using `os.execv`. This is primarily used for maintenance or critical error recovery, ensuring the manager itself is restarted with a clean slate while preserving essential operational context.
5.  **Graceful Shutdown:** Responds to `KeyboardInterrupt` (Ctrl+C) by attempting to stop all managed services gracefully before exiting.
6.  **Error Handling & Logging:** Implements comprehensive logging to a file (`service_manager.log`) and standard output, capturing startup, shutdown, and error events. Error reporting is enhanced to be more resilient under stress.
7.  **Parallel Service Startup:** Utilizes `concurrent.futures.ThreadPoolExecutor` to start multiple services concurrently, significantly reducing overall initialization time.
8.  **Rate Limiting:** Includes a mechanism to limit the rate of service respawns, preventing system overload during periods of multiple service failures.
9.  **Configuration Driven:** Service definitions, including commands, are loaded from an external JSON file, making it easy to manage services without modifying the script itself.

## Usage

1.  **Prerequisites:**
    *   Python 3.6+
    *   A `services_config.json` file in the same directory as the script.

2.  **Configuration (`services_config.json`):**
    The `services_config.json` file should be a JSON array of objects, where each object defines a service:
    ```json
    [
      {
        "name": "my_service_1",
        "command": "python /path/to/my_service_1.py --config /etc/my_service_1.conf"
      },
      {
        "name": "another_service",
        "command": "/usr/local/bin/another_app -d"
      }
    ]
    ```
    *   `name`: A unique identifier for the service.
    *   `command`: The shell command to execute to start the service.

3.  **Running the Script:**
    Execute the script from your terminal:
    ```bash
    python your_script_name.py
    ```
    The script will start, load services from `services_config.json`, and begin monitoring them.

4.  **Self-Respawn Trigger:**
    The script is configured to periodically respawn itself (e.g., every 5 minutes by default) to ensure the manager process itself remains healthy. This is triggered internally.

## Configuration Parameters

*   `CONFIG_FILE`: (Default: `'services_config.json'`) Path to the JSON file containing service definitions.
*   `LOG_FILE`: (Default: `'service_manager.log'`) Path to the log file.
*   `MAX_RETRIES`: (Default: `3`) Maximum number of times a crashed service will be automatically restarted.
*   `STATE_FILE`: (Default: `'script_state.pkl'`) File used for saving and loading the script's operational state.
*   **Internal Parameters:** `respawn_rate_limit`, exponential backoff delays, and self-respawn intervals are configured within the script and can be adjusted by modifying the code.

## Maintenance Procedures

1.  **Monitoring Logs:** Regularly check the `service_manager.log` file for any errors, warnings, or unusual activity related to service startups, shutdowns, or respawns.

2.  **Updating Service Configuration:** To add, remove, or modify services, edit the `services_config.json` file. The script will pick up these changes upon its next restart (either manual or self-respawn).

3.  **Manual Restart:** To restart the service manager itself (e.g., after updating the script or configuration), stop it manually (Ctrl+C) and then restart it:
    ```bash
    python your_script_name.py
    ```

4.  **State File Management:** The `script_state.pkl` file stores the operational state. In most cases, it should be left untouched. If you need to perform a completely clean start (e.g., reset all retry counts and statuses), you can manually delete this file before running the script. The script will then initialize with a fresh state.

5.  **Script Updates:** If the `your_script_name.py` file is updated, the next time it performs a self-respawn, the new version will be loaded. Alternatively, a manual stop and start will use the updated script immediately.

6.  **Troubleshooting:**
    *   **Service Not Starting:** Check the `services_config.json` for correct command syntax and paths. Examine `service_manager.log` for specific error messages during startup.
    *   **Excessive Respawning:** If a service repeatedly crashes, review its logs for the root cause. The `MAX_RETRIES` setting prevents infinite loops, but the underlying issue needs addressing.
    *   **Manager Unresponsive:** Check system resources (CPU, memory). If the manager process itself is consuming excessive resources or unresponsive, investigate potential issues within the manager script (e.g., deadlocks, infinite loops) by examining its logs and potentially triggering a manual restart.
