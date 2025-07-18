# System Runtime

This project is a system for running AI agents. It allows for the configuration and execution of agents, with support for different prompts and runtime environments.

## Project Structure

- `agents/`: Contains the configuration files for different agents. Each YAML file defines an agent's name, role, goal, model, and optionally, its team members and delegation strategy.
    - `aurora.yaml`: Defines the Aurora agent (Designer).
    - `kodax.yaml`: Defines the Kodax agent (Engineer).
    - `lyra.yaml`: Defines the Lyra agent (Prompt Engineer).
    - `orchestrator.yaml`: Defines the Meta-AI agent (Orchestrator), which manages the workflow and delegates tasks to other agents.
    - `tase.yaml`: Defines the TASe agent (Task-Agnostic Step extractor).
- `config/`: Contains the main runtime configuration for the system.
    - `runtime.yaml`: Specifies the default agent, maximum concurrent agents, logging level, and API endpoints.
- `prompts/`: Contains the instruction prompts for the agents, guiding their behavior and responses.
    - `aurora_instructions.txt`: Instructions for the Aurora agent.
    - `kodax_instructions.txt`: Instructions for the Kodax agent.
    - `lyra_instructions.txt`: Instructions for the Lyra agent.
    - `orchestrator_instructions.txt`: Instructions for the Orchestrator agent.
    - `tase_instructions.txt`: Instructions for the TASe agent.
- `runtime/`: Contains the core logic for the system.
    - `executor.py`: The main script for executing agent workflows.
    - `loader.py`: Utility functions for loading configurations, agent templates, and prompts.
    - `__init__.py`: Makes the runtime directory a Python package.
- `sessions/`: Stores session data, allowing the system to resume previous states and track artifacts.
- `requirements.txt`: Lists the Python dependencies for the project.
- `3rdparty.txt`: Lists third-party software used in the project.
- `.env`: Environment variables for the project.
- `.gitignore`: Specifies intentionally untracked files that Git should ignore.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:deniskropp/t20
    cd t20
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the system, execute the main runtime script with an initial task:

```bash
python -m runtime.executor "Your initial task description here"
```

For example:
```bash
python -m runtime.executor "Design and implement a new mobile UI for a task management app."
```

After running, check out all of the session's artifacts, especially the last stage, or the last result from each agent...
