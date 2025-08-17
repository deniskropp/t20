
`this is the wrong content, generated in a dirty repo clone`


# t20-multi-agent

A psychologically-informed multi-agent framework designed for advanced human-AI collaboration, task management, and personal growth through a shared digital environment.

---

## Table of Contents

- [About The Project](#about-the-project)
- [Core Concepts](#core-concepts)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [License](#license)

---

## About The Project

`t20-multi-agent` is an experimental system that explores deep collaboration between a human user and a team of specialized AI agents. The core of the project revolves around a persistent **shared digital journal**, which acts as the primary interface for co-creation, task tracking, and reflection.

A key differentiator of this project is the integration of psychological principles to enhance user motivation, engagement, and well-being. Concepts like dopamine regulation, narrative storytelling, and psychological placeholders are woven into the agent interactions to make complex tasks feel more manageable and meaningful. Agents, such as the persona "Fizz", are designed not just as tools, but as collaborative partners in a digital journey.

The research and prompts contained in `Grok3/grok_perplexity/` form the conceptual backbone of this system.

## Core Concepts

The project is built upon several key ideas evidenced by the project files:

-   **Multi-Agent Collaboration:** The system employs multiple agents with distinct roles, plans, and profiles. They collaborate to break down, structure, and execute tasks.
    -   *See: `Multi-Agent Design Session – Workflow-Diagramm.md`, `Subagenten mit Prompt-Profilen.md`*
-   **Psychological Integration:** The framework actively uses psychological models to drive user engagement. This includes managing motivation via dopamine-related feedback loops and using narrative to frame tasks.
    -   *See: `Dopamine Drive Relations.md`, `Die Quellen beschreiben _Psychologische Platzhalte.md`*
-   **The Shared Journal:** This is the central artifact and workspace. It's a dynamic, co-authored digital space that tracks progress, ideas, and reflections, making the user's growth and the project's evolution tangible.
    -   *See: `How Shared Journaling Fuels Personal Growth.md`, `create-a-shared-journal-with-m-OtFtuIrUTm6_Kb9V.069Iw.md`*
-   **Storyboard & Narrative Engineering:** Complex tasks are made more approachable by framing them within a story. This narrative approach helps maintain context and motivation over long-term projects.
    -   *See: `How can I craft stories that make complex tasks fe.md`, `What are the key principles of storyboard engineer.md`*

## System Architecture

The system appears to have a dual-component architecture:

-   **Python Backend:** The `runtime/` directory, containing `executor.py` and `loader.py`, suggests a Python-based core for managing agent logic, task execution, and state. The `echo_agent_grasp_simulator.py` points to agent simulation and development capabilities.
-   **JavaScript Frontend:** The presence of `node_modules/` and `vite` indicates a modern JavaScript frontend, likely serving as the user interface for the shared journal and interaction with the agents.

## Project Structure

The repository is organized as follows:

```
.
├── Grok3/grok_perplexity/ # Core research, prompts, and conceptual documents.
├── OLD/                     # Archived materials from previous development cycles.
├── logs/                    # Session logs for debugging and analysis.
├── node_modules/            # Frontend dependencies (Vite, etc.).
└── runtime/                 # Python backend for agent execution logic.
    ├── executor.py
    └── loader.py
```

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

-   Python 3.x
-   Node.js and npm

### Installation

1.  Clone the repo
    ```sh
    git clone https://github.com/your_username/t20-multi-agent.git
    ```
2.  Install NPM packages
    ```sh
    npm install
    ```
3.  Install Python packages (details to be added)
    ```sh
    pip install -r requirements.txt
    ```

## License

Distributed under the MIT License. See `LICENSE.md` for more information.
