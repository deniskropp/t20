<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Explain the syntax of PLAN blocks in KickLang

PLAN blocks in KickLang define structured sequences of actions for orchestrating role-based reasoning and knowledge graph operations.[^1][^3]

## Core Syntax

A PLAN block starts with a role prefix (e.g., rolePlanner or roleMetaCognito), followed by "PLAN PipelineName" and optional parameters like GranularityFine or HorizonShortTerm. Stages are nested within using "StageName action parameters," where actions draw from the verb catalog such as FIND, LINK, CLUSTER, or SUMMARIZE.[^3][^1]

Example:

```
rolePlanner PLAN PipelineStorySegment GranularityFine
Stage1Collect storyrequest
Stage2Plot rolePlotWeaver LINK CurrentEvent, precedes, NextPlotPoint
```

Placebo pipes like storyrequest act as meta-markers for deferred inputs or outputs between stages.[^1]

## Key Elements

- **Roles**: Prefix actions (e.g., roleStoryteller) to adopt cognitive stances like Planner for sequencing or Storyteller for narrative synthesis.[^3]
- **Stages**: Sequential blocks (Stage1, Stage2) for modular steps; support conditionals like IF/ELSE for branching based on graph state or traits.[^1]
- **Parameters**: Tune behavior (e.g., ToneEpic, Limit1, FilterPrecedesCurrent) for precision.[^3]


## Usage Patterns

Embed PLAN blocks in patterns or modules for reusability, chaining roles across pipelines (e.g., Storyteller output feeds Planner input). They ensure traceable, layered cognition without immediate execution of deferred pipes.[^1][^3]
<span style="display:none">[^10][^11][^12][^13][^2][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: kicklang-synthesis-objective-m-R_dnjarHQxOY8hblQMCb0A.md

[^2]: One-liner-about-KickLang.md

[^3]: Absolutely-lets-take-that-outline-and-turn-it-i.pdf

[^4]: https://www.kcl-lang.io/docs/reference/lang/tour

[^5]: https://www.reddit.com/r/ProgrammingLanguages/comments/309db8/blocks_syntax/

[^6]: https://picture.iczhiku.com/resource/eetop/WHiErepJdSoDKvnC.pdf

[^7]: https://www.youtube.com/watch?v=8KbjRRqAgBs

[^8]: https://www.youtube.com/watch?v=8gHKGnQjmW8

[^9]: https://pokemondb.net/pokedex/klinklang

[^10]: https://www.sciencedirect.com/science/article/abs/pii/S0004370221001855

[^11]: https://pokemon-planet.fandom.com/wiki/Klinklang

[^12]: https://diglib.eg.org/bitstreams/04475049-98f6-4ab4-a401-1587d4a23033/download

[^13]: https://bulbapedia.bulbagarden.net/wiki/Klinklang_(Pok%C3%A9mon)

