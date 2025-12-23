# Getting Started with T20SDK

T20SDK is the Python SDK for the T20 Multi-Agent System. It allows you to build, orchestrate, and run teams of AI agents.

## Installation

```bash
pip install t20sdk
```
*(Note: As this is currently a local package, install via `pip install -e .` from the source root)*

## Basic Usage

### 1. Initialize the System

```python
from t20sdk.core.system import System
import os

# Initialize system with the path to your project root (where assets/ resides)
# In this example, we assume we are in the package root.
system = System(root_dir=os.getcwd())

# Setup the system (loads agents and config)
system.setup(orchestrator_name="Meta-AI")
```

### 2. Run a Task

```python
import asyncio

async def main():
    # Define a high-level goal
    goal = "Write a short poem about coding."

    # Start the system to generate a plan
    plan = await system.start(high_level_goal=goal)

    # Execute the plan
    async for task, result in system.run(plan):
        print(f"Task Completed: {task.description}")
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Project Structure

Expected project structure for `root_dir`:

```
my_project/
├── config/
│   └── runtime.yaml
├── assets/
│   ├── agents/
│   │   └── my_agent.yaml
│   └── prompts/
│       └── my_agent_instructions.txt
└── main.py
```
