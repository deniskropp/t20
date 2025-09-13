# T20 Multi-Agent System

🧮[[MTC|LCP](https://ai.violass.club/mtc-lcp/)](https://ai.violass.club/mtc-lcp/)
🪬[[Demo](./new-logs/session_c1f43a58-89ca-47b7-a9f4-c4a009391961)](./new-logs/session_c1f43a58-89ca-47b7-a9f4-c4a009391961)
📖[[Docs](https://ai.violass.club/t20)](https://ai.violass.club/t20)

**T20 is a sophisticated, multi-agent framework designed to tackle complex tasks through collaborative AI. It empowers you to solve complex problems by assembling a team of specialized AI agents that work together, orchestrated by a central planner.**

---

## Philosophy

The T20 system is built on the idea of **Cognitive Cadence**: a structured, iterative process where AI agents with different "cognitive roles" collaborate to build knowledge and produce results. This approach mirrors a human team, where planners, researchers, and specialists work in a coordinated fashion. Our goal is to create a system that is not only powerful but also transparent and traceable, allowing you to understand and debug the entire problem-solving process.

## How It Works

T20 employs an orchestrator-delegate model. The workflow is simple yet powerful:

1.  **Goal Definition**: You provide a high-level goal (e.g., "Create a landing page for a new app").
2.  **Dynamic Planning**: A lead `Orchestrator` agent analyzes the goal and generates a step-by-step plan.
3.  **Task Delegation**: The `Orchestrator` assigns each task to the most suitable specialist agent.
4.  **Iterative Execution**: Agents execute their tasks, building upon each other's work.
5.  **Transparent Logging**: Every step, prompt, and output is logged for full traceability.

Here is a simplified view of the process:

```
[User Goal] -> [Orchestrator] -> [Step 1: Agent A] -> [Step 2: Agent B] -> [Final Output]
                      |
                  [Plan.json]
```

## The Team

The system comes with a diverse team of pre-configured agents, each with a specific role. Agents are defined in simple YAML files in the `agents/` directory.

| Name | Role | Goal |
| :--- | :--- | :--- |
| aitutor | AI Tutor | |
| Aurora | Designer | Generate aesthetic layouts, color palettes, typography, and UI flows, ensuring accessibility and visual balance. |
| Cogito | Humorist | Humor |
| Delivero | Creative and structural content generator | Generate creative ideas, detailed outlines, and full scripts |
| Fizz La Metta | Coordinator | Meta-temporal coordination of layered cognition processing |
| GPTASe | Task-Agnostic Step (TAS) extractor | Identify and extract each 'Task Agnostic Step' (TAS) towards the high-level goal. |
| Kodax | Engineer | Implement designs into clean, modular, and performant code, focusing on responsive design and accessibility. |
| La Cogito | Orchestrator | Orchestrates the team |
| La Metta | Orchestrator | Orchestrates the generation of producer.ai prompt-based music using a team of specialized agents. |
| La Shorty | Orchestrator | Orchestrates the generation of producer.ai prompt-based music using a team of specialized agents. |
| La TASe | Orchestrator | Orchestrates the extraction of Task Agnostic Steps (TASe) |
| La Task | Orchestrator | Orchestrates the 'Sacred Cycle of Theolinguistic Processing' by assigning tasks to specialized agents, managing their execution, and ensuring the overall integrity and theological coherence of the cycle. |
| Lyra | Prompt Engineer | Structure workflows and ensure clarity in agent instructions, system prompt engineering |
| lyrics | Lyricist | Craft compelling and evocative lyrics for music. |
| Meta-AI | Orchestrator | Orchestrate task delegation, manage role assignments, and maintain a knowledge graph for shared context. |
| Music-AI | Orchestrator | Orchestrates the generation of music using a team of specialized agents. |
| Producer-AI | Orchestrator | Orchestrates the generation of producer.ai prompt-based music using a team of specialized agents. |
| Qwen3-WebDev | Web Developer | Generate web development code (HTML, CSS, JavaScript, React) based on user requests, ensuring modern design principles, responsiveness, and functionality. |
| Shorty | Video Scriptor | Creates video scripts for YouTube Shorts accompanying the higher level goal |
| sonic | Music Designer | Manage sound definition and sonic engineering for music tracks. |
| sound | Music Producer | Manage sound definition, music production, and audio engineering for music tracks. |
| stream | Distribution and Promotion Agent | Manage digital distribution, music marketing, and audience engagement for music. |
| TASe | Task-Agnostic Step (TAS) extractor | Identify and extract each 'Task Agnostic Step' (TAS) towards the high-level goal. |
| uTASe | Task-Agnostic Step (TAS) extractor | Identify and return each 'Task Agnostic Step' (TAS) towards the high-level goal. |

## Creating Your Own Agents

The T20 framework is designed to be extensible, allowing you to define and integrate your own specialized AI agents. Follow these steps to create a new agent:

1.  **Create a YAML file:** In the `agents/` directory, create a new YAML file (e.g., `my_new_agent.yaml`). The filename should be descriptive of your agent.

2.  **Define Agent Properties:** Inside the YAML file, define the following properties:
    *   `name`: A unique name for your agent (e.g., `MyNewAgent`).
    *   `role`: A brief description of the agent's role (e.g., `Data Analyst`).
    *   `goal`: The primary objective or goal of your agent (e.g., `Analyze data and generate insights.`).
    *   `model`: (Optional) The LLM model to use for this agent. If not specified, the default model will be used.
    *   `delegation`: (Optional) Set to `true` if this agent can delegate tasks to other agents (i.e., it acts as an orchestrator).
    *   `team`: (Optional) A list of agent names that this agent can delegate tasks to. This is only relevant if `delegation` is `true`.

    Example `my_new_agent.yaml`:
    ```yaml
    name: MyNewAgent
    role: Data Analyst
    goal: Analyze data and generate insights.
    model: gemini-1.5-flash-latest
    ```

3.  **Create a System Prompt (Optional):** If your agent requires specific instructions or context, create a text file in the `prompts/` directory. The filename should follow the convention `{agent_name}_instructions.txt` (e.g., `mynewagent_instructions.txt`). The content of this file will be used as the system prompt for your agent.

    Example `mynewagent_instructions.txt`:
    ```
    You are an expert data analyst. Your task is to meticulously examine provided datasets, identify key trends, anomalies, and correlations, and present your findings in a clear, concise, and actionable report. Focus on statistical significance and avoid speculative conclusions.
    ```

Once you've created the YAML file and optionally the system prompt, your new agent will be automatically loaded by the T20 system and can be included in orchestration plans.

### Prerequisites

*   Python 3.9+
*   Git

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/t20-multi-agent.git
    cd t20-multi-agent
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -e .
    ```

4.  **Set up your environment variables:**
    Create a `.env` file and add your Google AI API key:
    ```
    # .env
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

## Usage

The framework is operated through the `t20-system` command.

```txt
usage: t20-system [-h] [-p] [-r ROUNDS] [-f [FILES ...]] [-o ORCHESTRATOR] [-m MODEL] task

Run the Gemini agent runtime.

positional arguments:
  task                  The initial task for the orchestrator to perform.

options:
  -h, --help            show this help message and exit
  -p, --plan-only       Generate only the plan without executing tasks.
  -r, --rounds ROUNDS   The number of rounds to execute the workflow.
  -f, --files [FILES ...]
                        List of files to be used in the task.
  -o, --orchestrator ORCHESTRATOR
                        The name of the orchestrator to use.
  -m, --model MODEL     Default LLM.
```


### Example 1

```bash
t20-system "Design and create the HTML and CSS for a modern, minimalist landing page for a new SaaS product called 'Innovate'."
```

### Example 2

```bash
t20-system -o LaMetta "Generate a 30-second instrumental music track with a chill, lo-fi hip-hop vibe, suitable for a study playlist."
```

### Example 3

```bash
t20-system -o Qwen3-WebDev "Create a simple React component for a 'Contact Us' form with fields for name, email, and message."
```

### Example 4

```bash
t20-system -o LaMetta "Generate a 60-second instrumental music track with an uplifting, cinematic orchestral feel, suitable for a movie trailer."
```



### What Happens Next

1.  A new session directory is created under `sessions/`.
2.  The orchestrator generates a plan (`initial_plan.json`).
3.  Agents execute the plan, saving their outputs (artifacts) in the session directory.
4.  The final result of the last step is saved in the session folder, providing a valuable template for further use.

## Use Cases

T20 can be used for a wide range of tasks, including:

*   **Web Development**: Generate full front-end code for web pages.
*   **Content Creation**: Write articles, scripts, and marketing copy.
*   **Music Production**: Compose and produce music tracks.
*   **Research & Analysis**: Break down complex topics and generate reports.
*   **Prototyping**: Quickly create and iterate on new ideas.

## Project Structure

```
t20/
├── agents/                 # Agent definitions (YAML)
├── prompts/                # System prompts for agents
├── runtime/                # Core Python source code
├── sessions/               # Output directory for all runs
├── logs/                   # Debugging logs
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

### The `runtime/` directory

The `runtime/` directory contains the core logic of the T20 system. Here is a breakdown of the files in this directory:

| File | Purpose |
| :--- | :--- |
| `__init__.py` | Makes the `runtime` directory a Python package and exposes key classes. |
| `agent.py` | Defines the base `Agent` class, and functions for instantiating and finding agents. |
| `bootstrap.py` | Contains the entry point and bootstrapping logic for the multi-agent runtime system. |
| `core.py` | Defines core data structures like `ExecutionContext` and `Session` for managing the workflow state. |
| `custom_types.py` | Contains custom type definitions used across the runtime, like `Role`, `Task`, `Plan`, and `AgentOutput`. |
| `executor.py` | (empty) |
| `llm.py` | Provides an abstract base class `LLM` and concrete implementations for different LLM providers (Gemini, Ollama, etc.). |
| `loader.py` | Contains functions for loading configuration, agent templates, and prompts from files. |
| `log.py` | Sets up logging for the application, including a colored formatter for console output. |
| `orchestrator.py` | Defines the `Orchestrator` agent, which is responsible for creating and managing the plan for the multi-agent workflow. |
| `sysmain.py` | The main entry point for the runtime system, parsing command-line arguments. |
| `temp.py` | A temporary file, seems to be a copy of `sysmain.py`. |
| `util.py` | Contains utility functions, like `read_file` and `find_project_root`. |


## Contributing

We welcome contributions! Please feel free to submit a pull request or open an issue.
