import { Session } from './Session';
import { Plan, File, Task } from '../custom_types';
import { Agent } from '../agent/Agent';
import { ExecutionContext } from './ExecutionContext';
import fs from 'fs';
import path from 'path';

// Mock dependencies
jest.mock('uuid', () => ({ v4: () => 'mock-uuid-123' }));
jest.mock('fs');
jest.mock('path');

describe('Session Core Component Testing', () => {
  let mockSession: Session;
  let mockAgent: Agent;
  let mockPlan: Plan;
  let mockExecutionContext: ExecutionContext;

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();

    // Mock Agent and Plan for Session initialization
    mockAgent = new Agent('TestAgent', 'Tester', 'Test Goal', 'mock-model', 'System Prompt');
    mockPlan = new Plan({
      highLevelGoal: 'Test Goal',
      reasoning: 'Test Reasoning',
      roles: [{ title: 'Tester', purpose: 'To test things' }],
      tasks: [
        new Task({ id: 'T1', description: 'Task 1', role: 'Tester', agent: 'TestAgent', requires: [] }),
      ],
    });

    // Mock dependencies for Session and ExecutionContext
    (path.join as jest.Mock).mockImplementation((...args) => args.join('/'));
    (fs.makedirs as jest.Mock).mockImplementation(() => {});

    mockSession = new Session([mockAgent], '/mock/project/root');
    mockExecutionContext = new ExecutionContext(mockSession, mockPlan);
  });

  it('should initialize with a unique session ID and directory', () => {
    expect(mockSession.sessionId).toBe('session_mock-uuid-123');
    expect(mockSession.sessionDir).toBe('/mock/project/root/sessions/session_mock-uuid-123');
    expect(fs.makedirs).toHaveBeenCalledWith(mockSession.sessionDir, {
      recursive: true,
    });
  });

  it('should add and retrieve string artifacts', async () => {
    const artifactName = 'test_string_artifact.txt';
    const artifactContent = 'This is a test string.';
    // Mock fs.promises.writeFile and fs.promises.readFile
    (fs.promises.writeFile as jest.Mock).mockImplementation((filePath, content, options) => Promise.resolve());
    (fs.promises.readFile as jest.Mock).mockImplementation((filePath, options) => Promise.resolve(artifactContent));
    (fs.promises.mkdir as jest.Mock).mockImplementation(() => Promise.resolve());

    await mockSession.addArtifact(artifactName, artifactContent);
    expect(fs.promises.writeFile).toHaveBeenCalledWith(expect.stringContaining(artifactName), artifactContent, 'utf-8');

    const retrievedContent = await mockSession.getArtifact(artifactName);
    expect(retrievedContent).toBe(artifactContent);
    expect(fs.promises.readFile).toHaveBeenCalledWith(expect.stringContaining(artifactName), 'utf-8');
  });

  it('should add and retrieve JSON artifacts', async () => {
    const artifactName = 'test_json_artifact.json';
    const artifactContent = { key: 'value', number: 123 };
    (fs.promises.writeFile as jest.Mock).mockImplementation((filePath, content, options) => Promise.resolve());
    (fs.promises.readFile as jest.Mock).mockImplementation((filePath, options) => Promise.resolve(JSON.stringify(artifactContent)));
    (fs.promises.mkdir as jest.Mock).mockImplementation(() => Promise.resolve());

    await mockSession.addArtifact(artifactName, artifactContent);
    expect(fs.promises.writeFile).toHaveBeenCalledWith(expect.stringContaining(artifactName), JSON.stringify(artifactContent, null, 2), 'utf-8');

    const retrievedContent = await mockSession.getArtifact(artifactName);
    expect(retrievedContent).toEqual(artifactContent);
  });

  it('should handle errors when getting non-existent artifacts', async () => {
    const artifactName = 'non_existent_artifact.txt';
    const error = new Error('File not found') as NodeJS.ErrnoException;
    error.code = 'ENOENT';
    (fs.promises.readFile as jest.Mock).mockImplementation(() => Promise.reject(error));

    const retrievedContent = await mockSession.getArtifact(artifactName);
    expect(retrievedContent).toBeNull();
  });

  it('should handle errors during artifact saving', async () => {
    const artifactName = 'save_error_artifact.txt';
    const artifactContent = 'Content';
    const error = new Error('Write error');
    (fs.promises.writeFile as jest.Mock).mockImplementation(() => Promise.reject(error));
    (fs.promises.mkdir as jest.Mock).mockImplementation(() => Promise.resolve());

    // Suppress console error for this specific test as it's expected
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    await mockSession.addArtifact(artifactName, artifactContent);
    expect(consoleErrorSpy).toHaveBeenCalled();
    consoleErrorSpy.mockRestore();
  });

  // Integration test: Recording and retrieving artifacts through ExecutionContext
  it('should record and retrieve artifacts via ExecutionContext', async () => {
    const artifactKey = 'context_artifact.txt';
    const artifactValue = 'Contextual data';
    // Mock Session.addArtifact to capture calls
    const addArtifactSpy = jest.spyOn(mockSession, 'addArtifact');
    // Mock Session.getArtifact
    const getArtifactSpy = jest.spyOn(mockSession, 'getArtifact').mockResolvedValue(artifactValue);

    await mockExecutionContext.recordArtifact(artifactKey, artifactValue, true);

    // Check if addArtifact was called on session
    expect(addArtifactSpy).toHaveBeenCalled();
    // Check if the artifact was added to context items memory
    expect(mockExecutionContext.items).toHaveProperty(expect.stringContaining(artifactKey));
    expect(mockExecutionContext.items[expect.stringContaining(artifactKey)].content).toBe(artifactValue);

    const retrievedValue = await mockSession.getArtifact(artifactKey); // Use original key for getArtifact
    expect(retrievedValue).toBe(artifactValue);
    expect(getArtifactSpy).toHaveBeenCalledWith(expect.stringContaining(artifactKey));
  });

  it('should record initial artifacts correctly', () => {
    const initialKey = 'initial_data.json';
    const initialValue = { data: 'some initial data' };
    mockExecutionContext.recordInitial(initialKey, initialValue);

    // Check if it's stored in context items
    expect(mockExecutionContext.items).toHaveProperty(initialKey);
    expect(mockExecutionContext.items[initialKey].content).toEqual(initialValue);
    expect(mockExecutionContext.items[initialKey].step.id).toBe('initial');
  });
});
