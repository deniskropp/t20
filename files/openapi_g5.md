# API Specification (minimized) - Generation 6

This document represents the next six generations of the API specification, building upon the original `openapi_g2.md`.

**Generation 2: Human-in-the-Loop:** Adds capabilities for workflows to pause and request human input, enabling more interactive and supervised processes.

**Generation 3: Advanced Triggering and Event-Driven Workflows:** Introduces event-based triggers and advanced scheduling for workflows.

**Generation 4: Workflow Definition and Versioning:** Introduces a dedicated API for managing workflow definitions, allowing for their creation, updating, and versioning. This promotes reusability and better lifecycle management of workflows.

**Generation 5: Collaboration and Access Control:** Adds features for sharing workflows and managing access control, enabling team-based development and secure collaboration.

**Generation 6: Extensibility with Plugins:** This generation introduces a plugin system, allowing developers to extend workflow capabilities with custom logic and integrations.

## KickLang API Definition

```kicklang
`<<START>>` POST `/start`
  `high_level_goal` (string, optional)
  `files` (array, optional)
  `plan_from` (string, optional)
  `orchestrator` (string, optional, default: "Meta-AI")
  `model` (string, optional, default: "gemini-2.5-flash-lite")
  `definitionId` (string, optional)
`<<RUN>>` POST `/runs/{jobId}`
  `jobId` (string, path, required)
  `plan` (object, required)
  `rounds` (integer, optional, default: 1)
  `files` (array, optional)
`<<GET RUN STATUS>>` GET `/runs/{jobId}`
  `jobId` (string, path, required)
`<<STREAM>>` GET `/runs/{jobId}/stream`
  `jobId` (string, path, required)
`<<CONTROL>>` POST `/runs/{jobId}/control`
  `jobId` (string, path, required)
  `command` (string, enum: ["pause", "resume", "cancel"], required)
`<<HUMAN INPUT>>` POST `/runs/{jobId}/human-input`
  `jobId` (string, path, required)
  `input` (object, required)
`<<REGISTER WEBHOOK>>` POST `/webhooks`
  `url` (string, url, required)
  `events` (array, optional, default: ["workflow_completed", "workflow_failed"])
  `secret` (string, optional)
`<<LIST WEBHOOKS>>` GET `/webhooks`
`<<UNREGISTER WEBHOOK>>` DELETE `/webhooks/{webhookId}`
  `webhookId` (string, path, required)
`<<HISTORY RUNS>>` GET `/history/runs`
  `limit` (integer, query, optional, default: 20)
  `offset` (integer, query, optional, default: 0)
  `status` (string, query, optional, enum: ["pending", "running", "completed", "failed", "paused", "paused_for_input"])
  `sortBy` (string, query, optional, default: "startTime")
  `sortOrder` (string, query, optional, enum: ["asc", "desc"], default: "desc")
`<<HISTORY RUN STATE>>` GET `/history/runs/{jobId}/state`
  `jobId` (string, path, required)

// Generation 3: Advanced Triggering and Event-Driven Workflows
`<<CREATE TRIGGER>>` POST `/triggers`
  `name` (string, required)
  `description` (string, optional)
  `workflowId` (string, required)
  `type` (string, enum: ["schedule", "event"], required)
  `config` (object, required)
`<<LIST TRIGGERS>>` GET `/triggers`
`<<GET TRIGGER>>` GET `/triggers/{triggerId}`
  `triggerId` (string, path, required)
`<<UPDATE TRIGGER>>` PUT `/triggers/{triggerId}`
  `triggerId` (string, path, required)
  `name` (string, optional)
  `description` (string, optional)
  `config` (object, optional)
  `enabled` (boolean, optional)
`<<DELETE TRIGGER>>` DELETE `/triggers/{triggerId}`
  `triggerId` (string, path, required)

// Generation 4: Workflow Definition and Versioning
`<<CREATE DEFINITION>>` POST `/definitions`
  `name` (string, required)
  `description` (string, optional)
  `definition` (object, required)
`<<LIST DEFINITIONS>>` GET `/definitions`
`<<GET DEFINITION>>` GET `/definitions/{definitionId}`
  `definitionId` (string, path, required)
`<<UPDATE DEFINITION>>` PUT `/definitions/{definitionId}`
  `definitionId` (string, path, required)
  `name` (string, optional)
  `description` (string, optional)
  `definition` (object, optional)
`<<DELETE DEFINITION>>` DELETE `/definitions/{definitionId}`
  `definitionId` (string, path, required)
`<<CREATE DEFINITION VERSION>>` POST `/definitions/{definitionId}/versions`
    `definitionId` (string, path, required)
    `description` (string, optional)
    `definition` (object, required)
`<<LIST DEFINITION VERSIONS>>` GET `/definitions/{definitionId}/versions`
    `definitionId` (string, path, required)

// Generation 5: Collaboration and Access Control
`<<SHARE WORKFLOW>>` POST `/workflows/{workflowId}/share`
  `workflowId` (string, path, required)
  `userId` (string, optional)
  `teamId` (string, optional)
  `role` (string, enum: ["viewer", "editor", "executor"], required)
`<<GET WORKFLOW PERMISSIONS>>` GET `/workflows/{workflowId}/permissions`
  `workflowId` (string, path, required)
`<<UPDATE WORKFLOW PERMISSIONS>>` PUT `/workflows/{workflowId}/permissions`
  `workflowId` (string, path, required)
  `permissionId` (string, required)
  `role` (string, enum: ["viewer", "editor", "executor"], required)
`<<REMOVE WORKFLOW PERMISSION>>` DELETE `/workflows/{workflowId}/permissions/{permissionId}`
    `workflowId` (string, path, required)
    `permissionId` (string, path, required)

// Generation 6: Plugin and Extension Ecosystem
`<<REGISTER PLUGIN>>` POST `/plugins`
  `name` (string, required)
  `description` (string, optional)
  `imageUrl` (string, optional)
  `endpoint` (string, url, required)
  `schema` (object, required)
`<<LIST PLUGINS>>` GET `/plugins`
`<<GET PLUGIN>>` GET `/plugins/{pluginId}`
  `pluginId` (string, path, required)
`<<UPDATE PLUGIN>>` PUT `/plugins/{pluginId}`
  `pluginId` (string, path, required)
`<<DELETE PLUGIN>>` DELETE `/plugins/{pluginId}`
  `pluginId` (string, path, required)
`<<ENABLE PLUGIN>>` POST `/workflows/{workflowId}/plugins`
    `workflowId` (string, path, required)
    `pluginId` (string, required)
    `config` (object, optional)
`<<DISABLE PLUGIN>>` DELETE `/workflows/{workflowId}/plugins/{pluginId}`
    `workflowId` (string, path, required)
    `pluginId` (string, path, required)
```


