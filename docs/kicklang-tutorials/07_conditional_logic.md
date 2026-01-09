# Chapter 7: Conditional Logic

Real-world workflows aren't always linear. You often need to make decisions based on data, user input, or the state of the world. KickLang provides `IF`, `ELSE`, and `END` blocks for this purpose.

## Syntax
Conditional blocks are placed directly inside a `PLAN`.

```kicklang
IF [Condition]
  StageName Action ...
ELSE
  StageName Action ...
END
```

*Note: Some implementations allow Python-style indentation without explicit END, but `END` is safer for clarity.*

## Types of Conditions

### 1. Entity Existence
Check if a `FIND` operation returned any results.

```kicklang
Stage1 FIND EntityDragon
IF <<results>>exists
  Stage2 roleHero ATTACK EntityDragon
ELSE
  Stage2 roleHero EXPLORE Cave
END
```

### 2. Trait Matching
Check if an entity has a specific trait.

```kicklang
IF has_trait=HighTension
  StageCrisis rolePlanner PLAN CrisisResponse
END
```

### 3. Quantitative Comparisons
Check numeric values or counts.

```kicklang
IF CLUSTER>5
  StageParallel roleTeam PLAN ParallelWork
END

IF precedes>3
  # If the chain is longer than 3 steps...
  StageStop roleManager SUMMARIZE Chain
END
```

### 4. Pipe Values
Check the content or metadata of a placebo pipe.

```kicklang
IF <<tension>>High
  StageCalm roleMediator PLAN Deescalate
END
```

## Complex Logic
You can nest `IF` blocks, though it is often cleaner to break complex logic into sub-pipelines.

```kicklang
IF <<user_input>>Valid
  IF <<user_input>>Urgent
     StageFastTrack roleAdmin DO_IT_NOW
  ELSE
     StageNormal roleWorker DO_IT_LATER
  END
END
```

In the next chapter, we will explore the underlying **Knowledge Graph** that powers these conditions.
