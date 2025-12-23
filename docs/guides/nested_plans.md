# Nested PLAN Blocks in KickLang

KickLang supports modular and hierarchical planning through **Nested PLAN Blocks**. This allows you to define high-level plans where specific stages are delegated to sub-planners or dedicated agents to execute their own detailed workflows.

## Syntax

A nested plan is defined within a `PLAN` block by assigning a stage to a specific role and using the `PLAN` keyword followed by the name of the sub-plan.

```kicklang
roleMainPlanner PLAN MainProject
Stage1 SetupEnv
Stage2 roleSubPlanner PLAN ComponentDevelopment
Stage3 Integration
```

In this example:
1.  `roleMainPlanner` executes `Stage1` and `Stage3` (implied default role).
2.  `Stage2` is assigned to `roleSubPlanner`.
3.  The task for `Stage2` is to execute the `ComponentDevelopment` plan.

## Semantics

When the runtime encounters a task with the description `PLAN <PlanName>`, it interprets this as a directive to:
1.  **Delegate**: Transfer control to the agent assigned to the role (e.g., `roleSubPlanner`).
2.  **Expand**: The delegate agent should generate or retrieve the detailed steps for `<PlanName>`.
3.  **Execute**: The sub-plan is executed as a self-contained workflow.
4.  **Return**: Upon completion of the sub-plan, the result (artifacts/output) is returned to the main plan's context, and execution proceeds to the next stage (`Stage3`).

## Example: Software Development

Here is a practical example of a software development workflow using nested plans.

### Main Plan
```kicklang
roleTechLead PLAN AppDevelopment
Stage1 InitRepo
Stage2 roleBackendLead PLAN BackendSystem
Stage3 roleFrontendLead PLAN FrontendInterface
Stage4 VerifySystem
```

### Sub-Plans (Conceptual)

The `BackendSystem` plan might look like this (managed by `roleBackendLead`):

```kicklang
roleBackendLead PLAN BackendSystem
Stage1 DatabaseSchema
Stage2 APIEndpoints
Stage3 AnthropicIntegration
```

## Benefits

-   **Modularity**: Break down complex goals into manageable sub-components.
-   **Specialization**: Assign different parts of the workflow to agents with specialized prompts/roles.
-   **Scalability**: Manage large-scale projects without a single, monolithic plan file.
