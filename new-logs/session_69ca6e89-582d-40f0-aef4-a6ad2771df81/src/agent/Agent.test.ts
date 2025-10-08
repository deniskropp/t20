import { Agent, AgentSpec, PromptSpec } from '../agent/Agent';
import { System } from '../system/System';
import { MockLLM } from '../__mocks__/MockLLM';
import { mockSystemConfig, mockAgentSpecs, mockPrompts } from '../__mocks__/SystemMocks';
import { Plan, File } from '../custom_types';
import { ExecutionContext } from '../core/ExecutionContext';
import { Session } from '../core/Session';

// Mock the LLM class before importing modules that use it
jest.mock('../llm/LLM', () => {
  return {
    LLM: jest.fn().mockImplementation(() => {
      return {
        generateContent: jest.mocked(MockLLM.prototype.generateContent),
      };
    }),
    // Mock the factory method if it's used directly by System or Agent
    factory: jest.fn().mockImplementation(() => new MockLLM()),
  };
});

// Mock the read_file utility function if it's used directly by Orchestrator
jest.mock('../util/Util', () => ({
  read_file: jest.fn().mockReturnValue('Mocked file content for planning prompt.'),
}));

describe('Agent Core Components Testing', () => {
  let mockSystem: System;
  let mockSession: Session;
  let mockExecutionContext: ExecutionContext;
  let mockAgent: Agent;
  let mockOrchestratorSpec: AgentSpec;
  let mockPromptSpec: PromptSpec;

  beforeAll(() => {
    // Mock necessary dependencies for System setup
    // We need to mock the file system operations that System uses
    jest.spyOn(fs, 'readFileSync').mockImplementation((filePath) => {
      if (filePath.includes('runtime.yaml')) {
        return JSON.stringify(mockSystemConfig);
      }
      if (filePath.includes('.yaml') && filePath.includes('agents')) {
        const agentName = filePath.split('/').pop()?.replace('.yaml', '');
        const spec = mockAgentSpecs.find(s => s.name.toLowerCase() === agentSpec.name.toLowerCase());
        return JSON.stringify(spec);
      }
      if (filePath.includes('.txt') && filePath.includes('prompts')) {
        return mockPrompts[filePath.split('/').pop()!];
      }
      return '{}'; // Default empty content
    });
    jest.spyOn(glob, 'sync').mockReturnValue([
      '/path/to/config/runtime.yaml',
      '/path/to/agents/meta-ai.yaml',
      '/path/to/agents/prompt-engineer.yaml',
      '/path/to/prompts/meta-ai_instructions.txt',
      '/path/to/prompts/prompt-engineer_instructions.txt',
    ]);
    jest.spyOn(path, 'resolve').mockImplementation((...args) => args.join('/'));
    jest.spyOn(fs, 'existsSync').mockReturnValue(true);
    jest.spyOn(fs, 'readFileSync').mockReturnValue('mock content'); // Mock for file reading
    jest.spyOn(os, 'makedirs').mockImplementation(() => {}); // Mock directory creation
    jest.spyOn(JSON, 'stringify').mockReturnValue('{}'); // Mock JSON stringify
    jest.spyOn(yaml, 'load').mockReturnValue(mockSystemConfig);
  });

  beforeEach(async () => {
    // Reset mocks and re-initialize system for each test
    jest.clearAllMocks();

    // Re-mock file system interactions specific to System setup
    jest.spyOn(fs, 'readFileSync').mockImplementation((filePath: string | URL) => {
      const pathStr = typeof filePath === 'string' ? filePath : filePath.toString();
      if (pathStr.includes(RUNTIME_CONFIG_FILENAME)) {
        return JSON.stringify(mockSystemConfig);
      }
      if (pathStr.includes(AGENTS_DIR_NAME) && pathStr.endsWith('.yaml')) {
        const agentName = path.basename(pathStr, '.yaml');
        const spec = mockAgentSpecs.find(s => s.name.toLowerCase() === agentName);
        return JSON.stringify(spec);
      }
      if (pathStr.includes(PROMPTS_DIR_NAME) && pathStr.endsWith('.txt')) {
        const promptName = path.basename(pathStr);
        return mockPrompts[promptName] || 'Default prompt content';
      }
      return '{}';
    });
    jest.spyOn(glob, 'sync').mockReturnValue([
      '/path/to/config/runtime.yaml',
      '/path/to/agents/meta-ai.yaml',
      '/path/to/agents/prompt-engineer.yaml',
      '/path/to/prompts/meta-ai_instructions.txt',
      '/path/to/prompts/prompt-engineer_instructions.txt',
    ]);
    jest.spyOn(path, 'resolve').mockImplementation((...args) => args.join('/'));
    jest.spyOn(fs, 'existsSync').mockReturnValue(true);
    jest.spyOn(fs, 'readFileSync').mockReturnValue('mock content');
    jest.spyOn(os, 'makedirs').mockImplementation(() => {});
    jest.spyOn(JSON, 'stringify').mockReturnValue('{}');
    jest.spyOn(yaml, 'load').mockReturnValue(mockSystemConfig);

    // Initialize System and its dependencies
    mockSystem = new System('/mock/project/root', 'mock-model');
    await mockSystem.setup('Meta-AI'); // Specify orchestrator name

    mockSession = mockSystem['session'] as Session;
    mockOrchestratorSpec = mockAgentSpecs.find(spec => spec.name === 'Meta-AI')!;
    mockPromptSpec = mockPrompts['meta-ai_instructions.txt'];

    // Get the instantiated orchestrator
    const orchestratorAgent = mockSystem['agents'].find(a => a.name === 'Meta-AI') as Agent;
    mockAgent = new Agent('TestAgent', 'Tester', 'Test Goal', 'mock-model', 'Initial prompt');

    // Create a mock plan and context
    const mockPlan = new Plan({
      highLevelGoal: 'Test Goal',
      reasoning: 'Test Reasoning',
      roles: [{ title: 'Tester', purpose: 'To test things' }],
      tasks: [
        {
          id: 'T1',
          description: 'Test Task',
          role: 'Tester',
          agent: 'TestAgent',
          requires: [],
        },
      ],
    });
    mockExecutionContext = new ExecutionContext(mockSession, mockPlan);
  });

  afterAll(() => {
    jest.restoreAllMocks();
  });

  describe('Agent Instantiation and Initialization', () => {
    it('should instantiate agents correctly from specs', () => {
      expect(mockSystem.agents.length).toBeGreaterThan(0);
      const promptEngineer = mockSystem.agents.find(a => a.name === 'Prompt Engineer');
      expect(promptEngineer).toBeDefined();
      expect(promptEngineer?.role).toBe('Prompt Engineer');
      expect(promptEngineer?.goal).toBe('Refine prompts for agents.');
      expect(promptEngineer?.systemPrompt).toContain('You are a Prompt Engineer');
    });

    it('should correctly identify and set the orchestrator agent', () => {
      expect(mockSystem['orchestrator']).toBeDefined();
      expect(mockSystem['orchestrator']?.name).toBe('Meta-AI');
    });

    it('should handle missing orchestrator gracefully', async () => {
      // Remove orchestrator from mocks to test error handling
      const originalAgentSpecs = [...mockAgentSpecs];
      mockAgentSpecs.length = 0; // Clear specs
      jest.spyOn(glob, 'sync').mockReturnValue(['/path/to/config/runtime.yaml']); // Adjust glob mock
      jest.spyOn(fs, 'readFileSync').mockImplementation((filePath: string | URL) => {
        const pathStr = typeof filePath === 'string' ? filePath : filePath.toString();
        if (pathStr.includes(RUNTIME_CONFIG_FILENAME)) return JSON.stringify(mockSystemConfig);
        return '{}';
      });

      const system = new System('/mock/project/root', 'mock-model');
      await expect(system.setup('NonExistentOrchestrator')).rejects.toThrow('Orchestrator with name');
      mockAgentSpecs.length = 0; // Clear for next test
      mockAgentSpecs.push(...originalAgentSpecs); // Restore original specs
    });

    it('should update system prompt correctly', () => {
      const newPrompt = 'This is a new, updated prompt.';
      mockAgent.updateSystemPrompt(newPrompt);
      expect(mockAgent.systemPrompt).toBe(newPrompt);
    });
  });

  describe('Agent Task Execution', () => {
    it('should execute a task and return AgentOutput', async () => {
      const mockOutput = { output: 'Task completed successfully.', artifact: undefined, team: undefined, reasoning: 'Standard execution.' };
      const mockAgentOutput = new AgentOutput(mockOutput);

      // Mock LLM to return a valid AgentOutput
      const mockLLMInstance = mockSystem['agents'].find(a => a.name === 'MockLLM');
      (mockLLMInstance as any).llm.generateContent.mockResolvedValue(mockAgentOutput);

      // Mock context to have a current step
      const mockPlan = new Plan({ ...mockSystem.start('Test Goal').plan, tasks: [{ id: 'T1', description: 'A mock task', role: 'Tester', agent: 'MockLLM', requires: [] }] });
      const mockContext = new ExecutionContext(mockSession, mockPlan);
      mockContext.recordInitial('initial_files', [new File({ path: 'input.txt', content: 'initial content' })]);

      const result = await (mockAgent as any).executeTask(mockContext);

      expect(result).toBeDefined();
      expect(JSON.parse(result!)).toEqual(mockAgentOutput.toJSON());
      expect(mockLLMInstance.llm.generateContent).toHaveBeenCalled();
    });

    it('should handle LLM errors during task execution', async () => {
      const mockError = new Error('LLM generation failed');
      (mockAgent as any).llm.generateContent.mockRejectedValue(mockError);

      const mockPlan = new Plan({ ...mockSystem.start('Test Goal').plan, tasks: [{ id: 'T1', description: 'A mock task', role: 'Tester', agent: 'MockLLM', requires: [] }] });
      const mockContext = new ExecutionContext(mockSession, mockPlan);

      await expect((mockAgent as any).executeTask(mockContext)).rejects.toThrow('LLM generation failed');
    });

    it('should record artifacts correctly', async () => {
      const mockOutput = { output: 'Task completed with artifact.', artifact: { task: 'T1', files: [{ path: 'output.txt', content: 'File content' }] }, reasoning: 'Artifact created.' };
      const mockAgentOutput = new AgentOutput(mockOutput);
      (mockAgent as any).llm.generateContent.mockResolvedValue(mockAgentOutput);

      const mockPlan = new Plan({ ...mockSystem.start('Test Goal').plan, tasks: [{ id: 'T1', description: 'A mock task', role: 'Tester', agent: 'MockLLM', requires: [] }] });
      const mockContext = new ExecutionContext(mockSession, mockPlan);

      await (mockAgent as any).executeTask(mockContext);

      // Check if the artifact was added to the session
      const savedArtifact = mockSession.getArtifact('__1/__step_0_MockLLM_output.txt'); // Adjust key based on actual recording logic
      expect(savedArtifact).toBeDefined();
      expect(savedArtifact).toContain('File content');
    });

    it('should process team updates from AgentOutput', async () => {
      const newPrompt = 'Updated prompt for Prompt Engineer';
      const mockOutput = {
        output: 'Task completed with team update.',
        artifact: undefined,
        team: {
          notes: 'Prompt updated',
          prompts: [{ agent: 'Prompt Engineer', role: 'Prompt Engineer', systemPrompt: newPrompt }],
        },
        reasoning: 'Team update applied.',
      };
      const mockAgentOutput = new AgentOutput(mockOutput);
      (mockAgent as any).llm.generateContent.mockResolvedValue(mockAgentOutput);

      const mockPlan = new Plan({ ...mockSystem.start('Test Goal').plan, tasks: [{ id: 'T1', description: 'A mock task', role: 'Tester', agent: 'Meta-AI', requires: [] }] });
      const mockContext = new ExecutionContext(mockSession, mockPlan);

      await (mockAgent as any).executeTask(mockContext);

      // Verify that the Prompt Engineer's prompt was updated
      const promptEngineer = mockSystem.agents.find(a => a.name === 'Prompt Engineer');
      expect(promptEngineer?.systemPrompt).toBe(newPrompt);
    });
  });
});
