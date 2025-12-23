<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KickLang Standard Specification

The KickLang Standard Specification defines a formal language and cognitive framework for orchestrating layered, role-based reasoning and knowledge structuring. KickLang enables modular, traceable workflows in knowledge graphs, supporting progressive knowledge building and multi-perspective synthesis.[^2][^4][^5]

### Core Principles

- Roles are cognitive stances, not just agents. Each role (e.g., Researcher, Analyst, Storyteller, Planner) defines a specific approach to a task, shaping both style and content.[^4][^5]
- Action verbs structure knowledge access, transformation, and synthesis (e.g., FIND, LINK, CLUSTER, SUMMARIZE, COMMENT, PLAN, TRANSFORM).[^4]
- Placebo pipes act as meta-markers, deferring or flagging logic for staged or conditional execution, rather than immediate action.[^5][^4]


### Syntax and Semantics

- Pipelines (PLAN) sequence actions, allowing for nested, composable reasoning episodes. Each PLAN stage can invoke subordinate reasoning blocks, which resolve as atomic cognitive units.[^3][^5]
- Nested PLANs have strict lifecycle containment: execution begins when invoked and completes before the parent stage advances. Inputs and outputs are explicitly bound; state isolation is enforced.[^3][^5]
- Role scoping is explicit and local. Roles within a nested PLAN do not inherit from parents, ensuring cognitive perspective, not authority, is modified.[^5][^3]


### Standard Specification Outline

- **Roles:** Cognitive stances with parameterization (e.g., ResearcherDepthHigh, StorytellerToneEpic, PlannerGranularityFine).[^4]
- **Action Verbs:**
    - Knowledge Access: FIND, LIST, DETAIL
    - Knowledge Structuring: LINK, MAP, CLUSTER
    - Knowledge Transformation: SUMMARIZE, COMPARE, EXPLAIN
    - Meta Operations: COMMENT, PLAN, TRANSFORM[^5][^4]
- **Pipelines:** Sequences of actions, supporting nested and conditional PLAN blocks.[^3][^5]
- **Placebo Pipes:** Deferred or conditional steps, used for traceable, modular workflows.[^4][^5]
- **Typing and Introspection:** PLANs are typed functions over structured contexts, with introspection metadata for traceability and debugging.[^3][^5]


### Example Pipeline

```
rolePlanner PLAN PipelineMain
  Stage1Prep FIND EntityContext context
  Stage2Nested roleSubPlanner PLAN PipelineSub context
  Stage3Synth SUMMARIZE PipelineSub output
```

This demonstrates layered cognition, with each stage delegating to a subordinate reasoning block and consuming its outputs declaratively.[^5][^3][^4]

KickLang’s standard specification thus enables robust, transparent, and modular orchestration of cognitive workflows, making it a living manual for collective reasoning and knowledge synthesis.[^2][^3][^4][^5]
<span style="display:none">[^1][^10][^11][^12][^13][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: kicklang-synthesis-objective-m-R_dnjarHQxOY8hblQMCb0A.md

[^2]: One-liner-about-KickLang.md

[^3]: this-is-solid-and-more-than-th-3FjwxRxoTDifMknLoT89qw.md

[^4]: Absolutely-lets-take-that-outline-and-turn-it-i.pdf

[^5]: https://github.com/sgl-project/sglang/issues/166

[^6]: https://www.facebook.com/groups/autokrosas/posts/8186035444785637/

[^7]: https://search-prod.lis.state.oh.us/api/v2/general_assembly_132/legislation/sb268/04_PH/pdf/

[^8]: https://www.reddit.com/r/wow/comments/1odq0nr/latest_alpha_build_removes_interrupts_from_healers/

[^9]: https://www.digifind-it.com/summit/DATA/newspapers/herald/1966/1966-10-27.pdf

[^10]: http://hpsclab.uniparthenope.it/pdf/NGuida_Tesi.pdf

[^11]: https://www.lsc.ohio.gov/assets/organizations/legislative-service-commission/files/digest-of-2018-enactments.pdf

[^12]: https://www.reddit.com/r/JRPG/comments/1fjf7da/freedom_wars_remastered_announcement_trailer/

[^13]: https://www.reddit.com/r/ProgrammingLanguages/comments/f8jp74/writing_specs_for_your_languages/

