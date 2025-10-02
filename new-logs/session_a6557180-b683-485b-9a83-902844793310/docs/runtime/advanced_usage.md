# Advanced Usage & Tutorials

## Customizing Agents

Developers can create custom agent subclasses by inheriting from the `Agent` class and implementing specific logic for task execution or interacting with external services.

## Integrating New LLMs

The `LLM.factory` method allows for easy integration of new LLM providers. To add support for a new LLM, create a new class inheriting from `LLM` and implement the `generate_content` method.

## Advanced Planning

The `Orchestrator` can be customized to generate more sophisticated plans. This might involve modifying the planning prompt or implementing more complex plan validation logic.
