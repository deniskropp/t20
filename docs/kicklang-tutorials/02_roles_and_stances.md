# Chapter 2: Roles and Stances

In KickLang, a **Role** is more than just a user ID; it is a "cognitive stance." It defines the persona, capabilities, and constraints of the agent performing an action.

## Defining a Role

Roles are invoked using the `⫻role:` syntax (or simply `roleName` inside specific blocks).

```kicklang
⫻role:Researcher
⫻role:Storyteller
⫻role:Planner
```

## Parameterization

You can specialize a role by appending parameters directly to its invocation. These parameters act as modifiers for the underlying model's system prompt or context.

### Syntax
```kicklang
⫻role:RoleName Parameter1 Parameter2 ...
```

### Examples

**1. A meticulous Researcher:**
```kicklang
⫻role:Researcher DepthHigh SourceAcademic
```

**2. A creative Storyteller:**
```kicklang
⫻role:Storyteller ToneEpic GenreFantasy
```

**3. A high-level Planner:**
```kicklang
⫻role:Planner GranularityCoarse HorizonLongTerm
```

## How Parameters Work
When the KickLang interpreter sees `DepthHigh`, it adjusts the `Researcher`'s instructions to prioritize depth over breadth. Similarly, `ToneEpic` instructs the `Storyteller` to use grand, dramatic language.

## Role Scope
Roles apply to the action immediately following them, or to the entire block if used in a `PLAN` definition.

```kicklang
# Applied to a single line
⫻role:Analyst COMPUTE Statistics

# Applied to a block (implicit in stage names if not overridden)
⫻role:Planner PLAN MasterPlan
  Stage1 FIND ...  # Executed by Planner
  Stage2 roleResearcher FIND ... # Executed by Researcher (override)
```

## Best Practices
- **Be Descriptive:** Use standard role names (`Researcher`, `Analyst`) for clarity.
- **Reuse Parameters:** Stick to a consistent vocabulary for parameters (e.g., `DepthHigh`, `DepthLow` rather than `VeryDeep`, `Shallow`).

In the next chapter, we will explore **Pipelines**, the backbone of KickLang orchestration.