## Enhanced OpenAPI 3.0.0 Specification with JSON Schema

This enhanced specification builds upon the previous version by incorporating JSON Schema for request and response bodies, providing more robust validation and definition.

### Endpoints

#### Workflow Management

*   `POST /start`: Initiates a new workflow.
    *   Request Body Schema:
        ```json
        {
          "type": "object",
          "properties": {
            "high_level_goal": {
              "type": "string",
              "description": "The overarching objective of the workflow. Required if definitionId is not provided."
            },
            "definitionId": {
              "type": "string",
              "description": "The ID of a pre-defined workflow definition to use. Required if high_level_goal is not provided."
            },
            "files": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Any initial files required for the workflow."
            },
            "plan_from": {
              "type": "string",
              "description": "Specifies a plan to start from."
            },
            "orchestrator": {
              "type": "string",
              "default": "Meta-AI",
              "description": "The AI orchestrator to use."
            },
            "model": {
              "type": "string",
              "default": "gemini-2.5-flash-lite",
              "description": "The AI model to utilize."
            }
          },
          "oneOf": [
            { "required": ["high_level_goal"] },
            { "required": ["definitionId"] }
          ]
        }
        ```
    *   Response Body Schema (e.g., for success):
        ```json
        {
          "type": "object",
          "properties": {
            "jobId": {
              "type": "string",
              "description": "The unique identifier for the newly created job."
            },
            "status": {
              "type": "string",
              "enum": ["pending", "running", "completed", "failed", "paused", "paused_for_input"],
              "description": "The initial status of the workflow run."
            }
          },
          "required": ["jobId", "status"]
        }
        ```

*   `POST /runs/{jobId}`: Executes a specific run of a workflow.
    *   Path Parameters:
        *   `jobId`: (string, required) The unique identifier for the job.
    *   Request Body Schema:
        ```json
        {
          "type": "object",
          "properties": {
            "plan": {
              "type": "object",
              "description": "The detailed plan for the run. Structure depends on workflow definition."
            },
            "rounds": {
              "type": "integer",
              "default": 1,
              "description": "The number of execution rounds."
            },
            "files": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Files specific to this run."
            }
          },
          "required": ["plan"]
        }
        ```

*   `GET /runs/{jobId}`: Retrieves the status of a specific workflow run.
    *   Path Parameters:
        *   `jobId`: (string, required) The unique identifier for the job.
    *   Response Body Schema (Example):
        ```json
        {
          "type": "object",
          "properties": {
            "jobId": {
              "type": "string"
            },
            "status": {
              "type": "string",
              "enum": ["pending", "running", "completed", "failed", "paused", "paused_for_input"]
            },
            "progress": {
              "type": "number",
              "description": "Percentage completion of the current run."
            },
            "lastUpdateTime": {
              "type": "string",
              "format": "date-time"
            }
          },
          "required": ["jobId", "status"]
        }
        ```

