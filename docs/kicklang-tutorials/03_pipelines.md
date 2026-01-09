# Chapter 3: Pipelines (The PLAN Block)

Pipelines are the core control structure in KickLang. They allow you to sequence multiple actions, pass data between them, and organize complex workflows.

## The PLAN Keyword

A pipeline is defined using a Role and the `PLAN` keyword.

```kicklang
⫻role:Planner PLAN PipelineName
  StageName Action ...
  StageName Action ...
```

### Example: A Simple Research Pipeline
```kicklang
⫻role:Planner PLAN PipelineResearchTopic
  Step1Gather roleResearcher FIND EntityTopic SourcesAll → <<raw_data>>
  Step2Filter roleAnalyst CLUSTER <<raw_data>> FilterRelevanceHigh → <<clean_data>>
  Step3Report roleWriter SUMMARIZE <<clean_data>> FormatBrief
```

## Stages
Each line inside a pipeline is a **Stage**.
- **Stage ID**: The first word (e.g., `Step1Gather`). Must be unique within the plan.
- **Role Override** (Optional): You can specify a different role for a specific stage (e.g., `roleResearcher`). If omitted, the parent plan's role is used.
- **Action**: The verb and its arguments.

## Nested Pipelines
KickLang supports nested pipelines for decomposing complex tasks.

```kicklang
⫻role:Planner PLAN HighLevelVis
  StagePrep FIND Data
  
  # Nested Plan
  StageDraft roleArtist PLAN SubPipelineDraft
     Sketch DrawOutlines
     Color FillColors
  
  StageReview REVIEW SubPipelineDraft
```

## Execution Flow
1. **Sequential**: By default, stages run one after another.
2. **Data Dependency**: If Stage 2 uses `<<output>>` from Stage 1, it waits for Stage 1 to complete.

## Naming Conventions
- Pipeline names should be PascalCase (`PipelineMyTask`).
- Stage names should be descriptive (`StageGather`, `StepValidate`).

In the next chapter, we will look at **Action Verbs**, the specific operations you can perform in each stage.
