import os
import sys
import time
import signal
import pickle
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor

# --- Configuration --- 
CONFIG_FILE = 'services_config.json' # Assumed to exist and be loaded
LOG_FILE = 'service_manager.log'
MAX_RETRIES = 3
STATE_FILE = 'script_state.pkl'

# --- Logging Setup ---
def setup_logging():
    logging.basicConfig( 
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout) # Also log to stdout
        ]
    )

# --- State Management ---
class ScriptState:
    def __init__(self):
        self.service_status = {}
        self.last_restart_time = 0

def save_state(state):
    try:
        with open(STATE_FILE, 'wb') as f:
            pickle.dump(state, f)
        logging.info("Script state saved successfully.")
    except Exception as e:
        logging.error(f"Failed to save state: {e}")

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'rb') as f:
                state = pickle.load(f)
                logging.info("Script state loaded successfully.")
                return state
        except Exception as e:
            logging.error(f"Failed to load state: {e}")
            # Fallback to a new state if loading fails
            return ScriptState()
    else:
        logging.info("No previous state file found. Initializing new state.")
        return ScriptState()

# --- Service Management ---
class ServiceManager:
    def __init__(self, services_config):
        self.services = services_config
        self.processes = {}
        self.service_status = {}
        self.respawn_delays = {}
        self.MAX_RETRIES = MAX_RETRIES
        self.respawn_queue = [] # For managing concurrent respawns
        self.respawn_rate_limit = 5 # Max respawns per second
        self.last_respawn_time = 0

    def _start_service(self, service_name, command):
        if service_name in self.processes and self.processes[service_name].poll() is None:
            logging.warning(f"Service '{service_name}' is already running.")
            return
        
        logging.info(f"Starting service '{service_name}' with command: {command}")
        try:
            # Use subprocess.Popen for better process control and group management
            # Ensure to create a new process group for signal handling
            process = subprocess.Popen(
                command,
                shell=True, 
                preexec_fn=os.setsid, # Create a new process group
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes[service_name] = process
            self.service_status[service_name] = 'running'
            self.respawn_delays[service_name] = 0
            logging.info(f"Service '{service_name}' started successfully (PID: {process.pid}).")
        except Exception as e:
            logging.error(f"Failed to start service '{service_name}': {e}")
            self.service_status[service_name] = 'failed'

    def start_all_services(self, state):
        logging.info("Starting all services...")
        # Use ThreadPoolExecutor for parallel startup
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for service in self.services:
                if service not in state.service_status or state.service_status[service] != 'running':
                    command = self.services[service]['command']
                    futures.append(executor.submit(self._start_service, service, command))
            
            # Wait for all futures to complete and update state based on actual status
            for future in futures:
                # The _start_service function already updates self.service_status
                pass
        logging.info("All services initiated.")

    def stop_service(self, service_name):
        if service_name in self.processes and self.processes[service_name].poll() is None:
            logging.info(f"Stopping service '{service_name}' (PID: {self.processes[service_name].pid}).")
            try:
                # Use os.killpg to send signal to the entire process group
                os.killpg(os.getpgid(self.processes[service_name].pid), signal.SIGTERM)
                self.processes[service_name].wait(timeout=5) # Wait for graceful shutdown
                logging.info(f"Service '{service_name}' stopped.")
                self.service_status[service_name] = 'stopped'
            except ProcessLookupError:
                logging.warning(f"Process group for service '{service_name}' not found (already terminated?).")
                self.service_status[service_name] = 'stopped'
            except subprocess.TimeoutExpired:
                logging.error(f"Service '{service_name}' did not stop gracefully. Forcing kill.")
                os.killpg(os.getpgid(self.processes[service_name].pid), signal.SIGKILL)
                self.service_status[service_name] = 'stopped'
            except Exception as e:
                logging.error(f"Error stopping service '{service_name}': {e}")
                self.service_status[service_name] = 'error'
        else:
            logging.warning(f"Service '{service_name}' is not running or already stopped.")

    def stop_all_services(self):
        logging.info("Stopping all services...")
        for service_name in list(self.processes.keys()): # Iterate over a copy
            self.stop_service(service_name)
        self.processes.clear()
        logging.info("All services stopped.")

    def check_services(self, state):
        current_time = time.time()
        for service_name, process in list(self.processes.items()): # Iterate over a copy
            if process.poll() is not None: # Process has terminated
                exit_code = process.poll()
                logging.warning(f"Service '{service_name}' terminated with exit code {exit_code}.")
                
                # Update status and retry logic
                self.service_status[service_name] = 'failed'
                retries = state.service_status.get(service_name, {}).get('retries', 0) + 1
                state.service_status[service_name] = {'status': 'failed', 'retries': retries}

                if retries <= self.MAX_RETRIES:
                    # Add to respawn queue with a delay
                    delay = self.respawn_delays.get(service_name, 1) # Default delay 1 sec
                    logging.info(f"Scheduling respawn for '{service_name}' in {delay} seconds (Retry {retries}/{self.MAX_RETRIES}).")
                    self.respawn_queue.append((service_name, delay))
                else:
                    logging.error(f"Service '{service_name}' exceeded max retries ({self.MAX_RETRIES}). Not respawning.")
                    
                del self.processes[service_name] # Remove from active processes
        
        # Process respawn queue with rate limiting
        self._process_respawn_queue(current_time, state)

    def _process_respawn_queue(self, current_time, state):
        if not self.respawn_queue:
            return

        # Sort queue by delay (earliest first) - though not strictly necessary with rate limiting
        self.respawn_queue.sort(key=lambda x: x[1])

        respawn_count = 0
        # Filter queue for items ready to respawn
        ready_to_respawn = []
        remaining_queue = []
        for service_name, delay in self.respawn_queue:
            # Simple check: if delay has passed, consider it ready
            # More sophisticated: track actual scheduled respawn time
            if delay <= (current_time - self.last_respawn_time):
                 ready_to_respawn.append(service_name)
            else:
                 remaining_queue.append((service_name, delay))
        
        self.respawn_queue = remaining_queue

        for service_name in ready_to_respawn:
            if respawn_count >= self.respawn_rate_limit:
                logging.warning(f"Rate limit reached for respawns. Holding back '{service_name}'.")
                # Add back to queue with a slightly increased delay or reschedule
                self.respawn_queue.append((service_name, self.respawn_delays.get(service_name, 1) * 2))
                continue
            
            if current_time - self.last_respawn_time >= 1.0 / self.respawn_rate_limit: # Ensure at least minimum interval between respawns
                command = self.services[service_name]['command']
                logging.info(f"Respawning service '{service_name}'...")
                self._start_service(service_name, command)
                # Reset delay for next potential failure
                self.respawn_delays[service_name] = min(self.respawn_delays.get(service_name, 1) * 1.5, 60) # Exponential backoff, capped at 60s
                self.last_respawn_time = time.time()
                respawn_count += 1
            else:
                # Not enough time passed since last respawn, put back
                self.respawn_queue.append((service_name, delay))


# --- Self-Loading and Respawning Mechanism ---
def respawn_self(state):
    logging.info("Initiating self-respawn...")
    # Save current state before respawning
    save_state(state)
    
    # Use os.execv to replace the current process with a new instance
    # Pass arguments to the new process, including a flag indicating it's a respawn
    # sys.executable is the path to the Python interpreter
    # sys.argv[0] is the path to the script itself
    os.execv(sys.executable, [sys.executable, sys.argv[0]] + sys.argv[1:])

# --- Main Execution Logic ---
def main(is_respawn=False):
    setup_logging()
    logging.info("Service manager script started.")

    state = load_state() # Load state, potentially from previous run
    if not is_respawn:
        # If this is the initial start, clear old state if desired, or merge
        # For simplicity, we'll just use loaded state. If it's truly a fresh start,
        # state file would be missing and load_state() returns ScriptState()
        pass
    
    # Ensure essential state exists for services
    for service in services_config:
        if service not in state.service_status:
            state.service_status[service] = {'status': 'unknown', 'retries': 0}

    manager = ServiceManager(services_config)

    # Start all services that were not running or failed previously
    manager.start_all_services(state)

    try:
        while True:
            current_time = time.time()
            # Check if self-respawn is needed (e.g., based on a condition or external trigger)
            # For this example, let's simulate a respawn after a certain time or condition
            if current_time - state.last_restart_time > 300: # Example: respawn every 5 minutes
                logging.info("Simulating a periodic self-respawn.")
                respawn_self(state)
                # execv replaces the process, so this part is never reached after respawn
            
            manager.check_services(state)
            save_state(state) # Periodically save state
            time.sleep(5) # Check services every 5 seconds

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received. Shutting down gracefully.")
        manager.stop_all_services()
        save_state(state) # Save state one last time before exiting
        logging.info("Service manager script stopped.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        manager.stop_all_services()
        save_state(state)
        logging.info("Service manager script stopped due to error.")
        # Optionally, trigger a self-respawn on critical errors if needed
        # respawn_self(state)

if __name__ == "__main__":
    # Check if the script is being respawned by itself
    # This is a simple check; more robust methods might involve environment variables or specific arguments
    is_respawn_process = len(sys.argv) > 1 and sys.argv[1] == "--respawned"
    if is_respawn_process:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)]) # Re-setup logging for respawned process
        logging.info("Script respawned successfully.")
        # Remove the respawn flag argument for the actual main function
        sys.argv.pop(1)
        main(is_respawn=True)
    else:
        # Load configuration first to get services_config
        # This part assumes services_config is loaded from CONFIG_FILE
        # For demonstration, using a placeholder:
        import json
        try:
            with open(CONFIG_FILE, 'r') as f:
                services_config = json.load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file '{CONFIG_FILE}' not found. Exiting.")
            sys.exit(1)
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from '{CONFIG_FILE}'. Exiting.")
            sys.exit(1)
        
        # Add the respawn flag to sys.argv before calling main
        # This is a way to signal to the respawned process that it's a respawn
        sys.argv.append("--respawned")
        main(is_respawn=False)
