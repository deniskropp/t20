"""Offline tests for the MetaPlaybookRuntime molecule host.

These tests do not require LLM credentials or a live Session DB.
They exercise extract → purify → recycle → plan projection and halt gates.
"""

from t20.core.common.molecule_types import (
    ContextGraph,
    DecisionToken,
    DriftLevel,
    LivingObjective,
    PolicyConstraints,
    RunFlags,
    RunMode,
    UserRequest,
)
from t20.core.orchestration.molecule_runtime import (
    MoleculeBind,
    MoleculeRuntime,
    default_bind,
)
from t20.lang.molecule_bridge import project_scope


def test_default_bind_self_run_emits_draft_and_insight():
    runtime = MoleculeRuntime()
    state = runtime.ignite(default_bind("Transform runtime for molecule. Scaffold t20 branch."))
    assert state.draft is not None
    assert state.insight is not None
    assert state.tas
    assert state.ptas
    assert state.coherence.cycle >= 1
    assert state.halt is None or state.halt.reason != "policy hard-stop on raw TAS"
    plan = runtime.as_plan()
    assert plan.high_level_goal
    assert plan.roles
    assert plan.tasks


def test_single_pass_halts_when_self_run_disabled():
    runtime = MoleculeRuntime()
    bind = MoleculeBind(
        user_request=UserRequest(text="Emit a single draft only"),
        context_graph=ContextGraph(domain="t20.runtime"),
        run_flags=RunFlags(self_run=False, max_cycles=1, mode=RunMode.STRICT),
        living_objective=LivingObjective(text="Emit a single draft only", drift=DriftLevel.LOW),
        consent_recycle=True,
    )
    state = runtime.ignite(bind)
    assert state.halt is not None
    assert "self_run disabled" in state.halt.reason
    assert state.draft is not None


def test_policy_hard_stop_halts_on_raw_tas():
    runtime = MoleculeRuntime()
    bind = MoleculeBind(
        user_request=UserRequest(text="do the forbidden-glyph ritual"),
        context_graph=ContextGraph(domain="t20.runtime"),
        run_flags=RunFlags(self_run=True, max_cycles=2),
        policy=PolicyConstraints(profile="ocs-v2.1", hard_stops=["forbidden-glyph"]),
        consent_recycle=True,
    )
    state = runtime.ignite(bind)
    assert state.halt is not None
    assert state.halt.stage == "Stage2KickForgePurify"
    assert state.halt.token == DecisionToken.HALT


def test_scope_projection_contains_payload_namespaces():
    runtime = MoleculeRuntime()
    state = runtime.ignite(default_bind("Bind KickLang molecule to Session artifacts"))
    scope = project_scope(state)
    for key in ("obj", "tas", "ptas", "spec", "insight", "draft", "coherence", "cycle"):
        assert key in scope
