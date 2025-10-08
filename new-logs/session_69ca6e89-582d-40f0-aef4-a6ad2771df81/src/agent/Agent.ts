import { LLM } from '../llm/LLM';
import { Session } from '../core/Session';
import { ExecutionContext } from '../core/ExecutionContext';
import { AgentOutput, Artifact, File, Plan, Role, Team, Prompt, Task } from '../custom_types';
import { Logger } from '../logger/Logger';
import { v4 as uuidv4 } from 'uuid';

const logger = Logger.getInstance();

// Define interfaces for agent specifications and prompts for clarity
export interface AgentSpec {
  name: string;
  role: string;
  goal: string;
  model?: string;
  systemPromptPath?: string; // Path to the system prompt file
  team?: AgentSpec[]; // For nested delegation
}

export interface PromptSpec {
  agent: string;
  role: string;
  systemPrompt: string;
}

// Represents an item stored in the ExecutionContext's memory
export class ContextItem {
  constructor(
    public name: string,
    public content: any,
    public step: Task // The task during which this item was recorded
  ) {}
}

export class Agent {
  public name: string;
  public role: string;
  public goal: string;
  public model: string;
  public systemPrompt: string;
  public llm: LLM;
  public team: Record<string, Agent> = {}; // For agents that delegate tasks

  constructor(name: string, role: string, goal: string, model: string, systemPrompt: string) {
    this.name = name;
    this.role = role;
    this.goal = goal;
    this.model = model;
    this.systemPrompt = systemPrompt;
    logger.info(`Agent instance created: ${this.name} (Role: ${this.role}, Goal: ${this.goal}, Model: ${this.model})`);
    this.llm = LLM.factory(model); // Use factory to get LLM instance
  }

  /**
   * Updates the agent's system prompt.
   * @param newPrompt The new system prompt content.
   */
  public updateSystemPrompt(newPrompt: string): void {
    this.systemPrompt = newPrompt;
    logger.info(`Agent ${this.name}'s system prompt updated.`);
  }

  /**
   * Executes a task based on the current execution context.
   * @param context The ExecutionContext containing plan, session, and step information.
   * @returns A Promise resolving to the agent's output (JSON string) or null.
   */
  public async executeTask(context: ExecutionContext): Promise<string | null> {
    const task = context.currentStep();
    const requiredTaskIds = ['initial', ...task.requires];

    // Record the system prompt used for this execution
    await context.recordArtifact(`${this.name}_system_prompt.txt`, this.systemPrompt);

    // Gather artifacts from previous steps based on task requirements
    const relevantArtifacts = Object.values(context.items).filter(item =>
      requiredTaskIds.includes(item.step.id)
    );

    const previousArtifactsString = relevantArtifacts.map(artifact =>
      `--- Artifact '${artifact.name}' from (${artifact.step.role}) in [${artifact.step.id}]:\n${artifact.content}`
    ).join('\n\n');

    // Construct the prompt for the LLM
    const promptParts: string[] = [
      `The overall goal is: '${context.plan.highLevelGoal}'`,
      `Your role's specific goal is: '${this.goal}'`,
      `Your specific sub-task is: '${task.description}'`,
      `Team roles definition:\n${JSON.stringify(context.plan.roles, null, 2)}`,
    ];

    if (previousArtifactsString) {
      promptParts.push(`Please use the following outputs from other agents as your input:\n${previousArtifactsString}`);
    }

    const fullPrompt = promptParts.join('\n\n');
    await context.recordArtifact(`${this.name}_task_prompt.txt`, fullPrompt);
    logger.debug(`Executing task '${task.id}' for agent '${this.name}' with prompt:\n${fullPrompt}`);

    try {
      // Generate content using the LLM
      const response = await this.llm.generateContent(
        this.model,
        fullPrompt,
        this.systemPrompt,
        0.7, // Default temperature
        'application/json', // Expect JSON output for structured responses
        AgentOutput // Use AgentOutput schema for parsing
      );

      let agentOutputJson: string;
      if (response instanceof AgentOutput) {
        // If response is already parsed AgentOutput, stringify it
        agentOutputJson = response.toJSON();
      } else if (typeof response === 'string') {
        // If response is a string, attempt to parse and validate as AgentOutput
        try {
           const parsedOutput = AgentOutput.parse(response);
           agentOutputJson = parsedOutput.toJSON();
        } catch (validationError) {
           logger.warn(`Agent output for task '${task.id}' is not a valid AgentOutput JSON. Response: ${response}. Treating as plain text.`);
           // If validation fails, treat the raw response as the output
           agentOutputJson = JSON.stringify({ output: response, reasoning: 'Raw LLM output, failed to parse as AgentOutput.' });
        }
      } else {
        // Handle unexpected response types (e.g., null, undefined)
        logger.error(`Unexpected response type from LLM for agent ${this.name}: ${typeof response}`);
        agentOutputJson = JSON.stringify({ output: `Error: Unexpected LLM response type for task ${task.id}.`, reasoning: 'LLM returned invalid format.' });
      }

      // Process artifacts from the agent's output
      let parsedOutput: AgentOutput;
      try {
        // Ensure we are working with a valid AgentOutput object for artifact processing
        parsedOutput = AgentOutput.parse(agentOutputJson);
      } catch (e) {
        logger.error(`Failed to parse final agent output JSON for task '${task.id}'.`, e);
        // Fallback: use the raw JSON string as the output if parsing completely fails
        parsedOutput = new AgentOutput({ output: agentOutputJson, reasoning: 'Failed to parse final agent output.' });
      }

      if (parsedOutput.artifact?.files) {
        for (const file of parsedOutput.artifact.files) {
          // Use a more specific key including task ID and round number for session storage
          const fileArtifactKey = `${this.name}_${task.id}_${context.roundNum}_${file.path}`;
          await context.recordArtifact(fileArtifactKey, file.content);
          logger.debug(`Recorded artifact file: ${file.path}`);
        }
      }

      // Return the JSON string representation of the AgentOutput
      return parsedOutput.toJSON();

    } catch (error) {
      logger.error(`Error during LLM content generation for agent ${this.name}, task ${task.id}:`, error);
      // Record the error as an artifact
      await context.recordArtifact(`${this.name}_task_error_${task.id}.txt`, (error as Error).message);
      throw error; // Re-throw the error to be caught by the System's runner
    }
  }
}

/**
 * Finds an agent in a list by its role.
 * @param agents List of Agent objects.
 * @param role The role of the agent to find.
 * @returns The found Agent object, or undefined if not found.
 */
export function findAgentByRole(agents: Agent[], role: string): Agent | undefined {
  logger.debug(`Searching for agent with role: ${role} in agents: ${agents.map(a => a.name).join(', ')}`);
  return agents.find(agent => agent.role.toLowerCase() === role.toLowerCase());
}
