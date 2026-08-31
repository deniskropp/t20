# t20 KickLang molecules

| File | Role |
|------|------|
| `HOST.kicklang` | t20 host binding (Session, Plan, Meta-DNA, halt gates) |
| `klmx-meta-playbook-molecule.kicklang` | Canonical MetaPlaybookRuntime v1.0 (20-stage lattice + recycle) |
| `runtime_gen.kl` | KickLang concept graph of the historical runtime |

Python host: `t20.core.orchestration.molecule_runtime.MoleculeRuntime`

Ignition:

```python
from t20.core.orchestration.molecule_runtime import MoleculeRuntime, default_bind
state = MoleculeRuntime().ignite(default_bind("<living objective>"))
plan = MoleculeRuntime().as_plan()  # after ignite on same instance
```
