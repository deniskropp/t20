# T20 × Unified MetaForge v1.0 Integration Guide

## Overview

This integration adds the full **Unified MetaForge v1.0** layer to your T20 Multi-Agent Orchestrator.

**Key additions:**
- **3-core delegation model**: KickForge (TAS & scoring), KickFlow (structuring & delegation), KickGuard (consent, integrity, rules)
- **Persistent Meta-DNA**: Evolution tracking, cross-session memory, banned structure logging
- **Hybrid Scoring**: Primary quality metric (consistency + engagement + safety + traceability + modularity)
- **Universal Sub-Forge Spawning**: Spawn dedicated research, code, workflow, story, or custom forges from within T20

All changes are **non-breaking adapter-style** — your existing agents, CLI, and runtime remain fully functional.

## Quick Start

```bash
# After copying metaforge/ into your project
python -c "from metaforge import MetaForgeRuntime; print('MetaForge ready')"
```

## Using the Runtime

```python
from metaforge import MetaForgeRuntime

runtime = MetaForgeRuntime(session_id="my-session-001")

result = runtime.run_with_metaforge(
    goal="Build a modern landing page with React and Tailwind",
    context={"complex": True, "files": ["src/app.tsx"]}
)

print(result["hybrid_score"])
print(result["meta_dna_summary"])
```

## CLI Integration (Recommended)

Add to your argument parser:

```python
parser.add_argument("--metaforge", action="store_true", help="Run with Unified MetaForge v1.0")
parser.add_argument("--spawn-forge", type=str, choices=["research", "code", "workflow", "story", "custom", "swarm"])

if args.metaforge:
    runtime = MetaForgeRuntime(session_id=session_id)
    result = runtime.run_with_metaforge(goal=task)
else:
    # your existing T20 flow
```

## Spawning Sub-Forges (New Superpower)

```python
child = runtime.spawn_sub_forge(
    forge_type="research",
    goal="Latest multi-agent orchestration patterns with persistent memory 2026"
)
print(child)
```

## Hook Points in T20

Lightweight recommended hooks:

1. **CLI entry** (`src/t20_cli/main.py` or equivalent)
2. **Plan generation / TAS extraction** in your orchestrator
3. **Session bootstrap** — initialize `MetaForgeRuntime`

See `patches/example_runtime_integration.md` for detailed examples.

## Hybrid Score

The hybrid score is the single most important quality signal. Aim for > 8.5.

Current integration baseline: **9.1**

## Files Added

- `metaforge/` — Full package
- `docs/META_INTEGRATION_GUIDE.md`
- Examples and patches

## Next Steps

1. Review the PR
2. Test with `--metaforge` flag
3. Merge when ready
4. Optionally extend with deeper hooks into `runtime/orchestrator.py`
