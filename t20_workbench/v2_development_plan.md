# T20 Workbench v2.0 - Development Plan

This document outlines the development plan for implementing the v2.0 requirements for the T20 Workbench.

## Phase 1: Codebase Refinements and Maintainability

This phase focuses on improving the codebase's structure and maintainability, which will provide a solid foundation for the new features.

### 1.1. Centralized Configuration Management
- **Task:** Create a `ConfigManager` class to handle loading and accessing configurations from YAML files and environment variables.
- **Files to modify:** `main_window.py`, `worker.py`, and potentially a new file `config_manager.py`.

### 1.2. Enhanced Modularity and Decoupling
- **Task:** Refactor `main_window.py` and `worker.py` to ensure the UI is fully decoupled from the runtime logic. Communication should be strictly through signals and slots.
- **Files to modify:** `main_window.py`, `worker.py`.

### 1.3. Comprehensive Testing Strategy
- **Task:** Set up `pytest` for the project. Write initial unit tests for the `runtime` classes.
- **Files to create:** `tests/test_runtime.py`.

### 1.4. Improved Extensibility
- **Task:** Review the current agent and orchestrator loading mechanism. Refactor to use a plugin-style architecture.
- **Files to modify:** `runtime/agent.py`, `runtime/loader.py`.

## Phase 2: Improved Runtime Capabilities

This phase focuses on enhancing the core runtime capabilities of the T20 system.

### 2.1. Flexible LLM Model and Provider Selection
- **Task:** Implement a pluggable architecture for LLM providers. Add UI components to select and configure providers.
- **Files to modify:** `runtime/llm.py`, `main_window.py`.

### 2.2. Direct Agent-to-Agent Communication
- **Task:** Implement a message bus system within the `runtime.System` for agent-to-agent communication.
- **Files to modify:** `runtime/system.py`, `runtime/agent.py`.

### 2.3. Granular Error Handling and Reporting
- **Task:** Refine exception handling in the `runtime.System` and agents. Display detailed error information in the UI.
- **Files to modify:** `runtime/system.py`, `main_window.py`, `worker.py`.

### 2.4. Parallel Task Execution
- **Task:** Implement a task scheduler in `runtime.System` to run independent tasks concurrently.
- **Files to modify:** `runtime/system.py`, `runtime/executor.py`.

### 2.5. Integrated Prompt Engineering Tools
- **Task:** Create a UI section for viewing, editing, and testing prompt templates.
- **Files to create:** `prompt_editor.py`.
- **Files to modify:** `main_window.py`.

## Phase 3: Enhanced UI Interactivity and User Experience

This phase focuses on improving the user interface and experience.

### 3.1. Stop Workflow Functionality
- **Task:** Implement a mechanism to gracefully stop the running workflow from the UI.
- **Files to modify:** `main_window.py`, `worker.py`.

### 3.2. Task Management and Rescheduling
- **Task:** Enhance the plan view to allow users to interact with tasks (view details, mark as complete, reschedule).
- **Files to modify:** `main_window.py`.

### 3.3. Agent Configuration UI
- **Task:** Create a UI for configuring agent parameters.
- **Files to create:** `agent_config_dialog.py`.
- **Files to modify:** `main_window.py`.

### 3.4. Advanced Artifact Browsing and Previewing
- **Task:** Enhance the artifact tab to preview files directly in the workbench.
- **Files to modify:** `main_window.py`.
