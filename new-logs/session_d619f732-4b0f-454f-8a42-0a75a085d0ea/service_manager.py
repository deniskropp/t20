import subprocess
import time
import sys
import os

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
            print(f"Service {service_name} is already running.")
            return

        try:
            print(f"Starting service: {service_name} with command: {command}")
            # Use Popen for non-blocking execution
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid) # os.setsid to create a new process group
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
            print(f"Error starting service {service_name}: {e}")
            # Handle initial start failure based on policy
            if restart_policy != 'no' and self.processes[service_name]['retries'] < max_retries:
                self.processes[service_name]['retries'] += 1
                print(f"Retrying service {service_name} in {retry_delay} seconds...")
                time.sleep(retry_delay)
                self.start_service(service_name) # Recursive call for retry
            else:
                print(f"Failed to start service {service_name} after {max_retries} retries.")

    def stop_service(self, service_name):
        if service_name in self.processes:
            process_info = self.processes[service_name]
            process = process_info['process']
            if process.poll() is None:  # If process is running
                print(f"Stopping service: {service_name}")
                try:
                    # Send SIGTERM to the process group
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    process.wait(timeout=5) # Wait for termination
                    print(f"Service {service_name} stopped.")
                except subprocess.TimeoutExpired:
                    print(f"Service {service_name} did not terminate gracefully, killing process group.")
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL) # Send SIGKILL to the process group
                    process.wait()
                except ProcessLookupError:
                    print(f"Service {service_name} process already terminated.")
                except Exception as e:
                    print(f"Error stopping service {service_name}: {e}")
            del self.processes[service_name]

    def monitor_services(self):
        for service_name, process_info in list(self.processes.items()): # Use list to allow modification during iteration
            process = process_info['process']
            exit_code = process.poll() # Check if process has exited

            if exit_code is not None: # Process has terminated
                print(f"Service {service_name} terminated with exit code: {exit_code}")
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
                    print(f"Restarting service {service_name} (Attempt {process_info['retries']}/{max_retries}) in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    self.start_service(service_name) # Restart the service
                else:
                    print(f"Service {service_name} will not be restarted (Max retries reached or policy forbids).")
                    del self.processes[service_name] # Remove from monitoring if not restarting

    def run(self):
        # Initial start of all services
        for service_name in self.service_configs:
            self.start_service(service_name)

        # Monitoring loop
        while self.running:
            self.monitor_services()
            time.sleep(2) # Check every 2 seconds

    def shutdown(self):
        print("Initiating shutdown...")
        self.running = False
        for service_name in list(self.processes.keys()):
            self.stop_service(service_name)
        print("All services stopped. Exiting.")

if __name__ == "__main__":
    # Example Service Configurations
    # In a real scenario, this would likely be loaded from a config file (e.g., JSON, YAML)
    # TAS: Load Service Configurations
    service_configurations = {
        "web_server": {
            "command": "python -m http.server 8000",
            "restart_policy": "always",
            "max_retries": 10,
            "retry_delay": 5
        },
        "background_task": {
            "command": "python background_worker.py", # Assumes background_worker.py exists
            "restart_policy": "on-failure",
            "max_retries": 5,
            "retry_delay": 10
        },
        "failing_service": {
            "command": "python failing_script.py", # Assumes failing_script.py exists and exits with non-zero code
            "restart_policy": "on-failure",
            "max_retries": 3,
            "retry_delay": 3
        }
    }

    # TAS: Initialize Orchestrator
    manager = ServiceManager(service_configurations)

    # Handle graceful shutdown via signals
    import signal
    def signal_handler(sig, frame):
        manager.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler) # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler) # Handle termination signal

    try:
        # TAS: Manage Service Lifecycle (through start_service and monitor_services)
        # TAS: Monitor Service Status (within monitor_services)
        # TAS: Implement Respawn Policy (within monitor_services)
        # TAS: Handle Process Errors (implicitly via subprocess and try-except blocks)
        # TAS: Implement Graceful Shutdown (via signal_handler and manager.shutdown())
        manager.run()
    except Exception as e:
        print(f"An unexpected error occurred in the main loop: {e}")
        manager.shutdown()
        sys.exit(1)
