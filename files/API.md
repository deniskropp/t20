# T20 Multi-Agent Runtime API Documentation

This page documents the API specification for the T20 multi-agent runtime system, which enables interaction with a multi-agent orchestration platform designed to plan and execute complex workflows.

## Overview

The API provides two main endpoints:

- **POST /start**: Initializes the system with a high-level goal and optionally files or a pre-existing plan. It returns a detailed plan including roles, tasks, and team configuration.
- **POST /run**: Executes the workflow based on a provided plan, running the system for a specified number of rounds and returning results for each task.

## API Endpoints

### POST /start

- **Summary:** Initialize the system and create a plan.
- **Description:** This endpoint initializes the system, creates a plan for a high-level goal, and returns the plan.
- **Request Body:**
  - `high_level_goal` (string, required): The main goal to achieve.
  - `files` (array of strings, optional): List of file paths to be used in the task.
  - `plan_from` (string, optional): File path to read a pre-existing plan from.
  - `orchestrator` (string, optional, default "Meta-AI"): The name of the orchestrator to use.
  - `model` (string, optional, default "gemini-2.5-flash-lite"): The default LLM model to use.
- **Response:**
  - `200 OK`: Returns a JSON object containing the generated plan.

### POST /run

- **Summary:** Run the system's main workflow.
- **Description:** Executes the main workflow of the system based on a provided plan.
- **Request Body:**
  - `plan` (object, required): The plan object generated from `/start`.
  - `rounds` (integer, optional, default 1): Number of rounds to execute the workflow.
  - `files` (array of strings, optional): List of file paths to be used in the task.
- **Response:**
  - `200 OK`: Returns results of each task execution.
  - `400 Bad Request`: Error if system not initialized.

## Data Schemas

### StartRequest

- `high_level_goal` (string): The main goal to achieve.
- `files` (array of strings): Optional list of file paths.
- `plan_from` (string or null): Optional file path for a pre-existing plan.
- `orchestrator` (string): Orchestrator name, default "Meta-AI".
- `model` (string): Default LLM model, default "gemini-2.5-flash-lite".

### RunRequest

- `plan` (Plan object): The plan to execute.
- `rounds` (integer): Number of rounds to run, default 1.
- `files` (array of strings): Optional list of file paths.

### Plan

- `high_level_goal` (string): The main goal.
- `reasoning` (string): Explanation of plan structure.
- `roles` (array of Role objects): Roles involved.
- `tasks` (array of Task objects): Tasks to perform.
- `team` (Team object): Team notes and prompts.

### Task

- `id` (string): Unique task ID.
- `description` (string): Task details.
- `role` (string): Role responsible.
- `agent` (string): Assigned agent.
- `requires` (array of strings): Dependencies.

### Role

- `title` (string): Role or agent name.
- `purpose` (string): Role purpose or goal.

### Team

- `notes` (string): General notes or feedback.
- `prompts` (array of Prompt objects): Prompts for agents.

### Prompt

- `agent` (string): Agent name.
- `role` (string): Role context.
- `system_prompt` (string): Full system prompt text.

### AgentOutput

- `output` (string): Text response from agent.
- `artifact` (Artifact object): Output artifact.
- `team` (Team object): Team feedback.
- `reasoning` (string or null): Explanation of output.

### Artifact

- `task` (string): Task ID that produced artifact.
- `files` (array of File objects): Files produced.

### File

- `path` (string): File path or name.
- `content` (string): Full file content.

This page serves as a reference for developers and users of the T20 multi-agent runtime API, providing clear definitions of endpoints, request/response formats, and data structures.