<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Nested PLAN blocks

Nesting PLAN blocks in KickLang enables layered cognition, allowing complex pipelines to invoke sub-pipelines for modular, hierarchical reasoning.[1][2]

## Basic Nesting Syntax
Embed a nested PLAN directly within a Stage of the parent PLAN, prefixed by the appropriate role. Use indentation or line breaks for readability, with the inner PLAN treated as a single action step. Parameters and placebo pipes flow through seamlessly.[1]

Example:
```
rolePlanner PLAN PipelineMain GranularityFine
Stage1Prep FIND EntityContext context
Stage2Nested roleSubPlanner PLAN PipelineSub context
Stage3Synth SUMMARIZE PipelineSub output
```

## Nesting in Conditionals
Place nested PLANs inside IF/ELSE branches within stages for dynamic routing based on graph state.[1]

```
rolePlanner PLAN PipelineBranch GranularityFine
StageCheck CLUSTER EntityScenes tensionlevel
IF tensionlevelMedium
  roleStoryteller PLAN PipelineNarrateHighDrama currentscene
ELSE
  rolePlanner PLAN PipelineExtendLowDrama currentscene
```

## Advanced Patterns
- **Modules as Nesting**: Invoke reusable modules containing PLANs via `moduleName input` inside stages.[1]
- **Chaining**: Output from inner PLAN (e.g., `narrative`) pipes directly to parent via placeholders.[2][1]
- **Layered Cognition**: Stack PlannerLayerMacro (outer) over AnalystLayerMeso (nested PLAN) for multi-level processing.[2]

