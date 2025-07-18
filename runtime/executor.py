import uuid
import os
import json
import argparse
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from google import genai
from google.genai import types
from dotenv import load_dotenv

from runtime.loader import load_config, load_agent_templates, load_prompts

load_dotenv()

@dataclass
class ExecutionContext:
    """Holds the state and context for a multi-agent workflow."""
    session: 'Session'
    high_level_goal: str
    plan: Dict[str, Any]
    step_index: int = 0
    artifacts: Dict[str, Any] = field(default_factory=dict)

    def current_step(self):
        """Returns the current step in the plan."""
        return self.plan.get("steps", [])[self.step_index]

    def record_artifact(self, key: str, value: Any, mem: bool = False):
        """Records an artifact from a step's execution."""
        if mem:
            self.artifacts[f"step_{self.step_index}_{key}"] = value
        self.session.add_artifact(f"step_{self.step_index}_{key}", value)

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
    client: Optional[genai.Client] = field(init=False, default=None)

    def __post_init__(self):
        """Initializes the agent after it has been created."""
        print(f"Agent instance created: {self.name} (Role: {self.role}, Model: {self.model}, ID: {self.instance_id})")
        try:
            self.client = genai.Client()
        except Exception as e:
            print(f"Error initializing GenAI client for {self.name}: {e}")

    def update_system_prompt(self, new_prompt: str):
        """Updates the agent's system prompt."""
        print(f"Agent {self.name}'s system prompt updated.")
        self.system_prompt = new_prompt

    def execute_task(self, context: ExecutionContext) -> Optional[str]:
        """Executes a task using the Generative AI model."""
        step = context.current_step()
        task_description = step.get("task", "No task description provided.")
        print(f"Agent {self.name} is executing task: {task_description}")

        context.record_artifact(f"{self.name}_prompt.txt", self.system_prompt)

        if not self.client:
            result = f"Error: GenAI client not initialized for {self.name}."
            print(result)
            context.record_artifact(f"{self.name}_error.txt", result)
            return result

        task_prompt: List[str] = [
            f"The overall goal is: '{context.high_level_goal}'",
            f"Your role's specific goal is: '{self.goal}'\n"
            f"Your specific sub-task is: '{task_description}'",
        ]

        previous_artifacts = "\n\n---\n\n".join(
            f"Artifact from {key}:\n{value}"
            for key, value in context.artifacts.items()
        )
        if previous_artifacts:
            task_prompt.append(f"Please use the following outputs from the other agents as your input:\n\n{previous_artifacts}\n\n")

        task_prompt.append(
            f"Please execute your sub-task, keeping the overall goal and your role's specific goal in mind to ensure your output is relevant to the project."
        )


        context.record_artifact(f"{self.name}_task.txt", "\n\n".join(task_prompt))

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=task_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.7,
                    response_mime_type='application/json' #if self.role == 'Prompt Engineer' else None
                ),
            )
            result = response.text or ''
            print(f"Agent {self.name} completed task. Output: {result[:200]}...")
        except Exception as e:
            result = f"Error executing task for {self.name}: {e}"
            print(result)

        return result

