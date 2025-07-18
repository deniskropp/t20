import uuid
import os
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from google import genai
from google.genai import types

from runtime.loader import load_config, load_agent_templates, load_prompts

@dataclass
class Agent:
    """Represents a runtime agent instance."""
    name: str
    role: str
    goal: str
    model: str
    system_prompt: str
    instance_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    team: Optional[List['Agent']] = None

    def __post_init__(self):
        print(f"Agent instance created: {self.name} (Role: {self.role}, Model: {self.model}, ID: {self.instance_id})")

    def start_workflow(self, session: 'Session', initial_task: str):
        """Initiates a workflow based on the agent's role."""
        print(f"Workflow started by {self.name} in Session {session.session_id} for task: '{initial_task}'")
        if self.role == 'Orchestrator' and self.team:
            self.orchestrate_task(session, initial_task)
        else:
            self.execute_task(session, initial_task)

    def execute_task(self, session: 'Session', task_description: str):
        """Executes a task using the Generative AI model."""
        print(f"Agent {self.name} is executing task: {task_description}")
        session.add_artifact(f"{self.name}_task_desc.txt", task_description)
        try:
            # Initialize the GenAI client (consider moving this to a more global/reusable place)
            # Ensure GOOGLE_API_KEY environment variable is set for Gemini Developer API
            # or GOOGLE_GENAI_USE_VERTEXAI, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION for Vertex AI
            client = genai.Client()

            response = client.models.generate_content(
                model=self.model,
                contents=[task_description],
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt, # type: ignore
                    temperature=0.7, # Example: adjust creativity
                    #max_output_tokens=800, # Example: adjust response length
                ),
            )

            result = response.text
            print(f"Agent {self.name} completed task. Output: {result[:200]}...") # Print first 200 chars

        except Exception as e:
            result = f"Error executing task for {self.name}: {e}"
            print(result)

        session.add_artifact(f"{self.name}_task_result.txt", result)

    def invoke_model(self, session: 'Session', prompt: str) -> Dict[str, Any]:
        """Simulates invoking the agent's language model to get a structured plan."""
        print(f"Agent {self.name} is invoking its model to generate a plan.")
        # In a real implementation, this would be an API call to the model specified in self.model.
        # For this example, we'll return a hardcoded, structured plan based on the prompt.
        
        # Heuristic to generate a plausible plan based on the goal.
        plan = {
            "steps": [
                {"role": agent.role, "task": f"Complete sub-task for goal: {prompt}"} for agent in self.team or []
            ]
        }

        # Save the generated plan as a session artifact for inspection.
        session.add_artifact(f"{self.name}_generated_plan.json", plan)
        return plan

    def orchestrate_task(self, session: 'Session', high_level_goal: str):
        """Orchestrates a task by generating a plan and delegating to team members."""
        print(f"Orchestrator {self.name} is breaking down goal: '{high_level_goal}'")
        
        # 1. Generate a prompt to create a plan.
        team_description = "\n".join([f"- {agent.name} (Role: {agent.role})" for agent in self.team or []])
        planning_prompt = (
            f"Given the high-level goal: '{high_level_goal}', and the available team members:\n"
            f"{team_description}\n\n"
            "Create a step-by-step JSON plan to achieve this goal. Each step should specify the 'role' of the agent responsible and the 'task' description."
        )

        # 2. Invoke the model to get a structured plan.
        plan = self.invoke_model(session, planning_prompt)
        session.add_artifact("initial_plan.json", plan)

        # 3. Delegate tasks based on the generated plan.
        if "steps" in plan and self.team:
            for step in plan["steps"]:
                role_to_find = step.get("role")
                task_to_delegate = step.get("task")
                
                if not role_to_find or not task_to_delegate:
                    print(f"Warning: Skipping invalid step in plan: {step}")
                    continue

                # Find the correct agent in the team by role.
                delegate_agent = next((agent for agent in self.team if agent.role == role_to_find), None)
                
                if delegate_agent:
                    delegate_agent.execute_task(session, task_to_delegate)
                else:
                    print(f"Warning: No agent found with role '{role_to_find}' for task: '{task_to_delegate}'")
        
        print("Orchestrator has delegated all tasks. Workflow complete.")


