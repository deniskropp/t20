# Example Runtime Integration Hooks for T20

## Recommended minimal hooks (non-breaking)

### 1. In CLI (src/t20_cli/main.py or equivalent)

```python
# Add to argument parser
parser.add_argument("--metaforge", action="store_true", help="Run goal with Unified MetaForge v1.0 (3-core + Meta-DNA + scoring)")
parser.add_argument("--spawn-forge", type=str, choices=["research", "code", "workflow", "story", "custom", "swarm"], help="Spawn a sub-forge")

# In execution
if args.metaforge or args.spawn_forge:
    from metaforge import MetaForgeRuntime
    runtime = MetaForgeRuntime(session_id=session_id)
    if args.spawn_forge:
        result = runtime.spawn_sub_forge(args.spawn_forge, task)
    else:
        result = runtime.run_with_metaforge(task, context={"files": args.files})
    print(result)
else:
    # original T20 flow
```

### 2. Lightweight hook in orchestrator / plan generation

```python
# In your plan generation or TAS step
try:
    from metaforge.kick_forge import KickForge
    from metaforge.meta_dna import MetaDNA
    kick_forge = KickForge()
    purified = kick_forge.extract_tas(goal)  # or enhance existing
    # score etc.
except ImportError:
    pass  # graceful fallback
```

See META_INTEGRATION_GUIDE.md for full details.