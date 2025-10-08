import { BaseModel, Field, model_validator } from 'pydantic';
import { z } from 'zod'; // Import Zod for potential schema definition or validation demonstration

// --- Core Types representing Task Agnostic Steps (TAS) ---

/** Represents a single actionable step within a plan. */
export class Task extends BaseModel {
  id: string = Field(..., { description: "Unique ID for the task (e.g., 'T1', 'T2')." });
  description: string = Field(..., { description: "Detailed description of what to do for this task." });
  role: string = Field(..., { description: "The role responsible for performing this task." });
  agent: string = Field(..., { description: "The specific agent assigned to execute this task." });
  requires: string[] = Field([], { description: "List of task IDs whose outputs are required as prerequisites (e.g., ['T1', 'T2'])." });
}

/** Represents a file generated or used within the system. */
export class File extends BaseModel {
  path: string = Field(..., { description: "File path or name (e.g., 'src/main.py')." });
  content: string = Field(..., { description: "Full content of the file." });
}

/** Represents the output artifact of a completed task. */
export class Artifact extends BaseModel {
  task: string = Field(..., { description: "ID of the task that produced this artifact (e.g., 'T1')." });
  files: File[] = Field([], { description: "List of files created or modified by the task." });
}

/** Defines a role within the system or team. */
export class Role extends BaseModel {
  title: string = Field(..., { description: "Title of the role (e.g., 'Engineer', 'Reviewer')." });
  purpose: string = Field(..., { description: "The main purpose and high-level responsibilities of this role." });
}

/** Represents a system prompt configuration for an agent. */
export class Prompt extends BaseModel {
  agent: string = Field(..., { description: "Name of the agent this prompt is for. Must match exactly an existing agent." });
  role: string = Field(..., { description: "Role context of the agent." });
  systemPrompt: string = Field(..., { description: "Full text of the system prompt for this agent." });
}

/** Contains metadata and coordination information for the team, including prompt updates. */
export class Team extends BaseModel {
  notes: string = Field('', { description: "General notes or feedback about the team's performance or the plan." });
  prompts: Prompt[] = Field([], { description: "A list of new or updated system prompts for agents in the team." });
}

/** Defines the overall plan for a workflow, including goal, roles, and tasks. */
export class Plan extends BaseModel {
  highLevelGoal: string = Field(..., { description: "The main goal this plan is designed to achieve." });
  reasoning: string = Field(..., { description: "A brief explanation of the plan's structure and strategy." });
  roles: Role[] = Field([], { description: "List of all roles required to execute the plan." });
  tasks: Task[] = Field([], { description: "A step-by-step sequence of tasks to be executed in order." });
  team: Team | null = Field(null, { description: "Optional updates to team configuration or system prompts." });
}

/**
 * Represents the structured output returned by an agent after executing a task.
 * Adheres to the JSON output format expected by the runtime.
 */
export class AgentOutput extends BaseModel {
  output: string = Field(..., { description: "A summary of the work done. Do not include file contents here; use the 'artifact' field instead." });
  artifact: Artifact | null = Field(null, { description: "Optional artifact containing files created or modified by the agent." });
  team: Team | null = Field(null, { description: "Optional updates to team configuration or system prompts." });
  reasoning: string | null = Field(null, { description: "Explanation of how the agent arrived at this output." });

  /**
   * Custom validator to ensure that an AgentOutput contains either an 'output' message or an 'artifact'.
   */
  @model_validator(mode='after')
  validateOutputAndArtifact(): this {
    if (!this.output && !this.artifact) {
      throw new Error('Agent output must contain either an "output" message or an "artifact".');
    }
    return this;
  }
}

// --- Example Usage & Schema Generation ---
// This block executes only when the script is run directly
if (require.main === module) {
  console.log('--- AgentOutput Schema ---\n', JSON.stringify(AgentOutput.model_json_schema(), null, 2));
  console.log('\n--- Plan Schema ---\n', JSON.stringify(Plan.model_json_schema(), null, 2));
}