*   `GET /runs/{jobId}/stream`: Streams real-time events for a workflow run.
    *   Path Parameters:
        *   `jobId`: (string, required) The unique identifier for the job.
    *   Response Body Schema: This endpoint typically returns a stream of Server-Sent Events (SSE) or WebSockets messages. The content of each message would be defined by an `Event` schema.
        *   Example Event Schema:
            ```json
            {
              "type": "object",
              "properties": {
                "eventType": {
                  "type": "string",
                  "enum": ["task_started", "task_completed", "step_progress", "workflow_progress", "error", "human_input_required"]
                },
                "timestamp": {
                  "type": "string",
                  "format": "date-time"
                },
                "details": {
                  "type": "object",
                  "description": "Specific details about the event. For 'human_input_required', this would contain the prompt for the user."
                }
              },
              "required": ["eventType", "timestamp"]
            }
            ```

*   `POST /runs/{jobId}/control`: Controls the execution of a workflow run.
    *   Path Parameters:
        *   `jobId`: (string, required) The unique identifier for the job.
    *   Request Body Schema:
        ```json
        {
          "type": "object",
          "properties": {
            "command": {
              "type": "string",
              "enum": ["pause", "resume", "cancel"],
              "description": "The control command to issue."
            }
          },
          "required": ["command"]
        }
        ```

*   `POST /runs/{jobId}/human-input`: Submits human input to a paused workflow.
    *   Path Parameters:
        *   `jobId`: (string, required) The unique identifier for the job.
    *   Request Body Schema:
        ```json
        {
          "type": "object",
          "properties": {
            "input": {
              "type": "object",
              "description": "The data provided by the human, matching the schema requested by the 'human_input_required' event."
            }
          },
          "required": ["input"]
        }
        ```

#### Advanced Triggering and Event-Driven Workflows

*   `POST /triggers`: Creates a new trigger.
    *   Request Body Schema:
        ```json
        {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "A unique name for the trigger."
            },
            "description": {
              "type": "string",
              "description": "A human-readable description of the trigger."
            },
            "workflowId": {
              "type": "string",
              "description": "The ID of the workflow to be triggered."
            },
            "type": {
              "type": "string",
              "enum": ["schedule", "event"],
              "description": "The type of the trigger."
            },
            "config": {
              "type": "object",
              "description": "Configuration for the trigger. e.g., cron expression for schedule, or event pattern for event."
            }
          },
          "required": ["name", "workflowId", "type", "config"]
        }
        ```

*   `GET /triggers`: Lists all triggers.
    *   Response Body Schema (Example):
        ```json
        {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "triggerId": { "type": "string" },
              "name": { "type": "string" },
              "description": { "type": "string" },
              "workflowId": { "type": "string" },
              "enabled": { "type": "boolean" }
            }
          }
        }
        ```

*   `GET /triggers/{triggerId}`: Retrieves a specific trigger.
    *   Path Parameters:
        *   `triggerId`: (string, required) The unique identifier for the trigger.

*   `PUT /triggers/{triggerId}`: Updates a trigger.
    *   Path Parameters:
        *   `triggerId`: (string, required) The unique identifier for the trigger.
    *   Request Body Schema: (Same as POST, but all fields are optional, and `enabled` can be updated)
        ```json
        {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "description": {
              "type": "string"
            },
            "config": {
              "type": "object"
            },
            "enabled": {
              "type": "boolean"
            }
          }
        }
        ```

*   `DELETE /triggers/{triggerId}`: Deletes a trigger.
    *   Path Parameters:
        *   `triggerId`: (string, required) The unique identifier for the trigger.


#### Webhook Management

*   `POST /webhooks`: Registers a new webhook subscription.
    *   Request Body Schema:
        ```json
        {
          "type": "object",
          "properties": {
            "url": {
              "type": "string",
              "format": "url",
              "description": "The URL to send webhook notifications to."
            },
            "events": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "default": ["workflow_completed", "workflow_failed"],
              "description": "The events to subscribe to."
            },
            "secret": {
              "type": "string",
              "description": "A secret for webhook signature verification."
            }
          },
          "required": ["url"]
        }
        ```
    *   Response Body Schema (Example):
        ```json
        {
          "type": "object",
          "properties": {
            "webhookId": {
              "type": "string",
              "description": "The unique identifier for the registered webhook."
            },
            "status": {
              "type": "string",
              "enum": ["active", "inactive"]
            }
          },
          "required": ["webhookId", "status"]
        }
        ```

