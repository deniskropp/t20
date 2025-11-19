(base) [einrichten@q3 ~/t20]$ aichat -f runtime 'extract 40 higher level shapes in the overall structure'
Here are 40 higher-level shapes extracted from the overall structure:

1.  **Core Runtime Components**: The fundamental building blocks of the application.
2.  **Agent Abstraction**: A base class or interface for all agents.
3.  **Orchestration Logic**: The central component responsible for planning and workflow management.
4.  **LLM Integration Layer**: A module to interface with various Large Language Models.
5.  **Task Management**: Mechanisms for defining, executing, and tracking tasks.
6.  **Workflow State Management**: How the system maintains and progresses through a workflow.
7.  **Artifact Handling**: Processes for creating, storing, and retrieving generated outputs.
8.  **Session Management**: Encapsulation of a single run or project context.
9.  **Configuration Loading**: Reading and parsing application settings.
10. **Prompt Management**: Loading and providing system prompts for agents.
11. **Agent Instantiation Factory**: A centralized way to create agent objects.
12. **Logging Setup and Configuration**: Establishing how the application logs events.
13. **Command-Line Interface (CLI) Parsing**: Handling user input from the command line.
14. **System Entry Point**: The main function that kicks off the application.
15. **Data Structure Definitions**: Pydantic models and dataclasses for consistent data representation.
16. **Execution Context**: The environment in which a task is executed.
17. **Team/Agent Collaboration**: Mechanisms for agents to interact with each other.
18. **LLM Provider Abstraction**: Differentiating between various LLM services (Gemini, Ollama, etc.).
19. **Dynamic Prompt Updates**: Ability for agents to modify their own prompts.
20. **File I/O Utilities**: Helper functions for reading and writing files.
21. **Error Handling and Logging**: Mechanisms for reporting and recording issues.
22. **Logging Formatter Customization**: Tailoring log output (e.g., with colors, JSON).
23. **Path Management**: Defining consistent directory and file paths.
24. **Agent Discovery/Lookup**: Finding agents based on criteria like role.
25. **Bootstrap Process**: The sequence of steps to initialize and run the system.
26. **Workflow Orchestration Loop**: The main loop that drives the execution of rounds and tasks.
27. **Task Dependency Management**: Handling prerequisites for task execution.
28. **Artifact Contextualization**: Providing relevant prior artifacts to agents.
29. **Agent Output Structuring**: Defining a standard format for agent responses.
30. **System Runtime Class**: An object to hold and manage the overall system state.
31. **Model-Specific LLM Wrappers**: Classes for each LLM provider (Gemini, Opi, Kimi, Mistral).
32. **Response Format Handling**: Managing different output formats from LLMs (text, JSON).
33. **Schema Validation for LLM Output**: Ensuring LLM responses conform to expected structures.
34. **Agent Specification Loading**: Reading agent definitions from configuration files.
35. **Prompt Template Loading**: Reading prompt content from text files.
36. **LLM Client Initialization**: Setting up connections to LLM services.
37. **Recursive Agent Instantiation**: Handling nested teams and dependencies.
38. **System Initialization Sequence**: The order of setup operations.
39. **Workflow Round Management**: Iterating through multiple execution cycles.
40. **Plan Generation and Validation**: Creating and ensuring the correctness of the execution plan.
