<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# extend this spec fragment into a formalized section of the KickLang standard

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

