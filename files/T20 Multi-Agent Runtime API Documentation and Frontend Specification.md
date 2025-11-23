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

# Progressive SPA Web Frontend Specification

This section outlines the specification for a progressive Single Page Application (SPA) frontend designed to interact with the T20 Multi-Agent Runtime API. The frontend aims to provide a responsive, dynamic, and user-friendly interface for managing multi-agent workflows.

## 1. Architecture Overview

- **Framework:** Use a modern JavaScript framework such as React, [Vue.js](https://Vue.js), or Svelte for component-based UI development.
- **Routing:** Implement client-side routing to enable seamless navigation without full page reloads.
- **State Management:** Utilize a state management library (e.g., Redux, Vuex, or Zustand) to manage application state, including plans, tasks, and execution results.
- **API Integration:** Communicate with the T20 API endpoints (`/start` and `/run`) via asynchronous HTTP requests (e.g., using Fetch API or Axios).
- **Progressive Enhancement:** Ensure the app works with JavaScript disabled by providing server-side rendered fallback pages or minimal functionality.

## 2. Key Features

- **Goal Initialization:** Form to input a high-level goal and optional files, triggering the `/start` endpoint to generate a plan.
- **Plan Visualization:** Display the generated plan with roles, tasks, dependencies, and team information in an interactive, expandable UI.
- **Workflow Execution:** Interface to run the plan through the `/run` endpoint, specifying rounds and monitoring task execution results.
- **Real-time Updates:** Use WebSockets or polling to update task statuses and results dynamically.
- **Error Handling:** Gracefully handle API errors, including system initialization errors and network issues.
- **File Management:** Upload and manage files associated with tasks and plans.

## 3. UI Components

- **Header:** Branding, navigation links, and user status.
- **Goal Input Form:** Fields for high-level goal, file uploads, orchestrator, and model selection.
- **Plan Viewer:** Tree or graph view of roles, tasks, and dependencies with detailed task descriptions.
- **Execution Console:** Controls to start, pause, and stop workflow runs; display logs and results.
- **File Manager:** Upload, list, and preview files used in workflows.
- **Notifications:** Toast messages or alerts for success, warnings, and errors.

## 4. Performance and Accessibility

- **Lazy Loading:** Load components and data on demand to improve initial load times.
- **Responsive Design:** Ensure usability across devices and screen sizes.
- **Accessibility:** Follow WCAG guidelines for keyboard navigation, screen reader support, and color contrast.

## 5. Security Considerations

- **Authentication:** Implement user authentication and authorization if needed.
- **Input Validation:** Sanitize and validate all user inputs.
- **Secure API Calls:** Use HTTPS and handle tokens securely.

## 6. Development and Deployment

- **Build Tools:** Use modern build tools like Vite, Webpack, or Parcel.
- **Testing:** Include unit, integration, and end-to-end tests.
- **CI/CD:** Automate builds, tests, and deployments.

## 7. Example User Flow

1. User lands on the homepage and inputs a high-level goal with optional file uploads.
2. The frontend calls `/start` to generate a plan and displays it in the Plan Viewer.
3. User reviews the plan, expands task details, and optionally modifies inputs.
4. User initiates workflow execution via the Execution Console.
5. The frontend polls or listens for real-time updates, displaying task progress and results.
6. User can upload additional files or download artifacts from completed tasks.
7. Notifications inform the user of success, errors, or important events.

## 8. Example Technology Stack

- **Frontend Framework:** React with TypeScript
- **State Management:** Redux Toolkit
- **Routing:** React Router
- **HTTP Client:** Axios
- **Real-time Communication:** Socket.IO or native WebSocket API
- **Build Tool:** Vite
- **Testing:** Jest, React Testing Library, Cypress

## 9. User Interaction Flows

This section describes detailed user interaction flows for the SPA frontend to guide development and ensure a smooth user experience.

### Flow 1: Initialize and Create Plan

1. User navigates to the homepage.
2. User enters a high-level goal in the input form.
3. User optionally uploads files and selects orchestrator and model.
4. User clicks "Create Plan" button.
5. Frontend validates inputs and sends a POST request to `/start` endpoint.
6. While waiting, a loading spinner or progress indicator is shown.
7. On success, the plan data is received and stored in state.
8. The Plan Viewer component renders the plan with roles, tasks, and dependencies.
9. Notifications inform the user of success or any warnings.

### Flow 2: Review and Modify Plan

1. User expands tasks or roles in the Plan Viewer to see details.
2. User can add or remove files related to the plan via the File Manager.
3. User edits optional parameters like orchestrator or model if UI allows.
4. Changes update the local state but do not immediately trigger API calls.
5. User can save changes or re-run the plan creation if needed.

### Flow 3: Execute Workflow

1. User navigates to the Execution Console.
2. User selects the number of rounds to run.
3. User clicks "Run Workflow" button.
4. Frontend sends a POST request to `/run` with the current plan and rounds.
5. Execution Console shows real-time logs and task statuses.
6. Frontend uses WebSocket or polling to receive updates.
7. User can pause or stop execution if controls are provided.
8. On completion, results and artifacts are displayed.
9. Notifications inform the user of completion or errors.

### Flow 4: File Management

1. User opens the File Manager panel.
2. User uploads new files or deletes existing ones.
3. Uploaded files are validated and added to the current task or plan context.
4. Files can be previewed or downloaded.
5. Changes reflect immediately in the UI and update the state.

### Flow 5: Error Handling and Notifications

1. Any API error triggers an error notification with details.
2. User can retry failed actions from notifications or UI controls.
3. Validation errors highlight the relevant input fields.
4. Network issues show a persistent warning until resolved.

These interaction flows ensure clarity and responsiveness, guiding users through the multi-agent runtime system's lifecycle from goal input to workflow execution and file management.