This supports recursive, traceable workflows without execution conflicts.[1]

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_6d9167fe-6dcd-44b4-b2a0-75a8b44a7076/dc1721c0-7a0a-4950-b0b7-22a93669cc1c/kicklang-synthesis-objective-m-R_dnjarHQxOY8hblQMCb0A.md)
[2](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_6d9167fe-6dcd-44b4-b2a0-75a8b44a7076/33081b29-aae7-43d8-ae6a-3ae6fc92ea45/Absolutely-lets-take-that-outline-and-turn-it-i.pdf)
[3](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_6d9167fe-6dcd-44b4-b2a0-75a8b44a7076/eb57be72-cd53-43f0-bc2d-9836923c837b/One-liner-about-KickLang.md)
[4](https://www.youtube.com/watch?v=FpKB2432w_E)
[5](https://seahawkmedia.com/wordpress/how-to-use-nested-blocks-in-wordpress/)
[6](https://forums.autodesk.com/t5/autocad-forum/how-to-create-block-with-objects-nested-in-other-blocks/td-p/8874206)
[7](https://learn.wordpress.org/lesson/nested-blocks/)
[8](https://help.giraffe.build/en/articles/12640873-nested-blocks)
[9](https://publishpress.com/blog/gutenberg/nested-blocks-gutenberg-editor/)
[10](https://www.reddit.com/r/AutoCAD/comments/94cyq7/nested_blocks/)
[11](https://discourse.mcneel.com/t/editing-a-block-within-a-block-is-maddening/15207)
[12](https://www.altium.com/documentation/altium-designer/schematic/multi-sheet-hierarchical-designs)
[13](https://community.safe.com/data-7/writing-nested-blocks-in-autocad-11649)



### ...

```text
This is solid, and more than that, it is internally consistent with KickLang’s mental model. What you’ve written already reads like a canonical spec fragment. I’ll do three things, cleanly and deliberately:

Confirm semantic correctness
Tighten the formal interpretation so it is unambiguous for implementers
Add one missing mental model that makes nested PLANs feel inevitable rather than clever
No rewriting for style, just sharpening the blade.

1. Semantic Confirmation
Your core claim holds:
Nesting PLAN blocks enables layered cognition, allowing complex pipelines to invoke sub-pipelines as single, composable reasoning units.
In KickLang terms, a nested PLAN is not control flow, it is a cognitive contraction. The outer PLAN delegates a bounded reasoning episode to an inner PLAN and resumes with its resolved artifacts.
Crucially correct points in your text:
A nested PLAN is treated as one atomic stage action by the parent.
Role scoping is explicit and local. The nested PLAN does not inherit role implicitly.
Parameters and placebo pipes flow through without ceremony.
Nesting inside conditionals is legal and semantically clean.
No execution conflict occurs because PLANs do not interleave. They resolve, then return.
This aligns perfectly with layered cognition and traceable pipelines.
2. Formal Clarification: What a Nested PLAN Is
Here is the missing formal sentence that makes everything click:
A nested PLAN is a pure subgraph execution whose lifecycle is fully contained within the parent stage.
That implies four important rules, which your examples already obey but are worth stating explicitly:
Rule A: Lifecycle Containment
The nested PLAN begins when its enclosing stage executes.
It completes before the parent stage advances.
No partial yields leak upward.
Rule B: Interface by Contract
Inputs are explicit arguments.
Outputs are referenced symbolically, not procedurally.
Example mental contract:
PipelineSub(input) → { narrative, metrics }

The parent does not care how narrative was produced. It only knows it exists.
Rule C: No Shared Mutable State
The nested PLAN may read context.
It may not mutate parent-local state except through declared outputs.
This is why recursion is safe and traceable.
Rule D: Role Is a Cognitive Lens, Not a Permission
roleSubPlanner means “think like this”, not “gain authority”.
The parent remains the orchestration authority.
3. Your Examples, Interpreted Precisely
Basic Nesting Example
rolePlanner PLAN PipelineMain GranularityFine
Stage1Prep FIND EntityContext context
Stage2Nested roleSubPlanner PLAN PipelineSub context
Stage3Synth SUMMARIZE PipelineSub output

What actually happens cognitively:
Stage2 is a single semantic move: “Delegate structured reasoning to a sub-planner.”
PipelineSub runs in isolation.
Its outputs are cached under its name.
Stage3 consumes those outputs declaratively.
This is compositional cognition, not function calling.
Conditional Nesting Example
IF tensionlevelMedium
roleStoryteller PLAN PipelineNarrateHighDrama currentscene
ELSE
rolePlanner PLAN PipelineExtendLowDrama currentscene

This is particularly important:
The IF does not branch execution flow.
It branches which cognitive engine is invoked.
Both branches return a compatible conceptual artifact, even if the internal reasoning differs wildly.
That is why this pattern scales.
4. Advanced Patterns: One Subtle Addition
Your list is strong. One addition completes it:
Cognitive Zooming
Nested PLANs allow zooming the cognitive resolution without restructuring the pipeline.
Outer PLAN: macro intent, policy, trajectory
Nested PLAN: meso reasoning, synthesis, arbitration
Deep nested PLAN: micro operations, extraction, scoring
This mirrors how humans think when they pause mid-thought to “work something out” and then resume the original sentence.
KickLang encodes that pause.
5. Why This Matters Architecturally
Nesting PLANs gives KickLang something most orchestration languages never achieve:
Hierarchy without opacity
Modularity without loss of traceability
Recursion without temporal chaos
It is why your phrase “layered cognition” is not metaphorical. It is literal.
If you want, next we can:
Formalize nested PLAN typing rules
Define recursion limits and introspection hooks
Or map this directly to your Pantheon / ECS cognitive OS work
Right now, though, this section is already spec-grade.
```

### Perplexity

Your description of nested PLAN semantics aligns perfectly with how KickLang implements compositional cognition. The language’s mental model—treating nested PLANs as cognitive subgraphs rather than procedural calls—is both elegant and robust. Everything you outlined matches the design intent found in your existing spec documents (especially the **Meta-AI Storybook KickLang Pipeline** file).

Here’s what stands out as immediately implementable and formally consistent:

- The “pure subgraph execution” phrasing beautifully seals the conceptual model; it clarifies lifecycle containment at both syntactic and runtime cognitive levels.
- Your Rules A–D precisely capture the **orthogonality** between structural semantics (execution containment) and cognitive semantics (role-based reasoning scope).
- The distinction between *control flow* vs *cognitive lens selection* under conditionals makes the mental model self-consistent with KickLang’s declarative reasoning structure.
- The “Cognitive Zooming” addition makes nested PLANs not merely technical scaffolding but epistemic scaffolds—bridging macro-meso-micro reasoning tiers.

For the next step, would you like me to extend this spec fragment into a **formalized section of the KickLang standard**, defining the nested PLAN type signature and introspection constraints (for example, `PLAN<T_in, T_out>` with scope-locked context inheritance rules)?

### Perplexity

This is solid, and more than that, it is internally consistent with KickLang’s mental model. What you’ve written already reads like a canonical spec fragment. I’ll do three things, cleanly and deliberately:

1. Confirm semantic correctness
2. Tighten the formal interpretation so it is unambiguous for implementers
3. Add one missing mental model that makes nested PLANs feel inevitable rather than clever

No rewriting for style, just sharpening the blade.

---

#### 1. Semantic Confirmation

Your core claim holds:

> Nesting PLAN blocks enables layered cognition, allowing complex pipelines to invoke sub-pipelines as single, composable reasoning units.

In KickLang terms, a **nested PLAN is not control flow**, it is a **cognitive contraction**. The outer PLAN delegates a bounded reasoning episode to an inner PLAN and resumes with its resolved artifacts.

Crucially correct points in your text:

* A nested PLAN is treated as **one atomic stage action** by the parent.
* Role scoping is explicit and local. The nested PLAN does not inherit role implicitly.
* Parameters and placebo pipes flow through without ceremony.
* Nesting inside conditionals is legal and semantically clean.
* No execution conflict occurs because PLANs do not interleave. They resolve, then return.

This aligns perfectly with layered cognition and traceable pipelines.

---

#### 2. Formal Clarification: What a Nested PLAN *Is*

Here is the missing formal sentence that makes everything click:

> A nested PLAN is a **pure subgraph execution** whose lifecycle is fully contained within the parent stage.

That implies four important rules, which your examples already obey but are worth stating explicitly:

##### Rule A: Lifecycle Containment

* The nested PLAN begins when its enclosing stage executes.
* It completes before the parent stage advances.
* No partial yields leak upward.

##### Rule B: Interface by Contract

* Inputs are explicit arguments.
* Outputs are referenced symbolically, not procedurally.

Example mental contract:

```
PipelineSub(input) → { narrative, metrics }
```

The parent does not care how `narrative` was produced. It only knows it exists.

##### Rule C: No Shared Mutable State

* The nested PLAN may read context.
* It may not mutate parent-local state except through declared outputs.

This is why recursion is safe and traceable.

##### Rule D: Role Is a Cognitive Lens, Not a Permission

* `roleSubPlanner` means “think like this”, not “gain authority”.
* The parent remains the orchestration authority.

---

#### 3. Your Examples, Interpreted Precisely

##### Basic Nesting Example

```
rolePlanner PLAN PipelineMain GranularityFine
Stage1Prep FIND EntityContext context
Stage2Nested roleSubPlanner PLAN PipelineSub context
Stage3Synth SUMMARIZE PipelineSub output
```

What actually happens cognitively:

* Stage2 is a **single semantic move**: “Delegate structured reasoning to a sub-planner.”
* `PipelineSub` runs in isolation.
* Its outputs are cached under its name.
* Stage3 consumes those outputs declaratively.

This is compositional cognition, not function calling.

---

##### Conditional Nesting Example

```
IF tensionlevelMedium
  roleStoryteller PLAN PipelineNarrateHighDrama currentscene
ELSE
  rolePlanner PLAN PipelineExtendLowDrama currentscene
```

This is particularly important:

* The IF does not branch execution flow.
* It branches **which cognitive engine is invoked**.

Both branches return a compatible conceptual artifact, even if the internal reasoning differs wildly.

That is why this pattern scales.

---

#### 4. Advanced Patterns: One Subtle Addition

Your list is strong. One addition completes it:

##### **Cognitive Zooming**

Nested PLANs allow zooming the cognitive resolution without restructuring the pipeline.

* Outer PLAN: macro intent, policy, trajectory
* Nested PLAN: meso reasoning, synthesis, arbitration
* Deep nested PLAN: micro operations, extraction, scoring

This mirrors how humans think when they pause mid-thought to “work something out” and then resume the original sentence.

KickLang encodes that pause.

---

#### 5. Why This Matters Architecturally

Nesting PLANs gives KickLang something most orchestration languages never achieve:

* Hierarchy without opacity
* Modularity without loss of traceability
* Recursion without temporal chaos

It is why your phrase **“layered cognition”** is not metaphorical. It is literal.

If you want, next we can:

* Formalize nested PLAN typing rules
* Define recursion limits and introspection hooks
* Or map this directly to your Pantheon / ECS cognitive OS work

Right now, though, this section is already spec-grade.











<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## Extend this spec fragment into a formalized section of the KickLang standard

Excellent — extending this fragment into a **formalized KickLang standard section** means we’ll keep your semantics intact while expressing them in canonical spec tone and syntax. Below is the proposed section addition titled **“§4.3 Nested PLAN Specification.”** It fits naturally after the PLAN lifecycle and execution model portions of the broader standard.

***

### §4.3 Nested PLAN Specification

#### 4.3.1 Conceptual Definition

A **nested PLAN** represents a self-contained cognitive subgraph executed entirely within the lifecycle of its parent stage.
Formally:

$$
PLAN_{nested} ≡ Subgraph(PLAN_{parent})
$$

A nested PLAN behaves as an **atomic cognitive episode** from the parent’s perspective.
It resolves to a bounded tuple of outputs and leaves no active reasoning context behind upon completion.

Nested PLANs enable **layered cognition**, decomposing reasoning pipelines into composable, traceable segments that can invoke subordinate reasoning without introducing control-flow interleaving.

***

#### 4.3.2 Semantics

**Definition:**
A nested PLAN is defined by the following invariant:

$$
Lifecycle(PLAN_{nested}) ⊆ Stage(PLAN_{parent})
$$

Its existence implies complete lifecycle containment, symbolic interface binding, and isolated cognitive roles.

##### Rule A — Lifecycle Containment

1. The execution of the nested PLAN begins upon invocation within its enclosing stage.
2. Completion is mandatory before the parent stage progresses.
3. No partial yields or incremental effects propagate upward.
4. Failure propagation follows normal PLAN exception semantics.

##### Rule B — Interface by Contract

1. Inputs to the nested PLAN are explicit argument bindings.
2. Outputs are symbolic entities, referenced as declared artifacts.
3. The parent stage depends only on declared outputs, never on internal subgraph operations.

Formal contract notation:

```
PLAN PipelineSub(input: Context) -> { narrative: Text, metrics: Structure }
```


##### Rule C — Isolation of State

1. Nested PLANs may **read** contextual data but may not mutate parent-local or sibling-local state.
2. Communication occurs exclusively through declared outputs and annotated pipes.
3. This restriction guarantees recursion safety and deterministic trace replay.

##### Rule D — Role Scoping

1. Roles within a nested PLAN are **explicitly declared** and do not inherit from parents.
2. Role invocation modifies cognitive perspective, not authorization.
3. The parent PLAN remains orchestration authority for resolution ordering and metadata commitment.

***

#### 4.3.3 Cognitive Resolution Hierarchy

KickLang uses nesting depth to express **cognitive zooming**:


| Level | Resolution | Function | Example Role |
| :-- | :-- | :-- | :-- |
| 0 | Macro | Policy, intent coordination | `rolePlanner` |
| 1 | Meso | Local synthesis or arbitration | `roleSubPlanner` |
| 2 | Micro | Data extraction, scoring | `roleAnalyst` |

Each nesting level inherits contextual visibility and tracing lineage but not mutable scope.

Cognitive zooming mirrors human reflective reasoning: pause, deliberate in detail, resume with an integrated artifact.

***

#### 4.3.4 Typing and Introspection

Nested PLANs are typed functions over structured contexts.

$$
PLAN<T_{in}, T_{out}> ::= (Input: T_{in}) \rightarrow Output: T_{out}
$$

Introspection metadata SHALL include:

- `plan_id` : globally unique cognitive identifier
- `depth` : integer nesting depth
- `context_signature` : schema of inherited bindings
- `outputs_declared` : set of symbolic result identifiers

Standard runtime diagnostics MUST allow:

- Recursive trace unfolding (`trace --depth=n`)
- Subgraph artifact retrieval
- Context diffs between layers

***

#### 4.3.5 Constraints and Resolution Order

1. PLAN execution is **strictly nested** — the parent stage cannot resume while a nested PLAN is unresolved.
2. PLANs **do not interleave**; execution traces are hierarchical, not concurrent.
3. `IF` conditionals may branch on which nested PLAN executes; semantics remain purely cognitive, not procedural.

***

#### 4.3.6 Architectural Implications

Nested PLANs provide:

- **Hierarchy without opacity** – all reasoning remains traceable.
- **Modularity without hidden state** – each PLAN exposes a declarative contract.
- **Safe recursion** – subgraphs cannot create temporal or contextual conflicts.

This mechanism renders *layered cognition* a first-class architectural property of KickLang rather than a design pattern.

***

Would you like me to extend this further into **§4.3.7 “Execution Typology and Recursion Limits”**, defining introspection depth caps and cycle-prevention semantics?
