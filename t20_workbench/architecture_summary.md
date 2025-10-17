# T20 Workbench v1.0 Architecture Summary

## Overview

The T20 Workbench is a Python-based GUI application built with PySide6, designed to orchestrate and manage workflows involving AI agents. It provides a user interface for defining goals, managing context files, visualizing execution plans, and monitoring logs and artifacts. The core functionality is powered by a separate runtime system that handles agent interactions and task execution in a background thread to maintain GUI responsiveness.

## Core Components and Modules:

1.  **`t20_workbench/main.py` (Entry Point):**
    *   Initializes the `QApplication`.
    *   Applies the global stylesheet (`APP_STYLE` from `styles.py`).
    *   Creates and displays the main window (`MainWindow`).
    *   Starts the Qt event loop.

2.  **`t20_workbench/main_window.py` (UI Layer):
    *   **`MainWindow` Class:** The central `QMainWindow` subclass.
        *   **UI Structure:** Organizes the UI into distinct panels using `QSplitter` and layout managers (`QVBoxLayout`, `QHBoxLayout`).
            *   **Left Panel:** Goal input (`QTextEdit`), orchestrator selection (`QComboBox`), context file management (add/remove buttons, `QListView` with `QStringListModel`).
            *   **Center Panel:** Execution plan visualization (`QTreeView` with `QStandardItemModel`). Displays status, task, and agent.
            *   **Bottom Panel:** Tabbed interface (`QTabWidget`) for logs (`QPlainTextEdit`) and artifacts (`QTreeView` with `QFileSystemModel`).
        *   **Orchestrator Loading:** Dynamically scans the `agents/` directory for `.yaml` files defining 'Orchestrator' roles and populates the `QComboBox`.
        *   **Worker Thread Management:** Manages a `QThread` and a `Worker` instance for background processing.
        *   **Signal/Slot Connections:** Connects UI events (button clicks, selections) to internal slots and worker thread signals/slots for communication.
        *   **State Management:** Manages UI states (e.g., running vs. idle) and enables/disables controls accordingly.
        *   **Event Handling:** Overrides `closeEvent` to ensure graceful shutdown of the worker thread.

3.  **`t20_workbench/worker.py` (Background Processing):
    *   **`Worker` Class:** Inherits from `QObject` to enable signal/slot communication across threads.
        *   **Threaded Execution:** Runs `runtime.System` operations in a separate `QThread`.
        *   **`runtime.System` Integration:** Instantiates and interacts with the `System` class from the `runtime` module.
            *   Calls `system.setup()` with orchestrator name.
            *   Calls `system.start()` to generate the execution plan.
            *   Calls `system.run()` to execute the plan.
        *   **Logging Integration:** Uses `QtLogHandler` to capture logs from the `runtime` and emit them as `log_message` signals to the UI.
        *   **Status Updates:** Emits signals for `plan_generated`, `task_status_updated`, `workflow_finished`, and `error_occurred` to update the UI.
        *   **File Handling:** Reads context files provided by the user into `runtime.File` objects.

4.  **`t20_workbench/logging_handler.py` (Thread-Safe Logging):
    *   **`QtLogHandler` Class:** A custom `logging.Handler` that inherits from `QObject`.
        *   **Signal Emission:** Emits a `new_log_message` signal for each log record, allowing thread-safe GUI updates.
        *   **Integration:** Attached to the root logger within the `Worker` class.

5.  **`t20_workbench/styles.py` (Styling):
    *   **`APP_STYLE`:** A multi-line string containing CSS-like rules for styling `PySide6` widgets, providing a dark theme.

## Agent Interactions & Workflow:

1.  **User Input:** The user defines a high-level goal, selects an orchestrator (from `agents/*.yaml`), and optionally adds context files.
2.  **Workflow Initiation:** User clicks 'Start Workflow'.
3.  **Worker Thread Activation:** The `MainWindow` emits `start_workflow_signal` to the `Worker` instance running in `QThread`.
4.  **Runtime Setup:** The `Worker` instantiates `runtime.System`, configures it with the chosen orchestrator, and sets up the `QtLogHandler`.
5.  **Plan Generation:** `system.start()` is called with the goal and context files. This process likely involves the orchestrator agent defining a sequence of tasks.
6.  **Plan Visualization:** The generated `Plan` object is emitted via `plan_generated` signal and displayed in the `MainWindow`'s plan view.
7.  **Workflow Execution:** `system.run()` is called, which iteratively executes tasks. During execution:
    *   The `runtime` logs messages, which are captured by `QtLogHandler` and sent to the UI via `log_message` signal.
    *   Task status changes (running, success, error) are signaled via `task_status_updated`.
8.  **Completion/Error:** Upon completion, `workflow_finished` is emitted, showing artifacts and resetting the UI. On error, `error_occurred` is emitted, displaying an error message and resetting the UI.

## Key Concepts from `TOP40.md` & `runtime` (Inferred):

*   **Core Runtime (`runtime.System`):** The central orchestrator logic, responsible for setting up, planning, and running workflows. It manages sessions and interacts with agents.
*   **Agent Abstraction:** Agents likely have a common interface (`Task` objects, `Agent` classes) allowing the `System` to invoke them.
*   **Orchestration Logic:** Handled by a selected 'Orchestrator' agent, responsible for generating the `Plan`.
*   **LLM Integration Layer:** The `runtime` likely contains modules to interface with various LLMs (e.g., Mistral, as hinted by `default_model='mistral:mistral-small-latest'`).
*   **Task Management:** The `Plan` object contains a list of `Task` objects, each with an ID, description, and assigned agent.
*   **Workflow State Management:** Tracked implicitly by the `runtime.System` and visually represented in the `MainWindow`'s plan view.
*   **Artifact Handling:** The `System` manages sessions, and completed workflows emit the `session_path`, implying artifact storage within session directories.
*   **Session Management:** Each workflow run appears to create a new session.
*   **Configuration Loading:** Orchestrator definitions are loaded from YAML files.
*   **Prompt Management:** Agents likely use prompts loaded from external files (inferred from `TOP40.md`).
*   **Data Structure Definitions:** `runtime.custom_types` defines `Plan` and `Task` models.

## Potential Areas for v2.0 Development:

1.  **Enhanced UI Interactivity:**
    *   **Stop Workflow:** Implement functionality for the 'Stop Workflow' button to gracefully terminate the `QThread` and `Worker`.
    *   **Task Editing/Rescheduling:** Allow users to modify tasks in the plan or manually reschedule them.
    *   **Agent Configuration UI:** Provide a UI to configure individual agents beyond just selecting orchestrators.
    *   **Artifact Browsing:** More sophisticated artifact browsing and previewing within the UI.

2.  **Improved Runtime Capabilities:**
    *   **Agent Communication:** Implement direct agent-to-agent communication channels if not already present.
    *   **Error Handling:** More granular error handling within the `runtime.System` and better reporting in the UI.
    *   **Parallel Task Execution:** Optimize workflow execution by running independent tasks in parallel (requires careful thread/process management).
    *   **LLM Model Selection:** Allow users to select different LLM models or providers directly from the UI.
    *   **Prompt Engineering Tools:** Integrate tools for editing and testing prompts within the workbench.

3.  **Codebase Refinements:**
    *   **Modularity:** Further decouple UI, worker, and runtime components.
    *   **Configuration Management:** Centralize configuration loading for agents and the system.
    *   **Testing:** Implement unit and integration tests for the `runtime` and UI components.
    *   **Extensibility:** Design for easier addition of new agent types, orchestrators, and LLM providers.