# Chapter 1: Introduction to KickLang

Welcome to **KickLang**, a domain-specific language designed for orchestrating cognitive roles, knowledge graphs, and complex reasoning pipelines.

KickLang is not just about writing code; it's about defining **who** does the work (Roles), **what** they do (Action Verbs), and **how** information flows between them (Pipelines & Knowledge Graph).

## What You Will Learn
In this series, you will learn how to:
1. Define cognitive Roles with specific parameters.
2. Structure reasoning attributes using Action Verbs.
3. Build Pipelines to sequence complex tasks.
4. Interact with a persistent Knowledge Graph.
5. Use Modules and Patterns to reuse logic.

## The Basic Structure

A KickLang script typically consists of three main components:
1. **Role Definitions** (implicit or explicit)
2. **Action Execution** (Pipelines or direct calls)
3. **Graph Operations** (Querying or modifying the state)

Here is a classic "Hello World" equivalent in KickLang:

```kicklang
⫻role:Greeter SUMMARIZE EntityWelcomeMessage ToneFriendly → <<greeting>>
⫻output:<<greeting>>
```

### Breakdown:
- `⫻role:Greeter`: We assign the cognitive stance of a "Greeter".
- `SUMMARIZE`: The action verb used.
- `EntityWelcomeMessage`: The target entity (concept) to process.
- `ToneFriendly`: A parameter guiding the role's behavior.
- `→ <<greeting>>`: The result is piped into a "Placebo Pipe" (variable) named `<<greeting>>`.
- `⫻output`: A special directive to display the final result.

## Running KickLang
KickLang code is typically saved in `.klang` files. The compiler or interpreter parses these files, builds an execution plan, and orchestrates the specified agents/LLMs to fulfill the roles.

## Your First Pipeline

Most real work happens inside a **PLAN**.

```kicklang
⫻role:Planner PLAN PipelineHelloWorld
  Stage1 FIND EntityUserContext
  Stage2 LIST AllGreetings
  Stage3 SUMMARIZE EntityUserContext + AllGreetings → <<final_message>>
```

In the next chapter, we will dive deeper into **Roles** and how to parameterize them effectively.
