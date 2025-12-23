<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# How to define ContextArtifact and NarrativeArtifact types

ContextArtifact and NarrativeArtifact are typed artifacts in KickLang pipelines, serving as structured inputs and outputs for nested PLAN operations.[^2]

## Defining Artifacts

Artifacts represent symbolic entities with declared schemas, enabling type-safe cognitive contracts between pipeline stages. Define them using explicit bindings in PLAN syntax: ContextArtifact as input (e.g., EntityContext with nodes like scenes or lore via FIND), NarrativeArtifact as output (e.g., synthesized prose with graph diffs via SUMMARIZE TRANSFORM ViewProse). Formal notation: PLAN<ContextArtifact, NarrativeArtifact> PipelineSub specifies Tin → Tout flow.[^1][^2]

## Schema Specification

Use knowledge graph primitives for typing: ContextArtifact CLUSTER EntitySetContext {Nodes: Characters/Locations/Events, Edges: precedes/hasttrait}; NarrativeArtifact LINK EntityStory {Text: Prose, Metadata: GraphDiffs}. Embed in module headers: moduleStoryPipeline v1.0 input ContextArtifact output NarrativeArtifact.[^3][^1][^2]

## Usage in Pipelines

In rolePlanner PLAN PipelineMain GranularityFine, Stage2Nested roleSubPlanner PLAN PipelineSub context yields NarrativeArtifact for Stage3Synth SUMMARIZE. Introspection via planid/depth ensures traceability without mutable state sharing.[^1][^2]
<span style="display:none">[^10][^11][^12][^13][^14][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: kicklang-synthesis-objective-m-R_dnjarHQxOY8hblQMCb0A.md

[^2]: this-is-solid-and-more-than-th-3FjwxRxoTDifMknLoT89qw.md

[^3]: Absolutely-lets-take-that-outline-and-turn-it-i.pdf

[^4]: One-liner-about-KickLang.md

[^5]: https://hacktext.com/2011/02/artifacts-building-dimension-into-your-narrative-narrative-artifacts-1-of-4-510/

[^6]: https://en.wikipedia.org/wiki/Artifact_(archaeology)

[^7]: https://condens.io/help/using-condens/sharing-findings/using-artifacts-for-research-outcomes/

[^8]: https://plato.stanford.edu/entries/artifact/

[^9]: https://repository.upenn.edu/bitstreams/6a295234-92f8-4857-97b3-951b09d7f7ff/download

[^10]: https://www.interaction-design.org/literature/topics/artifact

[^11]: https://study.com/learn/lesson/cultural-artifact-social-examples.html

[^12]: https://www.studysmarter.co.uk/explanations/anthropology/archaeology-and-anthropology/artifact-analysis/

[^13]: https://methods.sagepub.com/ency/edvol/sage-encyc-qualitative-research-methods/chpt/artifact-analysis

[^14]: https://fiveable.me/key-terms/introduction-archaeology/artifact-types

