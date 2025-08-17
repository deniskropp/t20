Links: [MTC|LCP](https://ai.violass.club/mtc-lcp/)


# T20 Multi-Agent System

T20 is a sophisticated, multi-agent framework designed to tackle complex tasks through collaborative AI. It employs an orchestrator-delegate model where a primary "Orchestrator" agent dynamically creates a plan and delegates sub-tasks to a team of specialized agents, each powered by different models from the Google Gemini family.

The system is built for autonomy and traceability. Once given a high-level goal, the agents work together, passing context and artifacts between steps, until the objective is met. Every action, prompt, and output is saved in a distinct session directory for easy debugging and review.

---

## Core Concepts

The workflow of the T20 system follows a clear, powerful pattern:

1.  **Initialization**: The user provides a single, high-level goal via a command-line interface (e.g., "Design a modern landing page for a new SaaS product").
2.  **Dynamic Planning**: The `Orchestrator` agent (Meta-AI) analyzes the goal and the capabilities of its team members. It then queries a powerful LLM (like Gemini 2.5 Pro) to generate a structured, step-by-step plan in JSON format. This plan outlines the roles and specific tasks required to achieve the goal.
3.  **Task Delegation & Execution**: The `Orchestrator` proceeds through the plan, assigning each task to the appropriate specialized agent based on their role (e.g., a design task goes to `Aurora`, the Designer).
4.  **Contextual Collaboration**: The output (artifact) of each step is saved and can be used as input for subsequent steps. This creates a chain of context, allowing agents to build upon each other's work.
5.  **Meta-Learning & Adaptation**: A unique `Prompt Engineer` agent (Lyra) can be tasked with refining the system prompts of other agents *during* the workflow, optimizing their performance for the specific goal at hand.
6.  **Session Logging**: The entire process—from the initial plan to the final output—is meticulously logged in a dedicated session folder, providing full transparency.

## Features

-   **Declarative Agent Definition**: Agents are defined in simple, easy-to-read YAML files.
-   **Dynamic, AI-Generated Plans**: No hardcoded workflows. The Orchestrator creates a custom plan for every unique goal.
-   **Role-Based Delegation**: Tasks are intelligently assigned to agents best suited for the job.
-   **Structured LLM Outputs**: Utilizes JSON schema enforcement with Pydantic for reliable, machine-readable plans from the Orchestrator.
-   **Stateful Sessions**: Each run is isolated in a session directory containing all artifacts, prompts, and results.
-   **CLI-Driven**: Simple and straightforward to run from the command line.
-   **Powered by Google Gemini**: Leverages a suite of Gemini models, from the highly capable `gemini-2.5-pro` for orchestration to the fast and efficient `gemini-2.5-flash-lite` for specialized tasks.

## The Team

The system comes pre-configured with a team of specialized agents:

| Name     | Role                        | Goal                                                                                         | Model                               |
| :------- | :-------------------------- | :------------------------------------------------------------------------------------------- | :---------------------------------- |
| **Meta-AI**  | Orchestrator                | Orchestrate tasks, manage roles, and maintain shared context.                                | `gemini-2.5-pro`                    |
| **Lyra**     | Prompt Engineer             | Structure workflows and refine agent instructions for clarity and effectiveness.             | `gemini-2.5-flash`                  |
| **Aurora**   | Designer                    | Generate aesthetic layouts, color palettes, typography, and UI flows.                        | `gemini-2.5-flash-lite-preview-06-17` |
| **Kodax**    | Engineer                    | Implement designs into clean, modular, and performant code.                                  | `gemini-2.5-flash-lite-preview-06-17` |
| **TASe**     | Task-Agnostic Step Extractor | Identify and extract each 'Task Agnostic Step' (TAS) towards the high-level goal.            | `gemini-2.5-flash-lite-preview-06-17` |

## Project Structure

```
t20-multi-agent/
├── agents/                 # YAML definitions for each agent
│   ├── orchestrator.yaml
│   ├── lyra.yaml
│   └── ...
├── prompts/                # System prompts and instructions for agents
│   ├── orchestrator_instructions.txt
│   └── ...
├── runtime/                # Core Python source code for the framework
│   ├── __init__.py
│   ├── executor.py         # Main execution logic, agent classes, CLI entry point
│   └── loader.py           # Utilities for loading configs, agents, and prompts
├── sessions/               # Output directory for all runtime sessions (auto-generated)
│   └── session_.../
│       ├── initial_plan.json
│       ├── 0__step_0_Lyra_result.txt
│       └── ...
└── setup.py                # Project setup and dependencies
```

## Getting Started

### Prerequisites

-   Python 3.9+
-   Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/t20-multi-agent.git
    cd t20-multi-agent
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the package and its dependencies:**
    This command uses the `setup.py` file to install the necessary libraries and make the `t20-cli` command available.
    ```bash
    pip install -e .
    ```

4.  **Set up your environment variables:**
    Create a file named `.env` in the root of the project directory and add your Google AI API key:
    ```
    # .env
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

## Usage

The framework is operated through the `t20-cli` command. Simply provide the high-level goal you want the agent team to accomplish as a string argument.

### Example

Let's ask the team to design and build a simple webpage.

```bash
t20-cli "Design and create the HTML and CSS for a modern, minimalist landing page for a new SaaS product called 'Innovate'."
```

### What Happens Next

1.  A new session is created in the `sessions/` directory.
2.  `Meta-AI` (the Orchestrator) receives the goal and generates a plan, which is saved as `initial_plan.json`. The plan might look something like this:
    -   **Step 1 (Prompt Engineer):** Refine the system prompts for the Designer and Engineer to align with a "modern, minimalist" aesthetic.
    -   **Step 2 (Designer):** Generate a color palette, typography suggestions, and a layout description for the landing page.
    -   **Step 3 (Engineer):** Take the design specifications from the Designer and write the complete HTML and CSS code.
3.  The `Orchestrator` executes the plan step-by-step, calling the appropriate agents.
4.  All intermediate and final outputs are saved as artifacts in the session folder. You can monitor the progress by watching the console output and exploring the generated files.

After the run is complete, you can find the final HTML and CSS code generated by `Kodax` inside the `sessions/session_<uuid>/` folder.
