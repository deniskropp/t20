# System Runtime

This project is a system for running AI agents. It allows for the configuration and execution of agents, with support for different prompts and runtime environments.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd system-runtime-repository
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the system, execute the main runtime script:

```bash
python -m runtime.executor
```

## Project Structure

- `agents/`: Contains the configuration files for different agents (e.g., `analyzer.yaml`, `orchestrator.yaml`).
- `config/`: Contains the main runtime configuration for the system.
- `prompts/`: Contains the instruction prompts for the agents.
- `runtime/`: Contains the core logic for the system, including the executor and loader.
- `sessions/`: Stores session data, allowing the system to resume previous states.
- `requirements.txt`: Lists the Python dependencies for the project.
