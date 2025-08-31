# Chapter 3: Getting Started with T20

This chapter provides a comprehensive guide for users to get started with the T20 Multi-Agent System. It covers the necessary prerequisites, guides through the installation process, details environment setup, and walks the user through their first execution of the T20 CLI. The aim is to make the initial setup and usage as smooth and straightforward as possible, enabling users to quickly leverage the system's capabilities.

## 3.1 Prerequisites

Before you begin installing and using the T20 system, ensure you have the following prerequisites in place:

*   **Python:** Version 3.9 or higher is required. You can check your Python version by running `python --version` or `python3 --version` in your terminal.
*   **Git:** Essential for cloning the T20 repository from its source. If you don't have Git installed, you can download it from [git-scm.com](https://git-scm.com/).

While not strictly required, having a basic understanding of command-line interfaces (CLI) and virtual environments will be beneficial.

## 3.2 Installation Guide

Follow these steps to install the T20 Multi-Agent System:

1.  **Clone the repository:**
    Navigate to the directory where you want to store the project and clone the repository using Git:
    ```bash
    git clone https://github.com/your-username/t20-multi-agent.git
    cd t20-multi-agent
    ```
    *Replace `https://github.com/your-username/t20-multi-agent.git` with the actual repository URL if it differs.*

2.  **Create and activate a virtual environment (Recommended):**
    Using a virtual environment helps manage project dependencies and avoids conflicts with other Python projects.
    *   **Create:**
        ```bash
        python -m venv venv
        ```
    *   **Activate:**
        *   On macOS and Linux:
            ```bash
            source venv/bin/activate
            ```
        *   On Windows:
            ```bash
            venv\Scripts\activate
            ```
    Your terminal prompt should change to indicate that the virtual environment is active (e.g., `(venv) your-prompt$`).

3.  **Install the package and its dependencies:**
    The T20 system is installed as an editable package using its `setup.py` file. This command installs the package and makes the `t20-cli` command available in your activated environment.
    ```bash
    pip install -e .
    ```

## 3.3 Environment Setup

To utilize the T20 system, you need to provide your Google AI API key. This key is used by the agents to access the Google Gemini models.

1.  **Create a `.env` file:**
    In the root directory of the cloned `t20-multi-agent` project (the same directory where `setup.py` is located), create a new file named `.env`.

2.  **Add your API Key:**
    Open the `.env` file in a text editor and add your Google AI API key in the following format:
    ```dotenv
    # .env
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
    *Replace `YOUR_API_KEY_HERE` with your actual API key obtained from Google AI Studio or a similar service.*

3.  **Verify Installation (Optional but Recommended):**
    After installation and setting up the `.env` file, you can perform a quick check to ensure the CLI command is accessible:
    ```bash
    t20-cli --help
    ```
    If the command is found and displays help information, your installation is likely successful.

## 3.4 Your First T20 Run

Now that the T20 system is installed and configured, let's run a simple example to see it in action. We'll use the command-line interface (`t20-cli`) to ask the system to design and create a basic webpage.

Execute the following command in your terminal from the root directory of the project:

```bash
t20-cli "Design and create the HTML and CSS for a modern, minimalist landing page for a new SaaS product called 'Innovate'."
```

**What happens during this run:**

1.  **Session Creation:** The T20 system automatically creates a new session directory within the `sessions/` folder (e.g., `sessions/session_abc123...`). This directory isolates the run's artifacts and logs.
2.  **Goal Processing:** The `Meta-AI` (Orchestrator) agent receives your high-level goal.
3.  **Dynamic Plan Generation:** `Meta-AI` consults an LLM (like `gemini-2.5-pro`) to generate a step-by-step execution plan in JSON format. This plan outlines the tasks and the agents responsible for them. The plan is saved as `initial_plan.json` in the session directory.
4.  **Task Delegation and Execution:** The Orchestrator proceeds through the plan, delegating tasks. For instance:
    *   `Lyra` might refine prompts for the design and coding agents.
    *   `Aurora` (Designer) might generate design specifications (color palette, layout).
    *   `Kodax` (Engineer) might then use these specifications to write the HTML and CSS code.
5.  **Artifact Saving:** The output of each agent's task (e.g., design descriptions, code snippets) is saved as an artifact within the session directory.

**Monitoring Progress:**
You can follow the execution progress through the console output. After the run completes, you will find the final generated HTML and CSS code (and all intermediate artifacts) within the specific session folder.

This first run demonstrates the core T20 workflow: receiving a goal, dynamically planning, delegating to specialized agents, and producing output artifacts, all while maintaining a traceable session log.