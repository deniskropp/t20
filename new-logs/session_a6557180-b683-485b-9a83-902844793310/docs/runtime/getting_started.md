# Getting Started

## Installation and Setup

To get started, ensure you have Python installed. The runtime can be installed via pip:

```bash
pip install -r requirements.txt
```

Followed by setting up any necessary environment variables for LLM providers.

## Quick Start Guide / Basic Usage Example

A simple example demonstrating how to run the system:

```bash
python -m runtime.sysmain "Your initial task description" -r 3 -f file1.txt file2.py
```

This command initiates the system with a high-level goal, executes it for 3 rounds, and includes `file1.txt` and `file2.py` as initial inputs.
