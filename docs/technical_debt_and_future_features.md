# Technical Debt and Future Features

This document outlines identified areas of technical debt and potential new features for the T20 multi-agent runtime system, based on the codebase analysis conducted on 2025-11-25.

## 1. Technical Debt & Refinements

-   **`runtime/agent.py` - `_run` method:** The error handling and response parsing is overly complex and brittle.
    -   **Recommendation:** Refactor to simplify the parsing logic. Potentially create a dedicated response validation and parsing class.
-   **`runtime/llm.py` - LLM Provider Abstraction:** Duplicated logic exists across concrete LLM implementations.
    -   **Recommendation:** Abstract common logic (e.g., stream handling, error logging) into the base `LLM` class or a helper.
-   **`runtime/message_bus.py` - Scalability:** The current list-based callback system is not scalable.
    -   **Recommendation:** Replace with a more robust pub/sub library or a more efficient implementation for better performance under load.
-   **`runtime/orchestrator.py` - Prompt Management:** The prompt template is hardcoded.
    -   **Recommendation:** Integrate prompt management into the centralized `System.py` loading mechanism.
-   **Error Handling:** Error handling is inconsistent across the codebase.
    -   **Recommendation:** Implement a standardized set of custom exception types.

## 2. Scalability Concerns

-   **`runtime/message_bus.py`:** As noted, the message bus is a primary bottleneck.
-   **Agent Instantiation:** Loading all agents at startup may be slow.
    -   **Recommendation:** Investigate lazy-loading or on-demand agent instantiation.
-   **`runtime/system.py` - `run` method:** `ThreadPoolExecutor` might not be optimal for CPU-bound tasks.
    -   **Recommendation:** While likely sufficient, keep `ProcessPoolExecutor` in mind as an alternative if performance becomes an issue.

## 3. Opportunities for New Features

-   **Advanced Debugging Tools:**
    -   Visual dependency graph of tasks.
    -   Step-by-step execution control (pause, step).
    -   Agent state and artifact inspection.
    -   LLM prompt/response history viewer.
-   **Advanced Agent Communication:**
    -   Implement structured communication protocols (e.g., RPC-like calls).
-   **Dynamic Agent Configuration:**
    -   Live editing and validation of agent YAML configurations.
    -   Dynamic addition/removal of agents at runtime.
-   **Scalable Artifact Storage:**
    -   Integrate with cloud storage (S3, GCS) for large artifacts.
-   **Agent Specialization:**
    -   Define clear interfaces for specialized agents (e.g., 'CodeGenerator', 'CodeReviewer').
-   **Dynamic Plan Modifiability:**
    -   Allow the plan to be modified during execution based on intermediate results.
