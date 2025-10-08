import os from 'os';
import path from 'path';
import fs from 'fs';
import yaml from 'js-yaml';
import { glob } from 'glob';

import { Agent, AgentSpec, PromptSpec } from '../agent/Agent';
import { Session } from '../core/Session';
import { ExecutionContext } from '../core/ExecutionContext';
import { Plan, File, Task, Role, Artifact } from '../custom_types';
import { LLM } from '../llm/LLM';
import { Logger } from '../logger/Logger';
import { read_file } from '../util/Util'; // Utility to read files

const logger = Logger.getInstance();

export class Orchestrator extends Agent {
  public team: Record<string, Agent> = {}; // Agents delegated to by this orchestrator

  constructor(name: string, role: string, goal: string, model: string, systemPrompt: string) {
    super(name, role, goal, model, systemPrompt);
    logger.info(`Orchestrator instance created: ${this.name} (Role: ${this.role}, Goal: ${this.goal}, Model: ${this.model})`);
  }

  /**
   * Generates a plan for the given high-level goal, considering available agents and context.
   * @param session The current session.
   * @param highLevelGoal The overall objective of the workflow.
   * @param files Initial files provided to the system.
   * @returns A Plan object or null if generation fails.
   */
  public async generatePlan(session: Session, highLevelGoal: string, files: File[] = []): Promise<Plan | null> {
    logger.info(`Orchestrator ${this.name} is generating a plan for: '${highLevelGoal}'`);

    if (!this.llm) {
      logger.error('LLM client is not initialized for the orchestrator.');
      return null;
    }

    // Construct a description of the available agents and their roles/goals for the prompt
    const teamDescription = Object.values(this.team).map(agent =>
      `    - Name: '${agent.name}'\n      Role:\n        title: '${agent.role}'\n        purpose: '${agent.goal}'`
    ).join('\n');

    // Load the general planning prompt template
    // NOTE: This path might need adjustment based on where prompts are stored relative to the executing script.
    const promptTemplatePath = path.resolve(__dirname, '..', 'prompts', 'general_planning.txt');
    const generalPromptTemplate = read_file(promptTemplatePath);

    if (!generalPromptTemplate || generalPromptTemplate.startsWith('Error:')) {
      logger.error(`Failed to load planning prompt template from ${promptTemplatePath}.`);
      return null;
    }

    // Format the prompt with goal, team description, and initial files
    let planningPrompt = generalPromptTemplate.replace('{high_level_goal}', highLevelGoal).replace('{team_description}', teamDescription);

    if (files.length > 0) {
      const fileSection = files.map(file =>
        `--- File: '${file.path}'\n${file.content}`
      ).join('\n\n');
      planningPrompt += `\n\nPlease consider the following input files:\n${fileSection}\n\n`;
    }

    logger.debug(`Planning prompt for LLM:\n${planningPrompt}`);
    await session.recordArtifact('planning_prompt.txt', planningPrompt);

    try {
      const response = await this.llm.generateContent(
        this.model, // Use the orchestrator's model
        planningPrompt,
        this.systemPrompt, // Use orchestrator's system prompt
        0.1, // Lower temperature for more deterministic planning
        'application/json', // Expect JSON output
        Plan // Specify the expected response schema
      );

      let plan: Plan;
      if (response instanceof Plan) {
        plan = response;
      } else {
        // Attempt to parse if not already a Plan instance (e.g., if response is JSON string)
        plan = Plan.parse(response); // Use Pydantic's parse method
      }

      logger.info('Successfully generated plan.');
      return plan;

    } catch (error) {
      logger.error(`Error generating plan: ${(error as Error).message}`, error);
      // Optionally, record the error or a partial plan if available
      await session.recordArtifact('plan_generation_error.txt', (error as Error).message);
      return null;
    }
  }

  /**
   * Executes a task within the context of the current execution.
   * This method is typically overridden by specific agent types.
   * For Orchestrator, it might involve delegating or performing planning actions.
   * @param context The current execution context.
   * @returns The result of the task execution.
   */
  public async executeTask(context: ExecutionContext): Promise<string | null> {
    // If the current step requires generating a plan, call generatePlan
    if (context.currentStep().description.toLowerCase().includes('generate plan')) {
      const plan = await this.generatePlan(context.session, context.plan.highLevelGoal, context.getInitialFiles());
      if (plan) {
        // Record the generated plan as part of the context's output for this step
        const artifactFile = new File({path: 'generated_plan.json', content: JSON.stringify(plan, null, 2)});
        return JSON.stringify(new AgentOutput({ output: 'Plan generated successfully.', artifact: { task: context.currentStep().id, files: [artifactFile] }, reasoning: 'Orchestrator completed plan generation task.' }));
      } else {
        return JSON.stringify(new AgentOutput({ output: 'Failed to generate plan.', reasoning: 'Orchestrator failed during plan generation.' }));
      }
    }

    // Default execution: delegate to base Agent or handle specific orchestrator logic
    logger.warn(`Orchestrator ${this.name} is executing a generic task. Default behavior is to delegate or plan.`);
    // Placeholder response if no specific logic is matched
    return JSON.stringify(new AgentOutput({ output: `Orchestrator ${this.name} placeholder task execution.`, reasoning: 'Default orchestrator task handling.' }));
  }
}
