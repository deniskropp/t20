# T20 Workbench v2.0 - Development Plan

This plan outlines the sequence of tasks required to implement the features and architectural changes for T20 Workbench v2.0, as defined in `t20_workbench/v2_requirements.md`.

## Phase 1: Foundational Improvements & Core Runtime

**Goal:** Stabilize and enhance the core runtime and essential UI elements before tackling more complex features.

*   **T5.1: Implement Stop Workflow Functionality**
    *   **Description:** Add the ability to gracefully stop the running workflow. This involves modifying `MainWindow` to emit a stop signal, `Worker` to listen and terminate its process, and `QThread` to be properly managed.
    *   **Dependencies:** T4 (requires stop functionality)
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** Functional stop button, updated `worker.py` and `main_window.py`.

*   **T5.2: Refine Error Handling and Reporting**
    *   **Description:** Enhance error catching within the `runtime.System` and `Worker`. Improve the detail of error messages displayed in the UI and logs. Update `MainWindow` to better present detailed errors.
    *   **Dependencies:** T4 (requires granular error handling)
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** More informative error messages, updated `worker.py` and `runtime/system.py` (assuming this is where core error handling resides).

*   **T5.3: Centralize Configuration Management**
    *   **Description:** Implement a `ConfigManager` to handle loading and accessing configurations from various sources. This will be a foundational step for many future features.
    *   **Dependencies:** T4 (requires centralized config)
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** New `config_manager.py` module, updated `runtime.System` and other relevant components to use `ConfigManager`.

*   **T5.4: Enhance Modularity and Decoupling (Initial Pass)**
    *   **Description:** Review and refactor key modules (`runtime`, `worker`, `main_window`) to improve separation of concerns. Focus on reducing direct dependencies between UI and backend logic.
    *   **Dependencies:** T5.1, T5.2, T5.3 (benefits from these foundational changes)
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** Refactored code in relevant modules, improved testability.

## Phase 2: Advanced Runtime Features

**Goal:** Introduce more sophisticated runtime capabilities, including parallel execution and flexible LLM integration.

*   **T5.5: Implement Parallel Task Execution**
    *   **Description:** Modify the `runtime.System` to identify and execute independent tasks in parallel. This will likely involve integrating `QThreadPool` or similar concurrency mechanisms.
    *   **Dependencies:** T5.2, T5.3, T5.4 (requires stable runtime and config)
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** Updated `runtime/system.py` supporting parallel execution.

*   **T5.6: Flexible LLM Model and Provider Selection**
    *   **Description:** Update the `System` to support a pluggable architecture for LLM providers. Integrate UI components for selecting and configuring models/providers.
    *   **Dependencies:** T5.3 (requires config management), T4 (requires flexible LLM selection)
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** Updated LLM integration layer in `runtime`, new UI elements in `main_window.py`.

*   **T5.7: Direct Agent-to-Agent Communication**
    *   **Description:** Implement a messaging system within `runtime.System` to allow direct communication between agents.
    *   **Dependencies:** T5.2, T5.3, T5.4 (requires stable runtime and communication infrastructure)
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** Messaging/event bus implementation in `runtime/system.py`, updated agent interfaces.

## Phase 3: Enhanced UI and User Interaction

**Goal:** Improve the user interface with advanced features for plan management, artifact handling, and agent configuration.

*   **T5.8: Enhance Task Management UI**
    *   **Description:** Update the plan `QTreeView` to allow viewing detailed task info, potentially manual status updates, and rescheduling. This may involve creating new dialogs or context menus.
    *   **Dependencies:** T4 (task management UI), T5.2 (error reporting)
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** Interactive plan view, updated `main_window.py`.

*   **T5.9: Implement Agent Configuration UI**
    *   **Description:** Develop UI components for configuring individual agents (parameters, LLMs, prompts). This will dynamically generate forms based on agent schemas.
    *   **Dependencies:** T5.3 (config management), T4 (agent config UI)
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** New agent configuration dialogs/widgets in `main_window.py`.

*   **T5.10: Advanced Artifact Browsing and Previewing**
    *   **Description:** Enhance the artifact tab with preview capabilities for common file types and improved organization/search.
    *   **Dependencies:** T4 (artifact browsing)
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** Integrated preview components in `main_window.py`.

## Phase 4: Prompt Engineering & Extensibility

**Goal:** Integrate tools for prompt engineering and ensure the system is easily extensible.

*   **T5.11: Integrated Prompt Engineering Tools**
    *   **Description:** Develop a UI section for viewing, editing, testing, and managing prompt templates. Implement a "test prompt" feature.
    *   **Dependencies:** T5.3 (config management), T4 (prompt tools)
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** Prompt management UI in `main_window.py`, supporting backend logic.

*   **T5.12: Improve Extensibility (Design & Implementation)**
    *   **Description:** Apply design patterns (Strategy, Factory, Plugin) to make adding new agents, orchestrators, and LLM providers more seamless.
    *   **Dependencies:** All previous tasks, especially those involving new components (T5.6, T5.9)
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** Refactored core components, clear extension points, updated documentation.

*   **T5.13: Comprehensive Testing Strategy**
    *   **Description:** Set up a testing framework (e.g., pytest) and write unit and integration tests for new and refactored components.
    *   **Dependencies:** Requires significant portions of the codebase to be implemented.
    *   **Role:** Engineer (Kodax)
    *   **Deliverable:** Test suite (`tests/` directory), improved code quality and reliability.

## Phase 5: Finalization & Synthesis

*   **T5.14: Final Code Review and Refinement**
    *   **Description:** Conduct a thorough review of all implemented v2.0 features, addressing any remaining issues, performance bottlenecks, or UI inconsistencies.
    *   **Dependencies:** T5.1 - T5.13
    *   **Role:** Engineer (Kodax), Code Investigator (Codein)
    *   **Deliverable:** Polished codebase.

*   **T5.15: Generate Final Report**
    *   **Description:** Synthesize all findings, implemented code, and refined plans into a final report detailing the T20 Workbench v2.0 development.
    *   **Dependencies:** T5.14
    *   **Role:** Task-Agnostic Step (TAS) extractor (uTASe)
    *   **Deliverable:** Final report document.