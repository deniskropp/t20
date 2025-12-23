# t20sdk API Reference

The `t20sdk` is a Python-based framework for building and orchestrating multi-agent systems. It provides the core primitives for defining agents, managing execution state, and handling inter-agent communication.

## Core System

### `t20sdk.core.system.System`

The central entry point for the multi-agent runtime. It manages the lifecycle of the application, including configuration loading, agent instantiation, and workflow execution.

**Constructor:**
```python
System(root_dir: str, default_model: str = "gemini-2.5-flash-lite")
```
-   `root_dir`: The absolute path to the project root.
-   `default_model`: The default LLM model identifier to be used by agents if not specified in their config.

**Methods:**

-   `setup(orchestrator_name: Optional[str] = None) -> None`:
    Initializes the system by loading the runtime configuration, agent templates, and prompts. It instantiates all agents and establishes the `Session`.
    -   Raises `RuntimeError` if setup fails (e.g., no agents found).

-   `start(high_level_goal: str, files: List[File] = [], plan: Plan = None) -> Plan`:
    Initiates the main workflow. If no plan is provided, it triggers the Orchestrator to generate one based on the `high_level_goal`.
    -   Returns the generated or validated `Plan`.

-   `run(plan: Plan, rounds: int = 1, files: List[File] = []) -> AsyncGenerator[Tuple[Task, Optional[str]], None]`:
    Executes the workflow defined in the `Plan`. It yields `(Task, Result)` tuples as tasks complete.
    -   Handles task dependency resolution and parallel execution where possible.

### `t20sdk.core.system.SystemConfig`

A Pydantic model defining global configuration settings.

-   `logging_level` (str): default "INFO".
-   `default_model` (str): default "gemini-2.5-flash-lite".

---

## Agents & Orchestration

### `t20sdk.core.agent.Agent`

The base class for all agents in the system.

**Attributes:**
-   `profile` (`AgentProfile`): Identity (name, role, goal) of the agent.
-   `model` (str): The LLM model used by this agent.
-   `system_prompt` (str): The system instructions governing the agent's behavior.

**Methods:**

-   `execute_task(context: ExecutionContext, task: Task) -> Optional[str]`:
    Performs a specific task by constructing a prompt with context (goal, other agents, previous artifacts) and querying the LLM.
    -   Returns the raw output string or error message.

-   `update_system_prompt(new_prompt: str) -> None`:
    Dynamically updates the agent's system instructions.

-   `subscribe(topic: str, callback: Any) -> None` / `publish(topic: str, message: Any) -> None`:
    Interface to the internal `MessageBus` for event-driven behavior.

### `t20sdk.core.orchestrator.Orchestrator`

A specialized `Agent` responsible for planning.

**Methods:**

-   `generate_plan(session: Session, high_level_goal: str, files: List[File] = []) -> Optional[Plan]`:
    Constructs a detailed execution plan to achieve the high-level goal. It uses a specialized prompt to decompose the goal into dependencies and tasks assigned to specific roles.

### `t20sdk.core.custom_types.AgentProfile`

Defines an agent's identity.
-   `name` (str): Unique name (e.g., "Coder").
-   `role` (str): Functional role (e.g., "Developer").
-   `goal` (str): The agent's primary objective.

---

## Runtime & State

### `t20sdk.core.core.Session`

Manages the persistent state of a single execution run.

-   `session_id` (str): Unique identifier for the session.
-   `session_dir` (str): Directory where session artifacts are stored.

**Methods:**

-   `add_artifact(name: str, content: Any) -> None`:
    Persists data (text or JSON) to the session directory.
-   `get_artifact(name: str) -> Any`:
    Retrieves stored artifact content.

### `t20sdk.core.core.ExecutionContext`

Holds the transient state during workflow execution, passing data between the `System` and `Agents`.

-   `plan` (`Plan`): The active plan.
-   `record_artifact(key: str, value: Any, step: Task, mem: bool = False)`:
    Records an output from a step. If `mem` is True, keeps it in memory for subsequent steps to use as context.

---

## Data Models (Types)

Defined in `t20sdk.core.custom_types`.

### `Plan`
The blueprint for execution.
-   `high_level_goal` (str): The objective.
-   `reasoning` (str): Explanation of the strategy.
-   `tasks` (List[`Task`]): Ordered list of steps.
-   `team` (`Team`): Optional team configuration updates.

### `Task`
A single unit of work.
-   `id` (str): Unique ID (e.g., "T-1").
-   `description` (str): Implementation instructions.
-   `role` (str) / `agent` (str): Assignee.
-   `deps` (List[str]): Task IDs that must complete before this one starts.

### `AgentOutput`
The structured response expected from an LLM agent.
-   `output` (str): Conversational or summary response.
-   `artifact` (`Artifact`): Contains any generated `files`.
-   `reasoning` (str): Chain-of-thought explanation.

### `Artifact` & `File`
-   `Artifact`: Wrapper for bundling multiple `File` objects from a task.
-   `File`: simple `path` and `content` pair.

---

## Messaging

### `t20sdk.core.message_bus.MessageBus`
A simple in-memory pub/sub system for agent communication.

### `t20sdk.core.message_bus.SpaceMessage`
A standardized message format for the ⫻Space protocol.
Format: `⫻{name}/{type}:{place}/{index}\n{content}`
