# Troubleshooting & FAQ

## Q: How do I handle missing LLM API keys?

A: Ensure that the necessary environment variables (e.g., `OPENAI_API_KEY`, `GOOGLE_API_KEY`) are set before running the system.

## Q: What should I do if an agent fails to execute a task?

A: Check the logs for detailed error messages. Ensure the agent's system prompt and the input context are correct. You may need to adjust the LLM parameters or the agent's logic.

## Q: How can I debug the workflow execution?

A: Set the logging level to `DEBUG` (`--log-level DEBUG`) to get more verbose output. Examine the artifacts generated at each step for detailed information.
