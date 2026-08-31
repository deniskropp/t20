# KLMX Molecule Runtime (t20)

Branch: `feature/klmx-molecule-runtime`

Transform of the existing multi-agent runtime so it can **host** the
self-running KickLang molecule `MetaPlaybookRuntime v1.0`.

## Intent

`runtime_gen.kl` is a KickLang concept graph of the historical runtime
(`types`, `agent`, `core`/`session`, `loader`, `llm`, `orchestrator`).
Those concepts already live in Python under `src/t20/core/*`.

This branch does **not** rewrite Agent/Orchestrator. It adds a molecule
host that:

1. Walks the 20-stage Meta-Playbook lattice.
2. Writes payload namespaces into `MoleculeState`.
3. Recycles `insight → obj` until convergence, max cycles, or halt.
4. Projects the result back onto `Plan` so `System` / `Pipeline` can consume it.
5. Optionally persists artifacts + Meta-DNA rail events on a live `Session`.

## Layout

```
src/t20/core/common/molecule_types.py          # payload schemas
src/t20/core/orchestration/molecule_runtime.py # 20-stage host + recycle kernel
src/t20/lang/molecule_bridge.py                # lang.runtime.ExecutionContext projection
src/t20/kicklang/molecules/
  klmx-meta-playbook-molecule.kicklang         # canonical molecule
  runtime_gen.kl                               # runtime concept graph
tests/test_molecule_runtime.py
```

## Concept map (runtime_gen.kl → t20)

| KickLang concept     | Python host                                      |
|----------------------|--------------------------------------------------|
| Role / Task / Plan   | `t20.core.common.types`                          |
| Artifact             | `types.Artifact` + `Session.add_artifact`        |
| Agent                | `t20.core.agents.agent.Agent`                    |
| Orchestrator         | `t20.core.orchestration.orchestrator.Orchestrator` |
| ExecutionContext     | `t20.core.system.session.ExecutionContext`       |
| Session              | `t20.core.system.session.Session` (+ MetaDNA)    |
| LLM / Gemini / Olli / Kimi | `t20.core.agents.llm.LLM`                  |
| LoadConfig / templates | `t20.core.common.loader`                       |

## Ignition

```python
from t20.core.orchestration.molecule_runtime import MoleculeRuntime, default_bind

runtime = MoleculeRuntime(session=session)  # session optional
state = runtime.ignite(default_bind("Convert Meta-Playbook into self-running molecule"))
plan = runtime.as_plan()
```

Halt gates (KickGuard-present):

- Stage 2 — policy `hard_stops` on raw TAS
- Stage 10 — ethical non-consent
- Stage 16 — joint-decision / integrity FAIL
- Stage 17 — coherence floor `< 0.72`
- Kernel — high drift, unresolved conflict, missing first-recycle consent

## Convergence

`coherence >= 0.90` AND `drift == low` AND no conflict AND draft present.

Max cycles default `3`. Microcycle (Stage 15 orbit) when spec is stable.
