import { Orchestrator } from './Orchestrator';
import { Agent, AgentSpec, PromptSpec } from '../agent/Agent';
import { Session } from '../core/Session';
import { Plan, File } from '../custom_types';
import { MockLLM } from '../__mocks__/MockLLM';
import { mockSystemConfig, mockAgentSpecs, mockPrompts } from '../__mocks__/SystemMocks';
import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { glob } from 'glob';

// Mock dependencies
jest.mock('uuid', () => ({ v4: () => 'mock-uuid-orchestrator' }));
jest.mock('../llm/LLM', () => ({ LLM: jest.fn().mockImplementation(() => new MockLLM()) }));
jest.mock('../util/Util', () => ({ read_file: jest.fn() })); // Mock read_file
jest.mock('fs');
jest.mock('path');
jest.mock('js-yaml');
jest.mock('glob');
jest.mock('../logger/Logger'); // Mock Logger

describe('Orchestrator Core Component Testing', () => {
  let mockSession: Session;
  let mockOrchestrator: Orchestrator;
  let mockLLM: MockLLM;
  let mockAgentInstance: Agent;

  beforeAll(() => {
    // Mock file system operations needed for setup
    jest.spyOn(fs, 'readFileSync').mockImplementation((filePath: string | URL) => {
      const pathStr = typeof filePath === 'string' ? filePath : filePath.toString();
      if (pathStr.includes('runtime.yaml')) return JSON.stringify(mockSystemConfig);
      if (pathStr.includes('agents') && pathStr.endsWith('.yaml')) {
        const agentName = path.basename(pathStr, '.yaml');
        return JSON.stringify(mockAgentSpecs.find(s => s.name.toLowerCase() === agentName));
      }
      if (pathStr.includes('prompts') && pathStr.endsWith('.txt')) {
        const promptName = path.basename(pathStr);
        return mockPrompts[promptName] || 'Default prompt content';
      }
      return '{}';
    });
    jest.spyOn(glob, 'sync').mockReturnValue([
      path.join('/mock/root', 'config', 'runtime.yaml'),
      path.join('/mock/root', 'agents', 'meta-ai.yaml'),
      path.join('/mock/root', 'agents', 'prompt-engineer.yaml'),
      path.join('/mock/root', 'prompts', 'meta-ai_instructions.txt'),
    ]);
    jest.spyOn(path, 'resolve').mockImplementation((...args) => args.join('/'));
    jest.spyOn(fs, 'existsSync').mockReturnValue(true);
    jest.spyOn(yaml, 'load').mockReturnValue(mockSystemConfig);
    jest.spyOn(fs.promises, 'writeFile').mockResolvedValue(); // Mock writeFile for Session
    jest.spyOn(fs.promises, 'mkdir').mockResolvedValue(); // Mock mkdir for Session
  });

  beforeEach(async () => {
    jest.clearAllMocks();

    // Re-mock file system interactions specific to System setup
    jest.spyOn(fs, 'readFileSync').mockImplementation((filePath: string | URL) => {
      const pathStr = typeof filePath === 'string' ? filePath : filePath.toString();
      if (pathStr.includes('runtime.yaml')) return JSON.stringify(mockSystemConfig);
      if (pathStr.includes('agents') && pathStr.endsWith('.yaml')) {
        const agentName = path.basename(pathStr, '.yaml');
        return JSON.stringify(mockAgentSpecs.find(s => s.name.toLowerCase() === agentName));
      }
      if (pathStr.includes('prompts') && pathStr.endsWith('.txt')) {
        const promptName = path.basename(pathStr);
        return mockPrompts[promptName] || 'Default prompt content';
      }
      return '{}';
    });
    jest.spyOn(glob, 'sync').mockReturnValue([
      path.join('/mock/root', 'config', 'runtime.yaml'),
      path.join('/mock/root', 'agents', 'meta-ai.yaml'),
      path.join('/mock/root', 'agents', 'prompt-engineer.yaml'),
      path.join('/mock/root', 'prompts', 'meta-ai_instructions.txt'),
    ]);
    jest.spyOn(path, 'resolve').mockImplementation((...args) => args.join('/'));
    jest.spyOn(fs, 'existsSync').mockReturnValue(true);
    jest.spyOn(yaml, 'load').mockReturnValue(mockSystemConfig);
    (fs.promises.writeFile as jest.Mock).mockResolvedValue();
    (fs.promises.mkdir as jest.Mock).mockResolvedValue();

    // Initialize Session and Agent dependencies
    const sessionAgents = [new Agent('TestAgent', 'Tester', 'Test Goal', 'mock-model', 'Initial prompt')];
    mockSession = new Session(sessionAgents, '/mock/project/root');

    // Instantiate Orchestrator
    const orchestratorSpec = mockAgentSpecs.find(spec => spec.name === 'Meta-AI');
    if (!orchestratorSpec) throw new Error('Meta-AI spec not found');
    mockLLM = new MockLLM();
    mockOrchestrator = new Orchestrator(
      orchestratorSpec.name,
      orchestratorSpec.role,
      orchestratorSpec.goal,
      orchestratorSpec.model || 'mock-model',
      mockPrompts[orchestratorSpec.name.toLowerCase() + '_instructions.txt']
    );
    mockOrchestrator.llm = mockLLM; // Inject mock LLM
    mockOrchestrator.team = {}; // Initialize team

    // Add other agents to the orchestrator's team if specified in config
    if (orchestratorSpec.team) {
      orchestratorSpec.team.forEach(memberSpec => {
        const memberAgent = new Agent(memberSpec.name, memberSpec.role || 'Unknown', memberSpec.goal || '', memberSpec.model || 'mock-model', mockPrompts[memberSpec.name.toLowerCase() + '_instructions.txt'] || '');
        mockOrchestrator.team[memberSpec.name] = memberAgent;
      });
    }

    // Mock the Agent class's constructor and methods if needed
    jest.spyOn(Agent.prototype, 'executeTask').mockResolvedValue(JSON.stringify({ output: 'Mock task output' }));
  });

  it('should generate a plan using the LLM', async () => {
    const highLevelGoal = 'Develop a new feature';
    const files: File[] = [new File({ path: 'feature.md', content: 'Feature details' })];
    const mockPlanResponse = new Plan({
      highLevelGoal: highLevelGoal,
      reasoning: 'Plan reasoning',
      roles: [{ title: 'Developer', purpose: 'Develop code' }],
      tasks: [
        new Task({ id: 'T1', description: 'Implement feature', role: 'Developer', agent: 'DeveloperAgent', requires: [] }),
      ],
    });

    // Configure MockLLM to return the mock plan
    mockLLM.generateContent.mockResolvedValue(mockPlanResponse.toJSON());

    const plan = await mockOrchestrator.generatePlan(mockSession, highLevelGoal, files);

    expect(plan).toBeInstanceOf(Plan);
    expect(plan?.highLevelGoal).toBe(highLevelGoal);
    expect(mockLLM.generateContent).toHaveBeenCalled();
    expect(mockSession.addArtifact).toHaveBeenCalledWith('planning_prompt.txt', expect.any(String));
  });

  it('should handle invalid JSON or validation errors during plan generation', async () => {
    const highLevelGoal = 'Generate invalid plan';
    // Mock LLM to return invalid JSON
    mockLLM.generateContent.mockResolvedValue('This is not JSON');

    await expect(mockOrchestrator.generatePlan(mockSession, highLevelGoal)).rejects.toThrow(); // Expecting validation error

    // Mock LLM to return valid JSON but invalid structure for Plan
    mockLLM.generateContent.mockResolvedValue(JSON.stringify({ invalid: 'structure' }));
    await expect(mockOrchestrator.generatePlan(mockSession, highLevelGoal)).rejects.toThrow(); // Expecting validation error
  });

  it('should correctly format the planning prompt with team description and files', async () => {
    const highLevelGoal = 'Develop a new feature';
    const files: File[] = [new File({ path: 'feature.md', content: 'Feature details' })];
    const mockPlanResponse = new Plan({
      highLevelGoal: highLevelGoal,
      reasoning: 'Plan reasoning',
      roles: [{ title: 'Developer', purpose: 'Develop code' }],
      tasks: [],
    });
    mockLLM.generateContent.mockResolvedValue(mockPlanResponse.toJSON());

    await mockOrchestrator.generatePlan(mockSession, highLevelGoal, files);

    // Check if the prompt passed to LLM contains the team description and file content
    const promptPassedToLLM = mockLLM.generateContent.mock.calls[0][1]; // Second argument is contents
    expect(promptPassedToLLM).toContain('Team Description:');
    expect(promptPassedToLLM).toContain('Feature details'); // File content
    expect(promptPassedToLLM).toContain('Agent: TestAgent'); // Team member info
  });
});
