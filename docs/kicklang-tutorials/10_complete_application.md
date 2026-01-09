# Chapter 10: A Complete Application

Congratulations! You've learned the core components of KickLang. Now, let's build a complete, cohesive application: **The Interactive Story Engine**.

## Goal
Create a system where:
1. A **Storyteller** generates a scene.
2. A **Planner** decides the next plot points based on the scene.
3. A **Critic** evaluates if the story is exciting enough.
4. If it's boring, we regenerate it.

## The Code

```kicklang
# Main.klang

# 1. Setup Roles
⫻role:Storyteller ToneDark GenreSciFi
⫻role:Planner GranularityFine HorizonShortTerm
⫻role:Critic CriteriaSuspense CriteriaPacing

# 2. Main Execution Pipeline
⫻role:Director PLAN InteractiveStoryEngine
  
  # Step A: Generate Scene
  StageGen roleStoryteller SUMMARIZE EntityPrompt "A derelict spaceship" → <<scene>>
  
  # Step B: Critique
  StageEval roleCritic COMPARE <<scene>> StandardExcitement → <<score>>
  
  # Step C: Branching Logic
  IF <<score>>Low
     # Loop back or fix
     StageFix roleStoryteller TRANSFORM <<scene>> AddConflict → <<final_scene>>
  ELSE
     StageKeep PASS <<scene>> → <<final_scene>>
  END
  
  # Step D: Update Graph
  StagePersist LINK Scene1, produces, <<final_scene>>
  
  # Step E: Plan Next
  StageNext rolePlanner PLAN PipelineNextSteps <<final_scene>>
    Step1 FIND EntityCharacters FilterInScene
    Step2 LINK NewPlotPoint, follows, Scene1
```

## Spec Breakdown
1. **Roles**: We defined 3 specialized roles.
2. **Pipelines**: `InteractiveStoryEngine` orchestrates the flow.
3. **Placebo Pipes**: `<<scene>>`, `<<score>>`, `<<final_scene>>` carry data.
4. **Conditions**: `IF <<score>>Low` handles quality control.
5. **Graph Ops**: `LINK` saves the state to memory.

## Next Steps
You are now ready to write your own KickLang programs!
- Explore the `guides/` folder for specific use cases.
- Check the `api_reference.md` for a full list of Verbs.
- Start building!