class Orchestrator(Agent):
    """An agent responsible for creating and managing a plan."""

    def start_workflow(self, session: 'Session', initial_task: str):
        """Initiates and manages the entire workflow."""
        print(f"Orchestrator {self.name} is starting workflow for goal: '{initial_task}'")

        plan = self._generate_plan(session, initial_task)
        if not plan or "steps" not in plan:
            print("Orchestration failed: Could not generate a valid plan.")
            return

        context = ExecutionContext(session=session, high_level_goal=initial_task, plan=plan)
        team_by_role = {agent.role: agent for agent in self.team} if self.team else {}

        while context.step_index < len(plan["steps"]):
            step = context.current_step()
            role = step.get("role")
            delegate_agent = team_by_role.get(role)

            if not delegate_agent:
                print(f"Warning: No agent found with role '{role}'. Skipping step {context.step_index}.")
                context.step_index += 1
                continue

            if delegate_agent.role == 'Prompt Engineer':
                print(f"Orchestrator detected special role: {delegate_agent.role}. Preparing inputs.")

            result = delegate_agent.execute_task(context)
            if result:
                context.record_artifact(f"{delegate_agent.name}_result.txt", result, True)
                if delegate_agent.role == 'Prompt Engineer':
                    try:
                        response = json.loads(result)
                        self._check_new_prompts(session, response)
                        for key, value in response.items() if isinstance(response, dict) else []:
                            if key == "refined_prompts" or key == "initial_prompts":
                                if "target_agent_name" in value:
                                    self._check_new_prompts(session, value)
                                else:
                                    self._check_new_prompts(session, list(value))
                    except json.JSONDecodeError:
                        print("Prompt Engineer's output was not a valid JSON for prompt update.")

            context.step_index += 1

        print("Orchestrator has completed the workflow.")

    def _check_new_prompts(self, session: 'Session', obj: dict | list):
        if isinstance(obj, dict):
            self._check_new_prompt(session, obj)
        else:
            for o in obj:
                self._check_new_prompt(session, o)

    def _check_new_prompt(self, session: 'Session', obj: dict):
        if "target_agent_name" in obj and "new_system_prompt" in obj:
            target_agent_name = obj.get("target_agent_name")
            new_system_prompt = obj.get("new_system_prompt")

            if target_agent_name and new_system_prompt:
                target_agent = next((a for a in self.team or () if a.name == target_agent_name), None)
                if not target_agent:
                    target_agent = next((a for a in session.agents if a.name == target_agent_name), None)

                if target_agent:
                    target_agent.update_system_prompt(new_system_prompt)
                else:
                    print(f"Warning: Target agent '{target_agent_name}' not found for prompt update.")
            #else:
            #    print("Prompt Engineer's output did not contain valid prompt update data.")

    def _generate_plan(self, session: 'Session', high_level_goal: str) -> Dict[str, Any]:
        """Invokes the language model to get a structured plan."""
        print(f"Orchestrator {self.name} is generating a plan for: '{high_level_goal}'")
        if not self.client or not self.team:
            print("Error: Orchestrator client or team not initialized.")
            return {}

        team_description = "\n".join(
            f"- Name: '{agent.name}', Role: `{agent.role}`, Goal: {agent.goal}" for agent in self.team
        )
        planning_prompt = [
            f"We are meta-artificial intelligence, working cohesively to create a detailed, step-by-step execution plan based on a high-level goal.",

            f"The final output must be a single JSON object containing a 'steps' key, where 'steps' is a list of tasks.\n"
            f"Each task in the list must have a 'role' and a 'task' description.\n"
            f"The 'role' in each step must exactly match one of the roles from the team list provided below. Do not use the agent's name.\n"
            f"Leverage the team members' goals to create a collaborative plan. For instance, a 'Prompt Engineer' should be used to refine the system prompts of other agents.",

            f"High-Level Goal: '{high_level_goal}'\n"
            f"Available Team Members:\n{team_description}",

            f"Generate the JSON plan."
        ]
        session.add_artifact("planning_prompt.txt", "\n\n".join(planning_prompt))

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=planning_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            plan = json.loads(response.text or '{}')
        except Exception as e:
            print(f"Error generating plan for {self.name}: {e}")
            plan = {"error": str(e)}

        session.add_artifact("initial_plan.json", plan)
        return plan



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
    prompt_key = f"{spec['name'].lower()}_instructions.txt"
    if spec.get('name') == 'Meta-AI':
        prompt_key = 'orchestrator_instructions.txt'

    if prompt_key not in prompts:
        print(f"Warning: Prompt for agent '{spec['name']}' not found with key '{prompt_key}'. Skipping.")
        return None

    agent_class = Orchestrator if spec.get('role') == 'Orchestrator' else Agent

    agent = agent_class(
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
    return next((agent for agent in agents if agent.role == role), None)

def system_runtime_bootstrap(root_dir: str, initial_task: str):
    print("--- System Runtime Bootstrap ---")

    config = load_config(os.path.join(root_dir, "config", "runtime.yaml"))
    agent_specs = load_agent_templates(os.path.join(root_dir, "agents"))
    prompts = load_prompts(os.path.join(root_dir, "prompts"))

    all_team_members = {member.lower() for spec in agent_specs if 'team' in spec for member in spec['team']}

    agents = []
    for spec in agent_specs:
        if spec['name'].lower() not in all_team_members:
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

    if not isinstance(orchestrator, Orchestrator):
        print(f"Error: Agent with role '{orchestrator_role}' is not a valid Orchestrator instance. Bootstrap aborted.")
        return

    session = Session(agents=agents)

    print("\n--- Starting Workflow ---")
    orchestrator.start_workflow(session, initial_task)

    print("\n--- System Runtime Bootstrap Complete ---")

def system_main():
    parser = argparse.ArgumentParser(description="Run the Gemini agent runtime.")
    parser.add_argument("task", type=str, help="The initial task for the orchestrator to perform.")
    args = parser.parse_args()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    system_runtime_bootstrap(project_root, args.task)


if __name__ == "__main__":
    system_main()
