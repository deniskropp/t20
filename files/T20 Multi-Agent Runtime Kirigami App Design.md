# T20 Multi-Agent Runtime: Kirigami App Design

This guide outlines a detailed design for a Kirigami app that interfaces with the T20 Multi-Agent Runtime API to initialize plans and run workflows.

## App Overview

The Kirigami app provides a user-friendly interface to interact with the T20 multi-agent system. It allows users to input high-level goals, manage files, view generated plans, execute workflows, and review results.

## Key Features

- Input form for high-level goal and optional parameters
- File management interface to upload/select files
- Display of generated plans with roles, tasks, and reasoning
- Workflow execution controls with progress and results display
- Error handling and system status feedback

## UI Components

### 1. Main Page

- Header with app title and navigation drawer
- Central content area with stacked views:
  - Goal Input View
  - Plan Display View
  - Workflow Execution View
  - Results View

### 2. Goal Input View

- TextField for entering the high-level goal (required)
- Optional fields:
  - File selector (multi-select)
  - Orchestrator dropdown (default: "Meta-AI")
  - Model dropdown (default: "gemini-2.5-flash-lite")
- Submit button to call `/start` endpoint
- Validation and error messages

### 3. Plan Display View

- Shows plan summary:
  - High-level goal
  - Reasoning
- List of Roles with titles and purposes
- List of Tasks with IDs, descriptions, roles, agents, and dependencies
- Button to proceed to workflow execution

### 4. Workflow Execution View

- Display current workflow status and progress
- Button to start running the workflow (`/run` endpoint)
- Option to specify number of rounds
- Display of each step's output as it completes
- Error messages if system not initialized or other failures

### 5. Results View

- Summary of workflow results
- Detailed output per task step
- Option to export results or save artifacts

## Navigation Flow

1. User enters goal and optional parameters, submits form.
2. App calls `/start`, receives plan.
3. Plan Display View shows plan details.
4. User proceeds to Workflow Execution View.
5. User starts workflow; app calls `/run`.
6. Results View displays outputs and artifacts.

## Error Handling

- Validate inputs before API calls.
- Show clear messages for network errors or API failures.
- Allow retrying failed operations.

## Styling and Theming

- Use Kirigami's native theming for consistency.
- Responsive layout for desktop and mobile.

This design provides a comprehensive foundation for building a Kirigami app that leverages the T20 Multi-Agent Runtime API effectively.

# T20 Multi-Agent Runtime API Documentation

This page provides an overview and details of the T20 Multi-Agent Runtime API based on the provided OpenAPI specification.

## Overview

The T20 Multi-Agent Runtime API allows interaction with a multi-agent system designed to orchestrate and execute complex workflows through defined plans and roles.

## API Endpoints

### POST /start

- **Summary:** Initialize the system and create a plan.
- **Description:** Initializes the system, creates a plan for a high-level goal, and returns the plan.
- **Request Body:** JSON object with:
  - `high_level_goal` (string, required): The main goal to achieve.
  - `files` (array of strings, optional): List of file paths to be used in the task.
  - `plan_from` (string, optional): File path to read a pre-existing plan from.
  - `orchestrator` (string, optional, default "Meta-AI"): The orchestrator to use.
  - `model` (string, optional, default "gemini-2.5-flash-lite"): The default LLM model to use.
- **Response:** On success, returns a JSON object containing the created plan.

### POST /run

- **Summary:** Run the system's main workflow.
- **Description:** Executes the main workflow based on a provided plan.
- **Request Body:** JSON object with:
  - `plan` (object, required): The plan to execute.
  - `rounds` (integer, optional, default 1): Number of rounds to execute.
  - `files` (array of strings, optional): List of file paths to be used in the task.
- **Response:** On success, returns results of each step with outputs. Returns error if system not initialized.

## Key Components

### Plan

- `high_level_goal`: The main goal the plan aims to achieve.
- `reasoning`: Explanation of the plan's structure and strategy.
- `roles`: Array of roles involved in the plan.
- `tasks`: Array of tasks to be performed.
- `team`: Team notes and prompts.

### Task

- `id`: Unique identifier.
- `description`: Detailed task description.
- `role`: Role responsible.
- `agent`: Assigned agent.
- `requires`: Dependencies by task IDs.

### Role

- `title`: Role or agent name.
- `purpose`: Role's purpose or goal.

### Team

- `notes`: General notes or feedback.
- `prompts`: Array of prompts for agents.

### AgentOutput

- `output`: Text response from agent.
- `artifact`: Associated artifact files.
- `team`: Team feedback.
- `reasoning`: Explanation of output.

## Usage

To use the API, first call `/start` with a high-level goal to generate a plan. Then call `/run` with the plan to execute the workflow and receive results.