@dataclass
class Session:
    """Manages the runtime context for a task."""
    session_id: str = field(default_factory=lambda: f"session_{uuid.uuid4()}")
    agents: List[Agent] = field(default_factory=list)
    state: str = "initialized"
    session_dir: str = field(init=False)

    def __post_init__(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.session_dir = os.path.join(project_root, 'sessions', self.session_id)
        os.makedirs(self.session_dir, exist_ok=True)
        print(f"Session created: {self.session_id} (Directory: {self.session_dir})")

    def add_artifact(self, name: str, content: Any):
        """Saves an artifact in the session directory."""
        artifact_path = os.path.join(self.session_dir, name)
        try:
            with open(artifact_path, 'w', encoding='utf-8') as f:
                if isinstance(content, (dict, list)):
                    json.dump(content, f, indent=4)
                else:
                    f.write(str(content))
            print(f"Artifact '{name}' saved in session {self.session_id}.")
        except (TypeError, IOError) as e:
            print(f"Error saving artifact '{name}': {e}")

    def get_artifact(self, name: str) -> Any:
        """Loads an artifact from the session directory."""
        artifact_path = os.path.join(self.session_dir, name)
        try:
            with open(artifact_path, 'r', encoding='utf-8') as f:
                if name.endswith('.json'):
                    return json.load(f)
                return f.read()
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            print(f"Error retrieving artifact '{name}': {e}")
            return None


def instantiate_agent(spec: Dict[str, Any], prompts: Dict[str, str], all_specs: List[Dict[str, Any]]) -> Optional[Agent]:
    """Creates an agent instance from its specification and prompt."""
    prompt_key = f"{spec['name'].lower()}_instructions.txt"
    if prompt_key not in prompts and spec.get('name') == 'Meta-AI':
        prompt_key = 'orchestrator_instructions.txt'

    if prompt_key not in prompts:
        print(f"Warning: Prompt for agent '{spec['name']}' not found. Skipping.")
        return None

    agent = Agent(
        name=spec.get('name', 'Unnamed Agent'),
        role=spec.get('role', 'Agent'),
        goal=spec.get('goal', ''),
        model=spec.get('model', 'default-model'),
        system_prompt=prompts[prompt_key]
    )

    if spec.get('delegation') and 'team' in spec:
        agent.team = []
        for team_member_name in spec['team']:
            member_spec = next((s for s in all_specs if s['name'].lower() == team_member_name.lower()), None)
            if member_spec:
                member_agent = instantiate_agent(member_spec, prompts, all_specs)
                if member_agent:
                    agent.team.append(member_agent)
            else:
                print(f"Warning: Team member '{team_member_name}' not found in agent specs.")
    return agent

def find_agent_by_role(agents: List[Agent], role: str) -> Optional[Agent]:
    """Finds an agent by its role."""
    for agent in agents:
        if agent.role == role:
            return agent
    return None

def system_runtime_bootstrap(root_dir: str, initial_task: str):
    """Initializes and starts the system runtime."""
    print("--- System Runtime Bootstrap ---")
    
    config = load_config(os.path.join(root_dir, "config/runtime.yaml"))
    agent_specs = load_agent_templates(os.path.join(root_dir, "agents/"))
    prompts = load_prompts(os.path.join(root_dir, "prompts/"))
    
    # Instantiate only the top-level agents first
    agents = []
    for spec in agent_specs:
        # Avoid instantiating team members directly; they'll be part of the orchestrator
        is_team_member = any(spec['name'].lower() in s.get('team', []) for s in agent_specs if 'team' in s)
        if not is_team_member:
            agent = instantiate_agent(spec, prompts, agent_specs)
            if agent:
                agents.append(agent)

    if not agents:
        print("Error: No agents could be instantiated. Bootstrap aborted.")
        return

    orchestrator_role = 'Orchestrator'
    orchestrator = find_agent_by_role(agents, orchestrator_role)

    if not orchestrator:
        print(f"Error: Orchestrator with role '{orchestrator_role}' not found. Bootstrap aborted.")
        return

    session = Session(agents=agents)
    
    print("\n--- Starting Workflow ---")
    orchestrator.start_workflow(session, initial_task)
    
    print("\n--- System Runtime Bootstrap Complete ---")


if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    task = "Develop a new landing page for our product."
    system_runtime_bootstrap(project_root, task)
