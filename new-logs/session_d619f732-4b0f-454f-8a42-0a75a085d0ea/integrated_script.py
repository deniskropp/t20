import importlib
import sys
import os
import time
import subprocess
import signal
import json

# --- Service Manager Class (from Technical Expert's output) ---
class ServiceManager:
    def __init__(self, service_configs):
        self.service_configs = service_configs
        self.processes = {}
        self.running = True

    def start_service(self, service_name):
        config = self.service_configs[service_name]
        command = config['command']
        restart_policy = config.get('restart_policy', 'on-failure')
        max_retries = config.get('max_retries', 5)
        retry_delay = config.get('retry_delay', 5)

        if service_name in self.processes and self.processes[service_name]['process'].poll() is None:
            log(f"Service {service_name} is already running.")
            return

        try:
            log(f"Starting service: {service_name} with command: {command}")
            # Use Popen for non-blocking execution, create new process group for easier termination
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid) 
            self.processes[service_name] = {
                'process': process,
                'command': command,
                'restart_policy': restart_policy,
                'max_retries': max_retries,
                'retry_delay': retry_delay,
                'retries': 0,
                'start_time': time.time()
            }
        except Exception as e:
            log(f"Error starting service {service_name}: {e}")
            # Handle initial start failure based on policy
            if restart_policy != 'no' and self.processes[service_name]['retries'] < max_retries:
                self.processes[service_name]['retries'] += 1
                log(f"Retrying service {service_name} in {retry_delay} seconds...")
                time.sleep(retry_delay)
                self.start_service(service_name) # Recursive call for retry
            else:
                log(f"Failed to start service {service_name} after {max_retries} retries.")

    def stop_service(self, service_name):
        if service_name in self.processes:
            process_info = self.processes[service_name]
            process = process_info['process']
            if process.poll() is None:  # If process is running
                log(f"Stopping service: {service_name}")
                try:
                    # Send SIGTERM to the process group
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    process.wait(timeout=5) # Wait for termination
                    log(f"Service {service_name} stopped.")
                except subprocess.TimeoutExpired:
                    log(f"Service {service_name} did not terminate gracefully, killing process group.")
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL) # Send SIGKILL to the process group
                    process.wait()
                except ProcessLookupError:
                    log(f"Service {service_name} process already terminated.")
                except Exception as e:
                    log(f"Error stopping service {service_name}: {e}")
            del self.processes[service_name]

    def monitor_services(self):
        for service_name, process_info in list(self.processes.items()): # Use list to allow modification during iteration
            process = process_info['process']
            exit_code = process.poll() # Check if process has exited

            if exit_code is not None: # Process has terminated
                log(f"Service {service_name} terminated with exit code: {exit_code}")
                process_info['retries'] += 1
                restart_policy = process_info['restart_policy']
                max_retries = process_info['max_retries']
                retry_delay = process_info['retry_delay']

                should_restart = False
                if restart_policy == 'always':
                    should_restart = True
                elif restart_policy == 'on-failure' and exit_code != 0:
                    should_restart = True
                elif restart_policy == 'on-abnormal-exit' and exit_code not in [0, 1]: # Example: 0 is success, 1 might be controlled exit
                    should_restart = True

                if should_restart and process_info['retries'] <= max_retries:
                    log(f"Restarting service {service_name} (Attempt {process_info['retries']}/{max_retries}) in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    self.start_service(service_name) # Restart the service
                else:
                    log(f"Service {service_name} will not be restarted (Max retries reached or policy forbids).")
                    del self.processes[service_name] # Remove from monitoring if not restarting

    def run_monitoring(self):
        # Monitoring loop
        while self.running:
            self.monitor_services()
            time.sleep(2) # Check every 2 seconds

    def shutdown(self):
        log("Initiating shutdown...")
        self.running = False
        for service_name in list(self.processes.keys()):
            self.stop_service(service_name)
        log("All services stopped. Exiting.")

# --- Logging Utility (from self_loader.py) ---
def log(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

# --- Self-Loading and Respawning Logic (integrated from self_loader.py) ---

# --- TAS: Define Orchestration Strategy (from T8)
# Using ServiceManager for orchestration and os.execv for self-respawn.

# --- TAS: Load Service Configurations (from T9)
# Load configurations from a JSON file
def load_config(config_path='services_config.json'):
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
            # Convert list of services to a dictionary keyed by service name
            services_dict = {svc['name']: svc for svc in config_data.get('services', [])}
            log(f"Configuration loaded successfully from {config_path}")
            return services_dict
    except FileNotFoundError:
        log(f"Configuration file not found at {config_path}. Using default dummy services.")
        # Fallback to default dummy services if config file is missing
        return {
            "example_service_1": {
                "command": f"{sys.executable} example_service_1.py",
                "restart_policy": "always",
                "max_retries": 10,
                "retry_delay": 5
            },
            "example_service_2": {
                "command": f"{sys.executable} example_service_2.py",
                "restart_policy": "on-failure",
                "max_retries": 5,
                "retry_delay": 10
            },
            "failing_service_demo": {
                "command": f"{sys.executable} failing_script.py",
                "restart_policy": "on-failure",
                "max_retries": 3,
                "retry_delay": 3
            }
        }
    except json.JSONDecodeError:
        log(f"Error decoding JSON from {config_path}. Using default dummy services.")
        # Fallback for invalid JSON
        return {
            "example_service_1": {
                "command": f"{sys.executable} example_service_1.py",
                "restart_policy": "always",
                "max_retries": 10,
                "retry_delay": 5
            },
            "example_service_2": {
                "command": f"{sys.executable} example_service_2.py",
                "restart_policy": "on-failure",
                "max_retries": 5,
                "retry_delay": 10
            },
            "failing_service_demo": {
                "command": f"{sys.executable} failing_script.py",
                "restart_policy": "on-failure",
                "max_retries": 3,
                "retry_delay": 3
            }
        }

# --- TAS: Implement Respawn Policy (from T9)
def respawn_self(reason=""): 
    log(f"Initiating self-respawn. Reason: {reason}")
    log(f"Current script: {sys.argv[0]}")
    log(f"Arguments: {sys.argv[1:]}")
    
    new_args = [sys.executable, os.path.abspath(__file__)]
    new_args.append("--respawned") 
    
    log(f"Executing: {' '.join(new_args)}")
    
    try:
        os.execv(sys.executable, new_args)
    except OSError as e:
        log(f"Failed to respawn script: {e}")
        sys.exit(1)

# --- TAS: Implement Graceful Shutdown (from T8 & T9) ---
def graceful_shutdown(service_manager=None):
    log("Initiating graceful shutdown...")
    if service_manager:
        service_manager.shutdown()
    log("Main process shutting down.")

# --- Main Execution Logic ---
def main():
    log("Script started.")
    
    service_manager = None
    
    # Check if this is a respawned instance (optional, for demonstration)
    if "--respawned" in sys.argv:
        log("This is a respawned instance.")
        # Potentially adjust behavior for respawned instance

    # --- Dynamic Loading and Service Management --- 
    # Load service configurations from JSON
    service_configs = load_config()
    
    service_manager = ServiceManager(service_configs)
    
    # Start the service monitoring in a separate thread or process if needed for complex scenarios.
    # For this example, we'll run it sequentially or manage its lifecycle.
    # A common pattern is to fork or thread the monitoring loop.
    # Here, we'll run it in the main thread after initial service starts.
    
    # Initial start of all services managed by ServiceManager
    for service_name in service_configs:
        service_manager.start_service(service_name)

    # --- Handling Signals for Graceful Shutdown ---
    def signal_handler(sig, frame):
        graceful_shutdown(service_manager)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler) # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler) # Handle termination signal

    # --- Main Loop: Keep script alive and monitor services ---
    try:
        # TAS: Manage Service Lifecycle (through start_service and monitor_services)
        # TAS: Monitor Service Status (within monitor_services)
        # TAS: Implement Respawn Policy (within monitor_services)
        # TAS: Handle Process Errors (implicitly via subprocess and try-except blocks)
        # TAS: Implement Graceful Shutdown (via signal_handler and manager.shutdown())
        service_manager.run_monitoring()
        
    except Exception as e:
        log(f"An unexpected error occurred in the main loop: {e}")
        graceful_shutdown(service_manager)
        # Optionally, trigger a self-respawn on critical errors
        respawn_self(f"Critical error in main loop: {e}")

if __name__ == "__main__":
    # --- Create dummy service files for demonstration if they don't exist ---
    if not os.path.exists("example_service_1.py"):
        with open("example_service_1.py", "w") as f:
            f.write("import time\nimport sys\nimport os\n\ndef run():\n    print('[Service 1] Running...')\n    # Simulate a process that might fail randomly\n    fail_chance = 0.1 # 10% chance of failure\n    counter = 0\n    while True:\n        print(f'[Service 1] Heartbeat... (counter: {counter})')\n        time.sleep(2)\n        counter += 1\n        if os.environ.get('FAIL_SERVICE_1') == 'true' and counter % 5 == 0: # Example condition to fail\n             print('[Service 1] Simulating failure!')\n             sys.exit(1)\n\ndef stop():\n    print('[Service 1] Stopping gracefully...')\n")

    if not os.path.exists("example_service_2.py"):
        with open("example_service_2.py", "w") as f:
            f.write("import time\n\ndef run():\n    print('[Service 2] Running...')\n    while True:\n        print('[Service 2] Working...')\n        time.sleep(3)\n\ndef stop():\n    print('[Service 2] Stopping gracefully...')\n")

    if not os.path.exists("failing_script.py"):
        with open("failing_script.py", "w") as f:
            f.write("import time\nimport sys\n\nprint('[Failing Script] Starting up...')\ntime.sleep(1)\nprint('[Failing Script] Exiting with error code 1...')\nsys.exit(1)\n")

    main()
