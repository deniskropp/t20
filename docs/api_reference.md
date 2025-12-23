# T20SDK API Reference

## Core (`t20sdk.core`)

The core module contains the runtime engine and base classes.

### System
`t20sdk.core.system.System`
The main entry point for the T20 system. Handles configuration, agent loading, and workflow execution.

### Session
`t20sdk.core.core.Session`
Manages the runtime state, including artifacts and agent context.

### ExecutionContext
`t20sdk.core.core.ExecutionContext`
Holds the execution context for a task, including the plan and shared artifacts.

### Agent
`t20sdk.core.agent.Agent`
Base class for all agents. Defines the interface for task execution and LLM interaction.

### Orchestrator
`t20sdk.core.orchestrator.Orchestrator`
A specialized agent responsible for generating plans and managing the workflow.

## Language (`t20sdk.lang`)

### KickLangParser
`t20sdk.core.parsing.KickLangParser`
Parses KickLang formatted plans into runtime `Plan` objects.

## Data Models (`t20sdk.data`)

### Plan
`t20sdk.core.custom_types.Plan`
Represents a structured plan with goals, roles, and tasks.

### Task
`t20sdk.core.custom_types.Task`
A single unit of work in a plan.

### AgentOutput
`t20sdk.core.custom_types.AgentOutput`
The structured response from an agent.

## Graph (`t20sdk.graph`)

*Documentation coming soon.*
