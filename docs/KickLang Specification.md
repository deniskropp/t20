## KickLang Specification

### Core Syntax

#### Roles
- Roles are cognitive stances, not just agents.
- Example roles: Researcher, Analyst, Storyteller, Planner.
- Parameterization: `ResearcherDepthHigh`, `StorytellerToneEpic`, `PlannerGranularityFine`.

#### Action Verbs
- Knowledge Access: `FIND`, `LIST`, `DETAIL`
- Knowledge Structuring: `LINK`, `MAP`, `CLUSTER`
- Knowledge Transformation: `SUMMARIZE`, `COMPARE`, `EXPLAIN`
- Meta Operations: `COMMENT`, `PLAN`, `TRANSFORM`

#### Pipelines
- Sequences of actions, supporting nested and conditional PLAN blocks.
- Example:
```
  rolePlanner PLAN PipelineMain
    Stage1Prep FIND EntityContext context
    Stage2Nested roleSubPlanner PLAN PipelineSub context
    Stage3Synth SUMMARIZE PipelineSub output
  ```

#### Placebo Pipes
- Deferred or conditional steps, used for traceable, modular workflows.
- Example: `<<story_request>>`, `<<world_state>>`, `<<character_update>>`, `<<plot_point>>`, `<<synthesis_output>>`

### Knowledge Graph Structure

#### Nodes
- Characters, Locations, Events, Items, Concepts.

#### Edges
- `has_trait`, `located_in`, `precedes`, `interacts_with`, `possesses`.

### Example Patterns

#### Meta-AI Storybook Pattern
  ```
⫻pattern:Meta-AI-Storybook
<<Reusable pipeline for generating consistent story segments via role orchestration and knowledge graph updates>>
```

#### Storyteller to Planner Chain
```
⫻role:Storyteller SUMMARIZE EntityScene ToneEpic → <<narrative>>
⫻role:Planner PLAN PipelineNext GranularityFine <<narrative>> [attached_file:2]
```

### Conditional Branching

#### Branch Types
- Entity Exists: `IF EntityX exists → BranchA`
- Trait Match: `IF has_trait=HighTension → DarkPath`
- Relation Count: `IF precedes>3 → ClimaxBranch`
- Cluster Size: `IF CLUSTER>5 → ParallelArc`
- Pipe Value: `IF <<tension>>High → ConflictPath`

#### Pipeline Example
```
⫻role:Planner PLAN PipelineBranching GranularityFine
  StageCheck: FIND Scene4 Filterhas_trait=Confrontation → <<state>>
  IF <<state>>exists:
    LINK Scene4, precedes, DragonDialogue; ToneIntense
  ELSE:
    LINK Scene4, precedes, EscapeRoute; ToneRelief
  IF CLUSTER EntityCharacters>3:
    ⫻role:Storyteller LINK Scene5, involves_multiple, GroupConflict [file:2]
```

### Modules and Reuse

#### Module Structure
```
KickLang-Module/
├── README.md
└── modules/
    └── storyteller-planner.klang
```

#### Module Example
```
⫻module:StorytellerToPlanner v1.0
<<Narrative → Planning chain>>
⫻role:Storyteller SUMMARIZE <<input>> ToneEpic → <<narrative>>
⫻role:Planner PLAN PipelineNext GranularityFine <<narrative>> → <<plan>>
⫻output:<<narrative>> + <<plan>> [attached_file:2]
```

### Invocation and Usage

#### Pattern Invocation
```
⫻kicklang:Execution/Pattern
⫻role:MetaCognito PLAN PipelineStorySegment <<story_request:User prompt or continuation>>
⫻pattern:Meta-AI-Storybook
```

#### Module Invocation
```
⫻import:KickLang-Module/storyteller-planner
⫻module:StorytellerToPlanner <<input:Hero battles dragon>>
```

### Graph Operations

#### Linking Scenes
```
⫻role:Planner LINKCHAIN Scene1 GranularityFine Horizon3Steps [file:2]
```

#### Querying Full Chain
```
⫻role:Planner MAP Scene1 - precedes - * → <<story_arc>> [file:2]
```

### Conditional Triggers

#### Recommended Conditions
- Tension Threshold: `IF CLUSTER Tension>Medium → StorytellerPlanner`
- Scene Gap: `IF precedes<3 → StorytellerPlanner`
- Character Conflict: `IF COMPARE CharacterStates ConflictHigh → StorytellerPlanner`
- Narrative Stall: `IF <<narrative_length>>Short → StorytellerPlanner`
- Arc Milestone: `IF MAP SceneChain Length=Climax → StorytellerPlanner`

