# Chapter 9: Modules and Patterns

As your KickLang projects grow, you will want to reuse code. KickLang supports **Modules** (external files) and **Patterns** (named, reusable blocks).

## Modules

A module is simply a `.klang` file that exports functionality.

### 1. Creating a Module
Create a file named `storyteller-planner.klang`.

```kicklang
⫻module:StorytellerToPlanner v1.0
<<Narrative → Planning chain>>

# Inputs
<<input>>

# Logic
⫻role:Storyteller SUMMARIZE <<input>> ToneEpic → <<narrative>>
⫻role:Planner PLAN PipelineNext GranularityFine <<narrative>> → <<plan>>

# Output
⫻output:<<narrative>> + <<plan>>
```

### 2. Importing a Module
In your main file:

```kicklang
# Import the file
⫻import:KickLang-Modules/storyteller-planner

# Invoke the module
⫻module:StorytellerToPlanner <<input:Scene1>>
```

## Patterns

Patterns are similar to modules but can be defined inline or within a patterns library. They represent common architectural flows.

```kicklang
⫻pattern:Meta-AI-Storybook
<<Reusable pipeline for generating consistent story segments>>

# Pattern Definition
⫻role:MetaCognito PLAN PipelineStorySegment <<story_request>>
  Stage1 ...
  Stage2 ...
```

### Invoking a Pattern
```kicklang
⫻pattern:Meta-AI-Storybook
```

## Creating a Library
You can organize your modules into a directory structure:

```
KickLang-Modules/
├── README.md
├── modules/
│   └── storyteller-planner.klang
└── patterns/
    └── meta-ai-storybook.klang
```

This ensures your team can share and version-control common cognitive workflows.

In the final chapter, we will bring everything together into a **Complete Application**.
