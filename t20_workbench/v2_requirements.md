# T20 Workbench v2.0 - Core Requirements and Architectural Changes

## 1. Enhanced UI Interactivity and User Experience

### 1.1. Stop Workflow Functionality
*   **Requirement:** Implement a robust mechanism to gracefully stop the currently running workflow. This involves terminating the worker thread and cleaning up resources without corrupting the session state.
*   **Architectural Change:** Introduce a `stop_workflow` signal in `MainWindow` connected to a slot that signals the `Worker` to stop. The `Worker` needs to periodically check a stop flag and exit its execution loop. The `QThread` should be properly terminated using `quit()` and `wait()`.

### 1.2. Task Management and Rescheduling
*   **Requirement:** Allow users to interact with tasks in the execution plan: view detailed task information, manually mark tasks as complete, reschedule tasks, or even add new ad-hoc tasks.
*   **Architectural Change:** Enhance the `Plan` and `Task` data structures to include more metadata (e.g., detailed error messages, execution time, dependencies). Modify the `QTreeView` for the plan to support editing and context menus. The `Worker` and `System` need to accommodate dynamic plan modifications during runtime.

### 1.3. Agent Configuration UI
*   **Requirement:** Provide an integrated UI for configuring individual agents, including their specific parameters, LLM model choices, and prompt templates, beyond just selecting an orchestrator.
*   **Architectural Change:** Develop new UI components (e.g., dialogs, property editors) that can dynamically generate forms based on agent configuration schemas (likely defined in their YAML files). The `System` class will need to manage and pass these configurations during agent instantiation.

### 1.4. Advanced Artifact Browsing and Previewing
*   **Requirement:** Enhance the artifact tab to allow users to preview common file types (text, code, images, potentially simple data formats) directly within the workbench, and offer better organization and search capabilities.
*   **Architectural Change:** Integrate lightweight preview components into the artifact `QTreeView` or a dedicated preview pane. The `System` or `Worker` might need to cache or index artifacts for faster access and searching.

## 2. Improved Runtime Capabilities

### 2.1. Direct Agent-to-Agent Communication
*   **Requirement:** Enable agents to communicate directly with each other during workflow execution, facilitating more complex interactions and collaborative problem-solving.
*   **Architectural Change:** Introduce a messaging or event bus system within the `runtime.System`. Agents would need methods to send and receive messages, and the `System` would route these messages based on agent IDs or topics.

### 2.2. Granular Error Handling and Reporting
*   **Requirement:** Improve the system's ability to catch, report, and potentially recover from errors at a granular task level. Provide detailed error information in logs and the UI.
*   **Architectural Change:** Refine exception handling within the `runtime.System` and individual agent execution logic. Introduce specific error types and codes. The `Worker` and `MainWindow` need to display this detailed error information effectively.

### 2.3. Parallel Task Execution
*   **Requirement:** Optimize workflow execution by running independent tasks concurrently, significantly reducing overall execution time.
*   **Architectural Change:** The `runtime.System` needs a sophisticated task scheduler capable of identifying and managing parallel task execution. This likely involves using `QThreadPool` or Python's `concurrent.futures` for managing multiple threads or processes, alongside careful synchronization mechanisms.

### 2.4. Flexible LLM Model and Provider Selection
*   **Requirement:** Allow users to select different LLM models and providers (e.g., Ollama, Gemini, OpenAI) directly from the UI, with the ability to configure API keys and endpoints.
*   **Architectural Change:** Enhance the `System`'s LLM integration layer to support a pluggable architecture for different providers. The UI will need components to manage these provider configurations. The `default_model` parameter in `System` initialization should be dynamically configurable.

### 2.5. Integrated Prompt Engineering Tools
*   **Requirement:** Provide tools within the workbench for users to view, edit, test, and manage prompt templates used by agents.
*   **Architectural Change:** Develop a dedicated UI section for prompt management. This could include a text editor with syntax highlighting, a 'test prompt' button that invokes an LLM with sample inputs, and functionality to save/load prompt templates associated with specific agents or tasks.

## 3. Codebase Refinements and Maintainability

### 3.1. Enhanced Modularity and Decoupling
*   **Requirement:** Further separate concerns between the UI (`main_window.py`), background processing (`worker.py`), and the core runtime logic (`runtime/`).
*   **Architectural Change:** Review dependencies and communication patterns. Ensure UI updates are strictly handled via signals/slots and background tasks do not directly manipulate UI elements. Refactor `runtime.System` to be more self-contained and testable.

### 3.2. Centralized Configuration Management
*   **Requirement:** Consolidate and standardize how configurations (for agents, LLMs, system settings) are loaded and accessed throughout the application.
*   **Architectural Change:** Implement a dedicated `ConfigManager` class or module that handles loading from various sources (YAML, environment variables, etc.) and provides a unified interface for accessing configuration values.

### 3.3. Comprehensive Testing Strategy
*   **Requirement:** Establish a robust suite of unit, integration, and potentially end-to-end tests for both the runtime and UI components.
*   **Architectural Change:** Introduce a testing framework (e.g., pytest). Write unit tests for core `runtime` classes and agent logic. Develop integration tests for key workflows. Consider UI testing frameworks or strategies.

### 3.4. Improved Extensibility
*   **Requirement:** Design the system to facilitate the easy addition of new agent types, orchestrators, LLM providers, and custom task handlers.
*   **Architectural Change:** Employ design patterns like Strategy, Factory, and Plugin architectures. Ensure interfaces and abstract base classes are well-defined for new components to hook into the existing system.