### Example Pipeline Execution

#### Execution Result
```
Graph: Scene1 → ... → Scene3 → Scene4(Confrontation) → Scene5(Revelation)

<<synthesis_output>>: Elara confronts the dragonlord amid crumbling ruins.
Flames illuminate ancient runes—Scene4. The beast speaks: "You bear the prophecy."
Revelation dawns as crystal pulses in sync. [file:2]
```

### Knowledge Graph Schema

#### Nodes and Edges
```
Nodes: Characters, Locations, Events, Items, Concepts
Edges: has_trait, located_in, precedes, interacts_with, possesses [attached_file:2]
```

### Role Mapping Table

| Storybook element | KickLang framing | Typical verbs |
| :-- | :-- | :-- |
| Characters | Entity nodes with `has_trait`, `interacts_with` | FIND, DETAIL, LINK, CLUSTER |
| Locations | Entity nodes with `located_in` hierarchy | FIND, MAP, LINK |
| Events / plot points | Event nodes linked by `precedes`, `involves` | LINK, MAP, COMPARE |
| Items | Entity nodes with `possesses`, `located_in` | FIND, LINK |
| Concepts / themes | Higher-order entities attached via `influences`, `symbolizes` | CLUSTER, SUMMARIZE, EXPLAIN |

### Story Segment Generation

#### Process
1. `<<story_request>>` received by MetaCognito.
2. MetaCognito routes request to PlotWeaver and WorldBuilder.
3. PlotWeaver determines next `<<plot_point>>`.
4. WorldBuilder updates `<<world_state>>`.
5. MetaCognito routes `<<plot_point>>` and `<<world_state>>` to Storyteller and CharacterManager.
6. Storyteller generates narrative, CharacterManager updates `<<character_update>>`.
7. All roles submit outputs to MetaCognito.
8. MetaCognito synthesizes into `<<synthesis_output>>` using KickLang graph operations.

### Placebo Pipes as Meta-Markers

#### Pipes
- `<<story_request>>`: Input for story generation.
- `<<world_state>>`: Current setting details.
- `<<character_update>>`: Character status and dialogue.
- `<<plot_point>>`: Next narrative event.
- `<<synthesis_output>>`: Final story segment.

### Modules and Reuse

#### Module Packaging
1. Create module file (`module-name.klang`).
2. Structure library Space.
3. Pin in Spaces.
4. Import syntax: `⫻import:KickLang-Library/StorytellerToPlanner`.

#### Versioning
- Use `v1.0 → v1.1` tags.
- Import `⫻import:Latest` auto-upgrades.

#### Distribution Options
- Space pinning: Central "KickLang Modules" Space → reference `⫻import:SpaceID/ModuleName`.
- Copy-paste: Direct block embedding (no import needed).
- Versioning: `⫻module:Name v1.1` → auto-upgrades via `⫻import:Latest`.

### Minimal Project Structure

#### Structure
```
KickLang-Modules/
├── README.md
├── modules/
│   └── storyteller-planner.klang
└── patterns/
    └── meta-ai-storybook.klang
```

### Core Files

#### README.md
```
# KickLang Module Library v1.0

## Usage
⫻import:KickLang-Modules/storyteller-planner
⫻module:StorytellerToPlanner <<input:Scene>>

## Modules
- storyteller-planner.klang [attached_file:2]
- meta-ai-storybook.klang [attached_file:2]
```

#### modules/storyteller-planner.klang
```
⫻module:StorytellerToPlanner v1.0
<<Narrative → Planning chain>>
⫻role:Storyteller SUMMARIZE <<input>> ToneEpic → <<narrative>>
⫻role:Planner PLAN PipelineNext GranularityFine <<narrative>> → <<plan>>
⫻output:<<narrative>> + <<plan>> [attached_file:2]
```

#### patterns/meta-ai-storybook.klang
```
⫻pattern:Meta-AI-Storybook-Minimal
⫻role:MetaCognito PLAN PipelineStory <<story_request>> [attached_file:2]
```

### Deploy Instructions

#### Instructions
1. Upload folder to Space as "KickLang Library".
2. Pin `README.md` in Welcome section.
3. Import anywhere: `⫻import:KickLang-Modules/storyteller-planner`.

### Example Code and Module File

#### README.md
```
# KickLang Simple Module Library

## Example Usage
⫻import:KickLang-SimpleModule/basic-research
⫻role:Researcher FINDEntityRelation AI FilterYear2025 Limit5 [file:2]

## Modules Available
- basic-research.klang [file:2]
```

