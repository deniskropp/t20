# API Reference

## `runtime.agent.Agent` Class

*   **`__init__(self, name: str, role: str, goal: str, model: str, system_prompt: str)`:** Initializes an Agent instance.
*   **`update_system_prompt(self, new_prompt: str)`:** Updates the agent's system prompt.
*   **`execute_task(self, context: ExecutionContext) -> Optional[str]`:** Executes a task based on the provided context.
*   **`_run(self, context: ExecutionContext, prompt: str) -> Optional[str]`:** Internal method to run the LLM and process its response.

## `runtime.core.Session` Class

*   **`__init__(self, session_id: str = ..., agents: list = ..., state: str = ..., session_dir: str = ..., project_root: str = ...)`:** Initializes a Session.
*   **`add_artifact(self, name: str, content: Any)`:** Saves an artifact to the session directory.
*   **`get_artifact(self, name: str) -> Any`:** Loads an artifact from the session directory.

## `runtime.core.ExecutionContext` Class

*   **`__init__(self, session: Session, plan: Plan, step_index: int = 0, round_num: int = 0, items: Dict[str, ContextItem] = field(default_factory=dict))`:** Initializes an ExecutionContext.
*   **`next(self)`:** Moves to the next step in the plan.
*   **`reset(self)`:** Resets the step index to 0.
*   **`current_step(self) -> Task`:** Returns the current task.
*   **`record_artifact(self, key: str, value: Any, mem: bool = False)`:** Records an artifact.
*   **`record_initial(self, key: str, value: Any)`:** Records an initial artifact.

## `runtime.orchestrator.Orchestrator` Class

*   **`generate_plan(self, session: Session, high_level_goal: str, files: List[File] = []) -> Optional[Plan]`:** Generates a workflow plan.

## `runtime.system.System` Class

*   **`setup(self, orchestrator_name: Optional[str] = None)`:** Sets up the system, loading config and agents.
*   **`start(self, high_level_goal: str, files: List[File] = []) -> Plan`:** Starts the workflow by generating a plan.
*   **`run(self, plan: Plan, rounds: int = 1, files: List[File] = [])`:** Executes the workflow for a specified number of rounds.
