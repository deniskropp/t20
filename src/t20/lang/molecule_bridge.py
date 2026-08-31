"""Bridge t20.lang.runtime.ExecutionContext with the molecule payload bus.

runtime_gen.kl ExecutionContext (session, plan, artifacts) and
lang.runtime.ExecutionContext (scope, artifacts) are two historical
surfaces. This module projects MoleculeState into both without breaking
either executor.
"""

from __future__ import annotations

from typing import Any, Dict

from t20.core.common.molecule_types import MoleculeState


def project_scope(state: MoleculeState) -> Dict[str, Any]:
    """Map data/* namespaces onto lang.runtime.ExecutionContext.scope keys."""
    return {
        "obj": state.obj,
        "tas": [t.model_dump() for t in state.tas],
        "ptas": [p.model_dump() for p in state.ptas],
        "spec": state.spec.model_dump(),
        "state": state.state,
        "logic": list(state.logic),
        "insight": state.insight.model_dump() if state.insight else None,
        "draft": state.draft.model_dump() if state.draft else None,
        "consensus": state.consensus,
        "coherence": state.coherence.model_dump(),
        "cycle": state.cycle,
        "mode": state.mode.value if hasattr(state.mode, "value") else state.mode,
        "halt": state.halt.model_dump() if state.halt else None,
    }


def apply_scope(lang_ctx: Any, state: MoleculeState) -> None:
    """Write molecule payloads into a lang.runtime.ExecutionContext."""
    for key, value in project_scope(state).items():
        if hasattr(lang_ctx, "set"):
            lang_ctx.set(key, value)
        if hasattr(lang_ctx, "artifacts") and isinstance(lang_ctx.artifacts, dict):
            lang_ctx.artifacts[f"data/{key}"] = value