#### modules/basic-research.klang
```
⫻module:BasicResearch v1.0
<<Simple research → analysis → summary pipeline>>

⫻role:Researcher FINDEntityRelation <<query>> Limit5 → <<sources>>
⫻role:Analyst CLUSTER <<sources>> ViewTrends → <<insights>>
⫻role:Summarizer SUMMARIZE <<insights>> LengthShort → <<output>>

⫻output:<<output>> [Sources:<<sources>>] [file:2]
```

### Example Invocation

#### Invocation
```
⫻module:BasicResearch <<query:AI ethics 2025>>
```

#### Output
```
Key AI ethics trends from 2025 sources, clustered and summarized.
```

### Passing Context and Memory

#### Pipe Method
```
⫻role:Storyteller SUMMARIZE EntityScene ToneEpic → <<narrative>>
⫻role:Planner PLAN PipelineNext GranularityFine <<narrative>> → <<plan>> [file:2]
```

#### Graph Method
```
⫻role:Storyteller LINK Scene1, produces, NarrativeNode; has_trait=Epic
⫻role:Planner FIND EntityNarrativeNode FilterPrecedesCurrent → <<context>>
⫻role:Planner PLAN PipelineNext <<context>> [file:2]
```

### Complete Module Example

#### Module
```
⫻module:StorytellerPlannerMemory v1.0
⫻role:Storyteller SUMMARIZE <<scene>> ToneEpic → <<narrative>>
LINK <<scene>>, produces, <<narrative>>  # Memory storage
⫻role:Planner FIND NarrativeNode FilterRecent → <<memory>>
PLAN PipelineNext <<narrative>>+<<memory>> → <<plan>>
⫻output:<<narrative>> + <<plan>> [file:2]
```

### Usage

#### Usage
```
⫻module:StorytellerPlannerMemory <<scene:Hero enters dungeon>>
```

#### Next Call
```
Planner automatically recalls prior `NarrativeNode` via `FIND`.
```

### Graph State Update

#### Update
```
Scene1 ─produces→ NarrativeNode (has_trait=Epic)
```

### Planner Memory Retrieval

#### Retrieval
```
⫻role:Planner FIND EntityNarrativeNode FilterPrecedesCurrent → <<context>>
```

#### Retrieved
```
<<context>> = NarrativeNode{Epic}
```

### Next Pipeline

#### Pipeline
```
⫻role:Planner PLAN PipelineNext GranularityFine <<context>>
Stage1: LINK NarrativeNode, precedes, Scene2 (TensionRising)
Stage2: CLUSTER EntitySetStory FilterRecent → <<arc>>
⫻output:<<arc>> [file:2]
```

#### Output
```
Elara clutches the prophecy crystal as shadows lengthen. A guttural roar echoes—Scene2 begins. Tension rises; dragonlord stirs.
```

### Persistent Graph

#### Graph
```
Scene1 → NarrativeNode → Scene2 (TensionRising) [file:2]
```

#### Memory
```
Next `FIND` retrieves full chain automatically.
```

### Linking Scenes

#### Command
```
⫻role:Planner LINKCHAIN Scene1 GranularityFine Horizon3Steps [file:2]
```

#### Result
```
Scene1 → NarrativeNode1 → Scene2 → NarrativeNode2 → Scene3 → NarrativeNode3
[Epic]       [precedes]    [TensionRising] [precedes]  [Climax]    [Resolution]
```

### Compact Sequence

#### Sequence
```
⫻role:Planner PLAN PipelineSceneChain
  LINK Scene1, precedes→, Scene2; Scene2, precedes→, Scene3
  LINK Scene2, produces→, Narrative2; Scene3, produces→, Narrative3 [file:2]
```

### Query Full Chain

#### Query
```
⫻role:Planner MAP Scene1 - precedes - * → <<story_arc>> [file:2]
```

#### Executes
```
Scene1 → Scene2 → Scene3 with narrative nodes auto-linked. Ready for `FIND` retrieval.
```

### Planner Pipeline to Continue

#### Pipeline
```
⫻role:Planner PLAN PipelineContinueScene1 GranularityFine HorizonShortTerm [file:2]
```

#### Execution Result
```
Graph: Scene1 → ... → Scene3 → Scene4(Confrontation) → Scene5(Revelation)

<<synthesis_output>>: Elara confronts the dragonlord amid crumbling ruins.
Flames illuminate ancient runes—Scene4. The beast speaks: "You bear the prophecy."
Revelation dawns as crystal pulses in sync. [file:2]
```

