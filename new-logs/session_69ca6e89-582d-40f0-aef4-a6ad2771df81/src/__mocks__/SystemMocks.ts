import { AgentSpec, PromptSpec } from '../agent/Agent';

export const mockSystemConfig = {
  loggingLevel: 'DEBUG',
  defaultModel: 'gemini-2.5-flash-latest',
  plan: {
    highLevelGoal: 'Initial Goal',
    reasoning: 'Initial Reasoning',
    roles: [],
    tasks: [],
  },
};

export const mockAgentSpecs: AgentSpec[] = [
  {
    name: 'Meta-AI',
    role: 'Orchestrator',
    goal: 'Orchestrate the workflow and generate plans.',
    model: 'gemini-2.5-flash-latest',
    systemPromptPath: 'meta-ai_instructions.txt',
    team: [
      { name: 'Prompt Engineer', role: 'Prompt Engineer', goal: 'Refine prompts for agents.' },
    ],
  },
  {
    name: 'Prompt Engineer',
    role: 'Prompt Engineer',
    goal: 'Refine prompts for agents.',
    model: 'gemini-2.5-flash-latest',
    systemPromptPath: 'prompt-engineer_instructions.txt',
  },
  {
    name: 'Developer',
    role: 'Developer',
    goal: 'Implement code based on requirements.',
    model: 'gemini-2.5-flash-latest',
    systemPromptPath: 'developer_instructions.txt', // Assuming this file exists
  },
  {
    name: 'Tester',
    role: 'Tester',
    goal: 'Test the implemented code.',
    model: 'gemini-2.5-flash-latest',
    systemPromptPath: 'tester_instructions.txt', // Assuming this file exists
  },
];

export const mockPrompts: Record<string, PromptSpec> = {
  'meta-ai_instructions.txt': 'You are Meta-AI, an Orchestrator. Your goal is to create a plan based on the high-level goal and available team roles. Analyze the team description and provide a structured plan.',
  'prompt-engineer_instructions.txt': 'You are a Prompt Engineer. Your role is to refine prompts for other agents based on feedback and performance. Analyze the output and suggest improvements.',
  'developer_instructions.txt': 'You are a Developer. Implement the given task description accurately.',
  'tester_instructions.txt': 'You are a Tester. Write test cases and execute them.',
};
