import { System } from './System';
import { Agent, AgentSpec, PromptSpec } from '../agent/Agent';
import { Orchestrator } from '../orchestrator/Orchestrator';
import { Session } from '../core/Session';
import { ExecutionContext } from '../core/ExecutionContext';
import { Plan, File } from '../custom_types';
import { MockLLM } from '../__mocks__/MockLLM';
import { mockSystemConfig, mockAgentSpecs, mockPrompts } from '../__mocks__/SystemMocks';
import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { glob } from 'glob';

// Mock dependencies
jest.mock('uuid', () => ({ v4: () => 'mock-uuid-system' }));
jest.mock('fs');
jest.mock('path');
jest.mock('js-yaml');
jest.mock('glob');
jest.mock('../llm/LLM', () => ({ LLM: jest.fn().mockImplementation(() => new MockLLM()) }));
jest.mock('../logger/Logger'); // Mock Logger to avoid console output during tests

describe('System Core Component Testing', () => {
  let system: System;
  const mockProjectRoot = '/mock/project/root';
  const mockDefaultModel = 'mock-model';

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();

    // Mock file system operations used by System setup
    jest.spyOn(fs, 'readFileSync').mockImplementation((filePath: string | URL) => {
      const pathStr = typeof filePath === 'string' ? filePath : filePath.toString();
      if (pathStr.includes('runtime.yaml')) {
        return JSON.stringify(mockSystemConfig);
      }
      if (pathStr.includes('agents') && pathStr.endsWith('.yaml')) {
        const agentName = path.basename(pathStr, '.yaml');
        const spec = mockAgentSpecs.find(s => s.name.toLowerCase() === agentName);
        return JSON.stringify(spec);
      }
      if (pathStr.includes('prompts') && pathStr.endsWith('.txt')) {
        const promptName = path.basename(pathStr);
        return mockPrompts[promptName] || 'Default prompt content';
      }
      return '{}'; // Default empty content
    });
    jest.spyOn(glob, 'sync').mockReturnValue([
      path.join(mockProjectRoot, 'config', 'runtime.yaml'),
      path.join(mockProjectRoot, 'agents', 'meta-ai.yaml'),
      path.join(mockProjectRoot, 'agents', 'prompt-engineer.yaml'),
      path.join(mockProjectRoot, 'prompts', 'meta-ai_instructions.txt'),
      path.join(mockProjectRoot, 'prompts', 'prompt-engineer_instructions.txt'),
    ]);
    jest.spyOn(path, 'resolve').mockImplementation((...args) => args.join('/'));
    jest.spyOn(path, 'dirname').mockReturnValue('/mock/dir');
    jest.spyOn(path, 'basename').mockImplementation((p) => p.split('/').pop() || '');
    jest.spyOn(fs, 'existsSync').mockReturnValue(true);
    jest.spyOn(os, 'makedirs').mockImplementation(() => {});
    (yaml.load as jest.Mock).mockReturnValue(mockSystemConfig);

    system = new System(mockProjectRoot, mockDefaultModel);
  });

  it('should initialize and setup the system correctly', async () => {
    await system.setup('Meta-AI');

    expect(system.config).toEqual(mockSystemConfig);
    expect(system.agents.length).toBeGreaterThan(0);
    expect(system['orchestrator']).toBeInstanceOf(Orchestrator);
    expect(system['orchestrator']?.name).toBe('Meta-AI');
    expect(system['session']).toBeInstanceOf(Session);
    expect(system.agents.find(a => a.name === 'Prompt Engineer')).toBeDefined();
  });

  it('should throw an error if no agents can be instantiated', async () => {
    // Mock glob to return no agent files
    jest.spyOn(glob, 'sync').mockReturnValue([path.join(mockProjectRoot, 'config', 'runtime.yaml')]);
    // Mock readFileSync to return empty for any agent spec attempts
    jest.spyOn(fs, 'readFileSync').mockImplementation((filePath: string | URL) => {
      if (typeof filePath === 'string' && filePath.includes(RUNTIME_CONFIG_FILENAME)) {
        return JSON.stringify({ ...mockSystemConfig, agents: [] });
      }
      return '{}';
    });

    await expect(system.setup('Meta-AI')).rejects.toThrow('No agents could be instantiated.');
  });

  it('should throw an error if orchestrator is not found', async () => {
    await expect(system.setup('NonExistentOrchestrator')).rejects.toThrow("Orchestrator with name 'NonExistentOrchestrator' not found.");
  });

  it('should throw an error if the found orchestrator is not an Orchestrator instance', async () => {
    // Find an agent that is NOT an Orchestrator and try to set it as such
    const nonOrchestratorAgent = system.agents.find(a => a.name !== 'Meta-AI');
    if (nonOrchestratorAgent) {
      await expect(system.setup(nonOrchestratorAgent.name)).rejects.toThrow(`Agent '${nonOrchestratorAgent.name}' is not a valid Orchestrator instance.`);
    } else {
      // Fallback if no other agent exists (should not happen with current mocks)
      await expect(system.setup('SomeOtherAgent')).rejects.toThrow();
    }
  });

  it('should start the workflow and generate a plan', async () => {
    await system.setup('Meta-AI');
    const mockPlan = new Plan({ ...mockSystemConfig.plan, highLevelGoal: 'Test Goal', reasoning: 'Test Reasoning', roles: [], tasks: [] });
    // Mock the orchestrator's generatePlan method
    const mockOrchestrator = system['orchestrator'] as Orchestrator;
    jest.spyOn(mockOrchestrator, 'generatePlan').mockResolvedValue(mockPlan);

    const plan = await system.start('Test High Level Goal');

    expect(plan).toBe(mockPlan);
    expect(mockOrchestrator.generatePlan).toHaveBeenCalled();
    expect(system['session']?.addArtifact).toHaveBeenCalledWith('initial_plan.json', JSON.stringify(mockPlan, null, 2));
  });

  it('should throw an error if plan generation fails during start', async () => {
    await system.setup('Meta-AI');
    const mockOrchestrator = system['orchestrator'] as Orchestrator;
    jest.spyOn(mockOrchestrator, 'generatePlan').mockResolvedValue(null as any);

    await expect(system.start('Test Goal')).rejects.toThrow('Orchestration failed: Could not generate a valid plan.');
  });

  it('should run the workflow for the specified number of rounds', async () => {
    await system.setup('Meta-AI');
    const mockPlan = new Plan({ ...mockSystemConfig.plan, highLevelGoal: 'Test Goal', reasoning: 'Test Reasoning', roles: [], tasks: [{ id: 'T1', description: 'Mock Task', role: 'Tester', agent: 'TestAgent', requires: [] }] });
    const mockOrchestrator = system['orchestrator'] as Orchestrator;
    jest.spyOn(mockOrchestrator, 'generatePlan').mockResolvedValue(mockPlan);

    // Mock agent execution
    const mockAgentInstance = system.agents.find(a => a.name === 'TestAgent') as Agent;
    const executeTaskSpy = jest.spyOn(mockAgentInstance, 'executeTask').mockResolvedValue(JSON.stringify({ output: 'Mock Task Output' }));

    await system.start('Test Goal'); // Generate plan first
    await system.run(mockPlan, 2);

    expect(executeTaskSpy).toHaveBeenCalledTimes(2); // Called once per round
    expect(system['session']?.recordArtifact).toHaveBeenCalledWith(expect.stringContaining('task_output_T1_round_'), expect.any(String));
  });

  it('should handle agent execution errors gracefully during run', async () => {
    await system.setup('Meta-AI');
    const mockPlan = new Plan({ ...mockSystemConfig.plan, highLevelGoal: 'Test Goal', reasoning: 'Test Reasoning', roles: [], tasks: [{ id: 'T1', description: 'Mock Task', role: 'Tester', agent: 'TestAgent', requires: [] }] });
    const mockOrchestrator = system['orchestrator'] as Orchestrator;
    jest.spyOn(mockOrchestrator, 'generatePlan').mockResolvedValue(mockPlan);

    const mockAgentInstance = system.agents.find(a => a.name === 'TestAgent') as Agent;
    const executeTaskSpy = jest.spyOn(mockAgentInstance, 'executeTask').mockRejectedValue(new Error('Agent execution failed'));

    await system.start('Test Goal');
    await system.run(mockPlan, 1);

    expect(executeTaskSpy).toHaveBeenCalledTimes(1);
    expect(system['session']?.recordArtifact).toHaveBeenCalledWith(expect.stringContaining('task_error_T1_round_'), expect.any(String));
  });

  it('should update agent prompts based on AgentOutput team prompts', async () => {
    await system.setup('Meta-AI');
    const mockPlan = new Plan({ ...mockSystemConfig.plan, highLevelGoal: 'Test Goal', reasoning: 'Test Reasoning', roles: [], tasks: [{ id: 'T1', description: 'Mock Task', role: 'Prompt Engineer', agent: 'Prompt Engineer', requires: [] }] });
    const mockOrchestrator = system['orchestrator'] as Orchestrator;
    jest.spyOn(mockOrchestrator, 'generatePlan').mockResolvedValue(mockPlan);

    const promptEngineerAgent = system.agents.find(a => a.name === 'Prompt Engineer') as Agent;
    const originalPrompt = promptEngineerAgent.systemPrompt;
    const newPrompt = 'New system prompt for Prompt Engineer';

    const mockAgentOutput = new AgentOutput({ 
      output: 'Success', 
      team: { notes: 'Prompt updated', prompts: [{ agent: 'Prompt Engineer', role: 'Prompt Engineer', systemPrompt: newPrompt }] }
    });
    const executeTaskSpy = jest.spyOn(promptEngineerAgent, 'executeTask').mockResolvedValue(mockAgentOutput.toJSON());

    await system.start('Test Goal');
    await system.run(mockPlan, 1);

    expect(promptEngineerAgent.systemPrompt).toBe(newPrompt);
    expect(promptEngineerAgent.systemPrompt).not.toBe(originalPrompt);
  });

  it('should fall back to orchestrator if assigned agent is not found', async () => {
    await system.setup('Meta-AI');
    const mockPlan = new Plan({ ...mockSystemConfig.plan, highLevelGoal: 'Test Goal', reasoning: 'Test Reasoning', roles: [], tasks: [{ id: 'T_NotFound', description: 'Task for unknown agent', role: 'Unknown', agent: 'NonExistentAgent', requires: [] }] });
    const mockOrchestrator = system['orchestrator'] as Orchestrator;
    jest.spyOn(mockOrchestrator, 'generatePlan').mockResolvedValue(mockPlan);

    // Mock the orchestrator's executeTask method as it will be the fallback
    const orchestratorExecuteTaskSpy = jest.spyOn(mockOrchestrator, 'executeTask').mockResolvedValue(JSON.stringify({ output: 'Fallback execution success' }));

    await system.start('Test Goal');
    await system.run(mockPlan, 1);

    expect(orchestratorExecuteTaskSpy).toHaveBeenCalledTimes(1);
  });
});
