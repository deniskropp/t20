# Updated Prompt Engineering Strategy for Python Self-Loading/Respawning Script

This document outlines the refined prompt engineering strategy for developing the Python script that loads itself and respawns services. It incorporates learnings from the development process, particularly the successful refinement of the script and the establishment of a feedback loop.

**Overall Goal:** Create a robust Python script capable of self-loading and managing the respawning of services.

**Role:** Prompt Engineer (Lyra)

**Core Principles:**
*   **Clarity and Specificity:** Prompts must be unambiguous, providing precise requirements and constraints.
*   **Iterative Refinement:** Prompts should facilitate an iterative development process, incorporating feedback and analysis at each stage.
*   **Contextual Awareness:** Prompts must provide sufficient context, including previous outputs, system architecture, and defined terminology.
*   **Task Decomposition:** Break down complex tasks into smaller, manageable steps for AI agents.
*   **Vocabulary Consistency:** Adhere to the project's defined lexicon, leveraging roles like 'Lexicographer' and 'Linguistic Mapper'.

**Strategy Evolution based on Development Outcomes:**

1.  **Enhanced Detail for Implementation Prompts (Post-T19):**
    *   **Rationale:** The successful refinement of `refined_script.py` demonstrated the need for highly specific instructions regarding complex functionalities like state management, process group handling, and concurrent operations.
    *   **Refined Approach:** Future prompts for implementation tasks (e.g., modifying the script further based on feedback) should explicitly mention:
        *   **State Management:** Specify serialization/deserialization methods (e.g., `pickle`), state file handling, and error handling during save/load operations.
        *   **Process Control:** Detail the use of `subprocess.Popen` with `preexec_fn=os.setsid`, signal handling (`SIGTERM`, `SIGKILL`), process group management (`os.killpg`), and graceful shutdown procedures.
        *   **Concurrency:** Clearly define requirements for thread/process pools (e.g., `concurrent.futures.ThreadPoolExecutor`), rate limiting, and queue management for respawning.
        *   **Error Handling & Logging:** Emphasize robust logging, including flushing mechanisms and handling errors during high-stress conditions.
    *   **Example Prompt Snippet:** `Implement a mechanism to ensure state persistence across self-respawns using pickle, saving to '{STATE_FILE}'. Handle potential exceptions during pickling and unpickling. Ensure the service manager correctly re-initializes processes based on loaded state.`

2.  **Integrating Feedback Loop Considerations (Post-T21):**
    *   **Rationale:** The establishment of a feedback loop requires agents to potentially interact with feedback data and contribute to the improvement cycle.
    *   **Refined Approach:** Prompts for agents involved in later stages (e.g., maintenance, further development) should include instructions related to:
        *   **Feedback Analysis:** Agents may be prompted to analyze logs or user feedback to identify patterns, root causes, or areas for enhancement.
        *   **Suggestion Generation:** Prompts can ask agents to propose specific code modifications or documentation updates based on analyzed feedback.
        *   **Documentation Updates:** Agents might be tasked with drafting or updating documentation sections based on script changes or new features.
    *   **Example Prompt Snippet:** `Analyze the provided error logs ({LOG_FILE}) and user feedback ({FEEDBACK_CHANNEL_SUMMARY}) to identify the top 3 most frequent issues. For each issue, propose a specific code change in the Python script to address it and draft a corresponding update for the documentation.`

3.  **Reinforcing Terminology and Workflow:**
    *   **Rationale:** Maintaining consistency is crucial for efficient collaboration, especially with AI agents.
    *   **Refined Approach:** Continue to:
        *   **Reference Defined Roles:** Clearly assign tasks to specific roles (e.g., 'Refinement Strategist', 'Improvement Analyst').
        *   **Utilize Task IDs:** Refer to previous tasks (e.g., 'T19', 'T21') to provide context.
        *   **Standardize Vocabulary:** Ensure prompts use terms consistent with the project's lexicon (e.g., 'self-loading', 'respawn', 'state management', 'process group').
        *   **Structure Prompts:** Maintain a clear structure: context, task, specific requirements, expected output format.

**Future Prompt Engineering Focus:**
*   **Automated Testing Integration:** Develop prompts that guide agents in creating or refining unit/integration tests based on script changes and identified issues.
*   **Configuration Management Prompts:** Create prompts for agents to design more sophisticated configuration loading and validation mechanisms.
*   **Security Considerations:** As the script evolves, prompts should address potential security vulnerabilities related to self-modification and external command execution.

By adhering to this updated strategy, prompt engineering efforts will continue to align with the project's evolving needs, ensuring efficient development, robust implementation, and a sustainable improvement cycle.