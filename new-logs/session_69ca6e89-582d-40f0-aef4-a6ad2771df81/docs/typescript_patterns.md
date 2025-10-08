# SOTA TypeScript/Node.js Patterns for Runtime System

This document outlines State-Of-The-Art (SOTA) TypeScript and Node.js implementation patterns and best practices for recreating the runtime system's functionalities, based on the identified Task Agnostic Steps (TAS).

## 1. System Initialization and Configuration

*   **Load System Configuration**: Use libraries like `dotenv` for environment variables and `yaml` or `json` for configuration files. For complex configurations, consider using `class-validator` for validation.
    *   **Example**: `import yaml from 'yaml'; const config = yaml.parse(fs.readFileSync('config/runtime.yaml', 'utf-8'));`
*   **Discover and Load Agents/Prompts**: Employ dynamic module loading using `fs.readdirSync` and `import()` or `require()`. Use a factory pattern for instantiating agents.
    *   **Pattern**: Factory Pattern, Dynamic Module Loading.
*   **Instantiate Agents**: Leverage classes and interfaces for defining agent structures. Use dependency injection (DI) for managing LLM clients and other dependencies.
    *   **TypeScript Feature**: Classes, Interfaces, Generics.
    *   **Pattern**: Dependency Injection (e.g., using `InversifyJS` or manual injection).
*   **Initialize LLM Clients**: Create an abstract `LLM` class with concrete implementations for different providers (e.g., `OpenAI`, `Gemini`, `Ollama`). Use a factory method for easy instantiation.
    *   **TypeScript Feature**: Abstract Classes, Interfaces, Factory Pattern.
    *   **Best Practice**: Abstract away provider-specific details.
*   **Set Up Logging**: Utilize libraries like `winston` or `pino` for robust logging. `pino` is known for its performance and JSON logging capabilities, suitable for structured output.
    *   **Best Practice**: Use structured logging (JSON) for easier parsing and analysis.

## 2. Workflow Planning

*   **Receive High-Level Goal**: Standard function parameter.
*   **Describe Available Agents and Roles**: Pass agent metadata (name, role, goal) as an object or array of objects to the planning agent's prompt.
*   **Generate Plan**: The LLM interaction follows the `LLM` abstraction. The prompt engineering will be crucial here, similar to the Python version.
    *   **TypeScript Feature**: Interfaces for `Plan`, `Task`, `Role`, `Agent`.
*   **Validate Plan**: Use Pydantic (via `zod` or `class-validator` in TS) to define and validate the `Plan` schema.
    *   **TypeScript Feature**: Interfaces or Classes with Validation (e.g., `zod`).
*   **Record Initial Plan**: Use the `Session`'s artifact storage mechanism.

## 3. Workflow Execution

*   **Initialize Session**: A `Session` class to manage state, potentially using a class with methods for artifact storage (e.g., using `fs` module for file persistence).
    *   **TypeScript Feature**: Classes, `async/await` for I/O operations.
*   **Initialize Execution Context**: A `ExecutionContext` class to hold `Session`, `Plan`, current step, round number, and artifacts (e.g., `Map<string, ContextItem>`).
    *   **TypeScript Feature**: Classes, `Map` for storing context items.
*   **Record Initial Artifacts**: Methods within `ExecutionContext` or `Session` to save files using the `fs` module.
    *   **Best Practice**: Use `async/await` for all file I/O operations.
*   **Iterate Through Workflow Rounds/Tasks**: Standard `for` loops and `while` loops. Use `async/await` for asynchronous agent task execution.
*   **Identify and Select Agent**: A helper function or method to find an agent by name or role, similar to `find_agent_by_role`.
*   **Prepare Task Prompt**: String interpolation or template literals for constructing prompts.
*   **Execute Task**: Agent's `executeTask` method will be `async` to handle potential LLM calls.
    *   **TypeScript Feature**: `async/await`.
*   **Agent Task Execution**: Classes implementing an `Agent` interface.
*   **LLM Interaction**: Calls to the abstracted `LLM` service.
*   **Parse LLM Response**: Use `JSON.parse()` for JSON responses. Employ `try-catch` blocks for error handling. Use Pydantic models (or `zod` schemas) for validation.
    *   **TypeScript Feature**: `try-catch`, `JSON.parse()`.
*   **Handle Agent Output**: Parse the `AgentOutput` structure (defined as an interface or class).
    *   **TypeScript Feature**: Interfaces, Classes.
*   **Record Task Result**: Use `Session` methods for artifact storage.
*   **Update Agent Prompts**: Methods on the `Agent` class or a central `AgentManager` to update prompts.
*   **Advance Execution Context**: Incrementing counters or updating state within `ExecutionContext`.
*   **Manage Artifacts**: `fs` module operations within `Session` or `ExecutionContext`.

## 4. Agent Communication and State Management

*   **Agent Lifecycle Management**: Defined by class methods (`constructor`, `executeTask`, etc.).
*   **Contextual Information Sharing**: Pass `ExecutionContext` objects to agent methods.
*   **Artifact Storage and Retrieval**: Use `fs` operations within `Session`.
*   **Session Management**: The `Session` class will manage its state.
*   **System Prompt Updates**: Methods on `Agent` objects or a central `AgentRegistry`.
    *   **Best Practice**: Use event emitters or callbacks for prompt updates if real-time propagation is needed.

## 5. LLM Interaction Abstraction

*   **Abstract LLM Interface**: Define an `abstract class LLM` with an `abstract generateContent` method.
    *   **TypeScript Feature**: `abstract class`, `abstract method`.
*   **LLM Model Selection**: Factory pattern as described in Section 1.
*   **Content Generation**: Implement `async` methods in concrete LLM classes.
*   **Response Formatting**: Use `JSON.stringify()` and `JSON.parse()`. Leverage validation libraries like `zod` or `class-validator` to ensure responses conform to expected schemas (e.g., `AgentOutput`).
    *   **TypeScript Feature**: `async/await`, `try-catch`, `JSON.stringify/parse`.
    *   **Best Practice**: Implement robust error handling and schema validation for LLM responses.

## 6. Error Handling and Resilience

*   **Exception Handling**: Use `try-catch` blocks extensively, especially around I/O operations and LLM calls. Define custom error types for better error management.
    *   **TypeScript Feature**: `try-catch`, custom error classes.
*   **LLM Call Retries**: Implement retry logic using libraries like `axios-retry` (if using `axios` for HTTP calls) or custom promise-based retry functions.
    *   **Best Practice**: Exponential backoff for retries.
*   **Fallback Mechanisms**: Implement checks for agent availability and provide default agents or behaviors.

## Key TypeScript/Node.js Considerations:

*   **Asynchronous Operations**: Node.js is inherently asynchronous. Use `async/await` extensively for I/O, network requests (LLM calls), and any operation that might block the event loop.
*   **Type Safety**: Leverage TypeScript's static typing to catch errors at compile time. Define interfaces and types for all data structures (Agents, Plans, Tasks, Artifacts, AgentOutput, etc.).
*   **Modularity**: Structure the project into clear modules (e.g., `agents`, `core`, `llm`, `utils`, `prompts`).
*   **Dependency Management**: Use `npm` or `yarn` for package management. Consider a monorepo structure (e.g., using Lerna or Nx) if the project grows complex.
*   **Testing**: Employ testing frameworks like `Jest` or `Mocha` with `Chai` for unit and integration tests. Mock external dependencies (like LLM APIs) for reliable testing.
