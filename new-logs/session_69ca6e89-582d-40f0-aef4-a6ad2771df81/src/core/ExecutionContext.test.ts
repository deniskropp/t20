import { ExecutionContext } from './ExecutionContext';
import { Session } from '../core/Session';
import { Plan, Task, File, Artifact } from '../custom_types';
import { Agent } from '../agent/Agent';
import fs from 'fs';
import path from 'path';

// Mock dependencies
jest.mock('uuid', () => ({ v4: () => 'mock-uuid-context' }));
jest.mock('../core/Session');
jest.mock('fs');
jest.mock('path');

describe('ExecutionContext Core Component Testing', () => {
  let mockSession: Session;
  let mockPlan: Plan;
  let mockExecutionContext: ExecutionContext;
  let mockAgent: Agent;

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();

    // Mock Session
    mockSession = new Session([], '/mock/project/root');
    // Mock Agent
    mockAgent = new Agent('TestAgent', 'Tester', 'Test Goal', 'mock-model', 'System Prompt');

    // Mock Plan
    mockPlan = new Plan({
      highLevelGoal: 'Test High Level Goal',
      reasoning: 'Test Reasoning',
      roles: [{ title: 'Tester', purpose: 'To test' }],
      tasks: [
        new Task({ id: 'T1', description: 'First Task', role: 'Tester', agent: 'TestAgent', requires: [] }),
        new Task({ id: 'T2', description: 'Second Task', role: 'Tester', agent: 'TestAgent', requires: ['T1'] }),
      ],
    });

    // Mock file system operations used by Session.addArtifact
    (path.join as jest.Mock).mockImplementation((...args) => args.join('/'));
    (fs.makedirs as jest.Mock).mockImplementation(() => {});
    (fs.writeFile as jest.Mock).mockImplementation((filePath, data, options, callback) => callback(null));

    // Initialize ExecutionContext
    mockExecutionContext = new ExecutionContext(mockSession, mockPlan);
  });

  it('should initialize correctly', () => {
    expect(mockExecutionContext.session).toBe(mockSession);
    expect(mockExecutionContext.plan).toBe(mockPlan);
    expect(mockExecutionContext.stepIndex).toBe(0);
    expect(mockExecutionContext.roundNum).toBe(1);
    expect(mockExecutionContext.items).toEqual({});
  });

  it('should advance stepIndex using nextStep()', () => {
    expect(mockExecutionContext.stepIndex).toBe(0);
    mockExecutionContext.nextStep();
    expect(mockExecutionContext.stepIndex).toBe(1);
    mockExecutionContext.nextStep();
    expect(mockExecutionContext.stepIndex).toBe(2);
  });

  it('should reset stepIndex using reset()', () => {
    mockExecutionContext.stepIndex = 2;
    mockExecutionContext.reset();
    expect(mockExecutionContext.stepIndex).toBe(0);
  });

  it('should return the current step using currentStep()', () => {
    const currentStep = mockExecutionContext.currentStep();
    expect(currentStep).toEqual(mockPlan.tasks[0]);
    mockExecutionContext.nextStep();
    const nextStep = mockExecutionContext.currentStep();
    expect(nextStep).toEqual(mockPlan.tasks[1]);
  });

  it('should throw error if stepIndex is out of bounds in currentStep()', () => {
    mockExecutionContext.stepIndex = mockPlan.tasks.length; // Set index beyond the last task
    expect(() => mockExecutionContext.currentStep()).toThrow('Step index is out of bounds');
  });

  it('should record artifacts using recordArtifact()', async () => {
    const key = 'agent_output';
    const value = 'Some output';
    // Mock Session.addArtifact to capture calls
    const addArtifactSpy = jest.spyOn(mockSession, 'addArtifact');

    await mockExecutionContext.recordArtifact(key, value, true);

    // Check if artifact was added to session
    expect(addArtifactSpy).toHaveBeenCalledWith(expect.stringContaining(key), value);
    // Check if artifact was added to context items memory
    expect(mockExecutionContext.items).toHaveProperty(expect.stringContaining(key));
    expect(mockExecutionContext.items[expect.stringContaining(key)].content).toBe(value);
    expect(mockExecutionContext.items[expect.stringContaining(key)].step.id).toBe('T1');
  });

  it('should record initial artifacts using recordInitial()', () => {
    const key = 'initial_file.txt';
    const value = 'Initial file content';
    const initialFile = new File({ path: key, content: value });
    mockExecutionContext.recordInitial(key, initialFile);

    // Check if artifact was added to context items memory
    expect(mockExecutionContext.items).toHaveProperty(key);
    expect(mockExecutionContext.items[key].content).toBe(initialFile);
    expect(mockExecutionContext.items[key].step.id).toBe('initial');
    expect(mockExecutionContext.items[key].step.description).toBe('Initial files provided by the user');
  });

  it('should retrieve initial files using getInitialFiles()', () => {
    const initialFile1 = new File({ path: 'input1.txt', content: 'Content 1' });
    const initialFile2 = new File({ path: 'input2.txt', content: 'Content 2' });
    mockExecutionContext.recordInitial('initial_files', [initialFile1, initialFile2]);

    const retrievedFiles = mockExecutionContext.getInitialFiles();
    expect(retrievedFiles).toEqual([initialFile1, initialFile2]);
  });

  it('should return null from getInitialFiles() if not found', () => {
    const retrievedFiles = mockExecutionContext.getInitialFiles();
    expect(retrievedFiles).toBeNull();
  });

  it('should return empty array from getInitialFiles() if initial files is empty', () => {
    mockExecutionContext.recordInitial('initial_files', []);
    const retrievedFiles = mockExecutionContext.getInitialFiles();
    expect(retrievedFiles).toEqual([]);
  });
});
