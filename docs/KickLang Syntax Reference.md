<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Generate KickLang Syntax Reference

KickLang is a formal language and cognitive framework designed for orchestrating layered, role-based reasoning and knowledge structuring, with a syntax built around meta-communicative and modular workflows for dynamic collaboration in knowledge graphs. Below is a concise KickLang syntax reference based on the available documentation.[^2][^9]

### Core Role Presets

KickLang uses cognitive roles as lenses for system engagement. Common roles include:

- Researcher: Evidence gathering, source validation
- Analyst: Causal reasoning, trend mapping
- Storyteller: Narrative synthesis, context weaving
- Summarizer: Condensation into digestible insights
- Planner: Sequencing, dependencies, meta-logic

Each role can be parameterized for depth, focus, or output style.[^3][^9]

### Action Verb Catalog

KickLang’s syntax centers on verbs for knowledge access, structuring, and transformation:

- Knowledge Access: `FINDEntityRelation`, `LISTEntitiesRelations`, `DETAILEntity`
- Knowledge Structuring: `LINKEntityA, Relation, EntityB`, `MAPEntityA - EntityB`, `CLUSTEREntitySet`
- Knowledge Transformation: `SUMMARIZEEntityCorpus`, `COMPAREEntityA, EntityB`, `EXPLAINEntityRelation`
- Meta Operations: `COMMENT`, `PLANPipeline`, `TRANSFORMView`.[^3]


### Pipeline and Staging Syntax

Pipelines are defined with `PLANPipelineName` and can be staged for progressive knowledge building:

```
rolePlanner PLAN PipelineStorySegment StageCollectRequest, StageWeavePlot, StageUpdateWorld, StageNarrate, StageSyncCharacters, StageSynthesizeOutput
```

Stages can be conditional and support nested `PLAN` blocks for layered cognition.[^4][^9]

### Placebo Pipes and Meta-Markers

Placebo pipes are meta-markers for deferred or conditional steps:

- Example: `Planner PLAN PipelineClimateMitigationAnalysis StageCollectData, StageRunScenarioModels, StageDraftPolicyBrief`
Pipes signal staged actions or deferred logic, making all reasoning traceable.[^9][^3]


### Example Syntax Block

```
rolePlanner PLAN PipelineMain GranularityFine
  Stage1Prep FIND EntityContext context
  Stage2Nested roleSubPlanner PLAN PipelineSub context
  Stage3Synth SUMMARIZE PipelineSub output
```

This structure demonstrates role delegation, pipeline nesting, and compositional cognition.[^4][^9]

### Key Features

- Modular, reusable patterns and pipelines
- Role chaining for multi-perspective outputs
- Conditional branching and cognitive zooming
- Traceable, hierarchical reasoning through nested PLANs

KickLang’s syntax is designed for transparency, traceability, and cognitive orchestration, supporting both simple queries and complex, layered workflows.[^9][^3][^4]
<span style="display:none">[^1][^10][^11][^12][^13][^5][^6][^7][^8]</span>

<div align="center">⁂</div>

[^1]: kicklang-synthesis-objective-m-R_dnjarHQxOY8hblQMCb0A.md

[^2]: One-liner-about-KickLang.md

[^3]: Absolutely-lets-take-that-outline-and-turn-it-i.pdf

[^4]: this-is-solid-and-more-than-th-3FjwxRxoTDifMknLoT89qw.md

[^5]: https://www.kcl-lang.io/docs/reference/lang/tour

[^6]: https://pkl-lang.org/main/current/language-reference/index.html

[^7]: https://stackoverflow.com/questions/73385297/generate-a-method-dispatcher-with-define-syntax-in-racket

[^8]: https://www.youtube.com/watch?v=MOawB4k9-jk

[^9]: https://huggingface.co/collections?p=15860\&sort=trending

[^10]: https://github.com/KusionStack/KCLVM/issues/212

[^11]: https://racket.discourse.group/t/where-to-find-the-correct-syntax-for-lang-racklog/3759

[^12]: https://www.nextlang.co/docs

[^13]: https://wiki.tcl-lang.org/page/Generating+Syntax+Diagrams+Using+Tk

