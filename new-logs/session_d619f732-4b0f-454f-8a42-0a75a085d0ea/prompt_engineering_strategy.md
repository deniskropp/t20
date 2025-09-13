## Prompt Engineering Strategy for Python Service Orchestrator

**Overall Goal:** Develop a Python script that can load itself and respawn services.

**Role:** Prompt Engineer (Lyra)

**Sub-Task:** Define the prompt engineering strategy for guiding the development of the Python script, focusing on clarity and effectiveness for AI agents.

**Input:** Detailed Implementation Plan (from T6 - Workflow Designer)

**Strategy Overview:**

This strategy aims to provide clear, concise, and effective prompts for AI agents involved in developing the Python Service Orchestrator. It emphasizes breaking down complex tasks into manageable steps, specifying required inputs, defining expected outputs, and setting constraints. The strategy will be iterative, allowing for refinement as the project progresses.

**Core Principles:**

1.  **Clarity and Specificity:** Prompts must be unambiguous, leaving no room for misinterpretation. Use precise language and avoid jargon where possible, or define it clearly.
2.  **Contextual Relevance:** Each prompt should provide sufficient context, referencing previous decisions, design documents, or requirements.
3.  **Actionability:** Prompts should clearly state the desired action or outcome.
4.  **Modularity:** Break down complex tasks into smaller, well-defined sub-tasks, each addressed by a specific prompt.
5.  **Iterative Refinement:** The prompts and this strategy will be reviewed and updated based on agent performance and project evolution.

**Prompt Structure Template:**

```
[Agent Persona/Role]
**Goal:** [Specific, concise goal for this prompt]
**Context:** [Relevant background information, e.g., links to design docs, previous task outputs]
**Input:** [Specific files, data, or information the agent should use]
**Task:** [Detailed, step-by-step instructions for the agent]
**Constraints:** [Limitations, e.g., Python version, allowed libraries, performance requirements, security considerations]
**Output Format:** [Expected structure and content of the agent's response, e.g., code, documentation, report, JSON]
**Evaluation Criteria:** [How the output will be assessed for correctness and completeness]
```

**Phased Prompt Application:**

**Phase 1: Design & Planning (Completed/In Progress)**

*   **Focus:** Defining requirements, architecture, and implementation plan.
*   **Example Prompt (Conceptual):**
    ```
    System Architect
    **Goal:** Propose a high-level system architecture for the Python script.
    **Context:** Based on requirements (T1) and research (T2).
    **Input:** T1 output (Requirements), T2 output (Research findings).
    **Task:** Outline key modules, their responsibilities, and interactions. Consider modularity, scalability, and maintainability.
    **Constraints:** Must support self-loading and service respawning.
    **Output Format:** Markdown document detailing the architecture.
    ```

**Phase 2: Implementation**

*   **Focus:** Writing, integrating, and testing code modules.
*   **Prompt Strategy:** Generate prompts for specific modules or functionalities defined in the implementation plan (T6). Each prompt will target a specific agent (e.g., Python Developer Agent).
*   **Example Prompt (for `service_manager.py`):**
    ```
    Python Developer Agent
    **Goal:** Implement the `service_manager.py` module.
    **Context:** Refer to the Detailed Implementation Plan (T6), specifically Section 1 (Module Breakdown) and Section 2 (Data Structures) for `service_manager.py`. The module should manage individual service processes using `subprocess.Popen`.
    **Input:** `implementation_plan.md`.
    **Task:** 
    1. Implement the `ServiceManager` class.
    2. Implement `start_service(service_config)`: Launch service via `subprocess.Popen`, capture Popen object, update state registry. Handle `working_dir`, `environment`.
    3. Implement `stop_service(service_name)`: Send SIGTERM, wait for `timeout_stop`.
    4. Implement `restart_service(service_name)`: Calls stop then start.
    5. Implement `get_service_status(service_name)`: Use `Popen.poll()`.
    6. Implement internal state registry to track Popen objects and status.
    **Constraints:** 
    *   Use standard Python libraries (`subprocess`, `os`, `signal`).
    *   Handle potential exceptions during process management.
    *   Adhere to the data structures defined in the plan.
    **Output Format:** Python code for `service_manager.py`.
    **Evaluation Criteria:** Code is functional, includes error handling, follows the implementation plan, and passes basic unit tests.
    ```

**Phase 3: Testing & Refinement**

*   **Focus:** Quality assurance, bug fixing, performance optimization.
*   **Prompt Strategy:** Generate prompts for QA agents and refinement specialists. Prompts will focus on test case generation, execution, bug analysis, and implementing improvements.
*   **Example Prompt (for QA Specialist):**
    ```
    Quality Assurance Specialist Agent
    **Goal:** Develop and execute a test plan for the `service_manager.py` module.
    **Context:** Based on the implementation of `service_manager.py` (from Phase 2) and the overall project goals.
    **Input:** Implemented `service_manager.py` code.
    **Task:** 
    1.  Write unit tests covering `start_service`, `stop_service`, `restart_service`, and `get_service_status` under various conditions (success, failure, timeouts).
    2.  Write integration tests to verify interaction with `config_manager` and `monitor` (once implemented).
    3.  Execute all tests and report results, including any failures or unexpected behavior.
    **Constraints:** Tests should be written using a standard Python testing framework (e.g., `unittest`, `pytest`).
    **Output Format:** Test suite code (e.g., `test_service_manager.py`) and a test execution report.
    **Evaluation Criteria:** Test coverage is adequate, tests correctly identify expected and actual behavior, and the report is clear.
    ```

**Phase 4: Documentation & Deployment**

*   **Focus:** Creating user guides, API documentation, and deployment instructions.
*   **Prompt Strategy:** Generate prompts for documentation specialists, ensuring all aspects of the script are clearly explained.

**Vocabulary and Terminology:**

*   **Orchestrator:** The main Python script itself.
*   **Service:** An individual process managed by the Orchestrator.
*   **Self-Loading:** The script's ability to dynamically load or reload its own code/modules.
*   **Respawning:** The process of restarting a terminated service based on its policy.
*   **Service Configuration:** The external definition (e.g., JSON file) specifying how a service should be run and managed.
*   **State Registry:** Internal data structure tracking the status and process information of managed services.
*   **Restart Policy:** Rules defining when and how a service should be respawned.

**Feedback and Iteration:**

*   Monitor the performance of AI agents when executing prompts based on this strategy.
*   Collect feedback on prompt clarity, completeness, and effectiveness.
*   Refine prompts and this strategy document (T22) regularly based on feedback and project evolution.