*   `GET /webhooks`: Lists all registered webhook subscriptions.
    *   Response Body Schema (Example):
        ```json
        {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "webhookId": {
                "type": "string"
              },
              "url": {
                "type": "string",
                "format": "url"
              },
              "events": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "status": {
                "type": "string",
                "enum": ["active", "inactive"]
              }
            },
            "required": ["webhookId", "url", "events", "status"]
          }
        }
        ```

*   `DELETE /webhooks/{webhookId}`: Unregisters a webhook subscription.
    *   Path Parameters:
        *   `webhookId`: (string, required) The unique identifier for the webhook subscription.

#### History and Reporting

*   `GET /history/runs`: Retrieves historical workflow run data.
    *   Query Parameters:
        *   `limit`: (integer, optional, default: 20) The maximum number of results to return.
        *   `offset`: (integer, optional, default: 0) The number of results to skip.
        *   `status`: (string, optional, enum: ["pending", "running", "completed", "failed", "paused", "paused_for_input"]) Filters runs by status.
        *   `sortBy`: (string, optional, default: "startTime") The field to sort the results by.
        *   `sortOrder`: (string, optional, enum: ["asc", "desc"], default: "desc") The order of sorting.
    *   Response Body Schema (Example):
        ```json
        {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "jobId": {
                "type": "string"
              },
              "high_level_goal": {
                "type": "string"
              },
              "status": {
                "type": "string",
                "enum": ["pending", "running", "completed", "failed", "paused", "paused_for_input"]
              },
              "startTime": {
                "type": "string",
                "format": "date-time"
              },
              "endTime": {
                "type": "string",
                "format": "date-time",
                "nullable": true
              }
            },
            "required": ["jobId", "high_level_goal", "status", "startTime"]
          }
        }
        ```

*   `GET /history/runs/{jobId}/state`: Retrieves the historical state of a specific workflow run.
    *   Path Parameters:
        *   `jobId`: (string, required) The unique identifier for the job.
    *   Response Body Schema (Example):
        ```json
        {
          "type": "object",
          "properties": {
            "jobId": {
              "type": "string"
            },
            "currentState": {
              "type": "object",
              "description": "Represents the state of the workflow at a specific historical point."
            },
            "history": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "timestamp": {
                    "type": "string",
                    "format": "date-time"
                  },
                  "stateSnapshot": {
                    "type": "object",
                    "description": "A snapshot of the workflow state at that timestamp."
                  }
                },
                "required": ["timestamp", "stateSnapshot"]
              }
            }
          },
          "required": ["jobId", "currentState", "history"]
        }
        ```

#### Generation 4: Workflow Definition and Versioning

*   `POST /definitions`: Creates a new workflow definition.
    *   Request Body Schema:
        ```json
        {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "description": { "type": "string" },
            "definition": { "type": "object" }
          },
          "required": ["name", "definition"]
        }
        ```

*   `GET /definitions`: Lists all workflow definitions.

*   `GET /definitions/{definitionId}`: Retrieves a specific workflow definition.

*   `PUT /definitions/{definitionId}`: Updates a workflow definition.

*   `DELETE /definitions/{definitionId}`: Deletes a workflow definition.

*   `POST /definitions/{definitionId}/versions`: Creates a new version of a workflow definition.

*   `GET /definitions/{definitionId}/versions`: Lists all versions of a workflow definition.

#### Generation 5: Collaboration and Access Control

*   `POST /workflows/{workflowId}/share`: Shares a workflow with other users or teams.

*   `GET /workflows/{workflowId}/permissions`: Gets permissions for a workflow.

*   `PUT /workflows/{workflowId}/permissions`: Updates permissions for a workflow.

*   `DELETE /workflows/{workflowId}/permissions/{permissionId}`: Removes a user's or team's permission from a workflow.

#### Generation 6: Extensibility with Plugins

*   `POST /plugins`: Registers a new plugin.

*   `GET /plugins`: Lists available plugins.

*   `GET /plugins/{pluginId}`: Gets details of a plugin.

*   `PUT /plugins/{pluginId}`: Updates a plugin.

*   `DELETE /plugins/{pluginId}`: Deletes a plugin.

*   `POST /workflows/{workflowId}/plugins`: Enables a plugin for a workflow.

*   `DELETE /workflows/{workflowId}/plugins/{pluginId}`: Disables a plugin for a workflow.

### Authentication

*   `securitySchemes`:
    *   `apiKeyAuth`:
        ```json
        {
          "type": "apiKey",
          "name": "X-API-Key",
          "in": "header"
        }
        ```
*   `security`:
    *   `apiKeyAuth`: []