### Full Chain Query

#### Query
```
⫻role:Planner MAP Scene1 - precedes - * ViewStoryArc [file:2]
```

#### Yields
```
Complete Scene1→Scene5 arc with traits and narratives.
```

#### Pipeline
```
Auto-extends from Scene1's current chain position.
```

### Conditional Branch Types

#### Types
- Entity Exists: `IF EntityX exists → BranchA`
- Trait Match: `IF has_trait=HighTension → DarkPath`
- Relation Count: `IF precedes>3 → ClimaxBranch`
- Cluster Size: `IF CLUSTER>5 → ParallelArc`
- Pipe Value: `IF <<tension>>High → ConflictPath`

### Pipeline Example

#### Example
```
⫻role:Planner PLAN PipelineBranching GranularityFine
  StageCheck: FIND Scene4 Filterhas_trait=Confrontation → <<state>>
  IF <<state>>exists:
    LINK Scene4, precedes, DragonDialogue; ToneIntense
  ELSE:
    LINK Scene4, precedes, EscapeRoute; ToneRelief
  IF CLUSTER EntityCharacters>3:
    ⫻role:Storyteller LINK Scene5, involves_multiple, GroupConflict [file:2]
```

### Common Triggers

#### Triggers
- Graph State: `Entity exists`, `Relation count`, `Trait value`
- Pipeline State: `<<pipe>>High/Low`, `Stage succeeded/failed`
- Temporal: `TimeHorizonShort→QuickResolution`
- Quantitative: `CLUSTER size>5→ParallelStorylines`

#### Usage
```
Embed `IF/ELSE` directly in PLAN stages for dynamic routing.
```

### Recommended Branch Conditions

#### Conditions
- Tension Threshold: `IF CLUSTER Tension>Medium → StorytellerPlanner`
- Scene Gap: `IF precedes<3 → StorytellerPlanner`
- Character Conflict: `IF COMPARE CharacterStates ConflictHigh → StorytellerPlanner`
- Narrative Stall: `IF <<narrative_length>>Short → StorytellerPlanner`
- Arc Milestone: `IF MAP SceneChain Length=Climax → StorytellerPlanner`

### Pipeline Template

#### Template
```
⫻role:Planner PLAN PipelineStoryBranch GranularityFine
  StageCheckTension: CLUSTER EntityScenes FilterTension → <<tension_level>>
  IF <<tension_level>>Medium:
    ⫻module:StorytellerToPlanner <<current_scene>>
  IF MAP Scene1-precedes Length<5:
    ⫻role:Storyteller LINK NextScene, produces, NarrativeNew ToneEpic
    ⫻role:Planner PLAN PipelineNext <<NarrativeNew>> [file:2]
```

### Priority Triggers

#### Triggers
- Always: `SceneCount<HorizonLongTerm` (extend underdeveloped arcs)
- High: `Trait=UnresolvedConflict` (force plot advancement)
- Critical: `<<user_request>>Continue` (direct continuation demand)

#### Rationale
```
Storyteller→Planner excels at creative extension when graph shows gaps, tension, or incomplete arcs per Playbook role chaining.
```

### KickLang Standard Specification

#### Core Principles
- Roles are cognitive stances, not just agents.
- Action verbs structure knowledge access, transformation, and synthesis.
- Placebo pipes act as meta-markers, deferring or flagging logic for staged or conditional execution.

#### Syntax and Semantics
- Pipelines (PLAN) sequence actions, allowing for nested, composable reasoning episodes.
- Nested PLANs have strict lifecycle containment.
- Role scoping is explicit and local.

#### Standard Specification Outline
- Roles: Cognitive stances with parameterization.
- Action Verbs: Knowledge Access, Knowledge Structuring, Knowledge Transformation, Meta Operations.
- Pipelines: Sequences of actions, supporting nested and conditional PLAN blocks.
- Placebo Pipes: Deferred or conditional steps.
- Typing and Introspection: PLANs are typed functions over structured contexts.

#### Example Pipeline
```
rolePlanner PLAN PipelineMain
  Stage1Prep FIND EntityContext context
  Stage2Nested roleSubPlanner PLAN PipelineSub context
  Stage3Synth SUMMARIZE PipelineSub output
```

#### KickLang’s Standard Specification
```
Enables robust, transparent, and modular orchestration of cognitive workflows, making it a living manual for collective reasoning and knowledge synthesis.
```
