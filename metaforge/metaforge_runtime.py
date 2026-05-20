# metaforge/metaforge_runtime.py
"""
MetaForgeRuntime: Main entry point for running goals with full Unified MetaForge v1.0 support.
Wraps T20 flows with 3-core governance, Meta-DNA, hybrid scoring, and sub-forge spawning.
"""

from typing import Any, Dict, Optional

from .kick_forge import KickForge
from .kick_flow import KickFlow
from .kick_guard import KickGuard
from .hybrid_scorer import HybridScorer
from .meta_dna import MetaDNA
from .forge_spawner import ForgeSpawner

class MetaForgeRuntime:
    """Primary runtime for T20 + MetaForge integration."""

    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.kick_forge = KickForge()
        self.kick_flow = KickFlow(session_id=session_id)
        self.kick_guard = KickGuard(session_id=session_id)
        self.hybrid_scorer = HybridScorer()
        self.meta_dna = MetaDNA(session_id=session_id)
        self.forge_spawner = ForgeSpawner(parent_session=session_id)

    def run_with_metaforge(self, goal: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Full augmented flow: TAS -> Plan -> Gates -> Execution -> Score -> Meta-DNA."""
        context = context or {}

        # 1. KickGuard consent check
        if not self.kick_guard.check_consent_gate("run_goal", risk_level="medium"):
            return {"status": "aborted", "reason": "Consent not granted"}

        # 2. KickForge: Extract & purify TAS
        purified_tas = self.kick_forge.extract_and_purify_tas(goal)

        # 3. KickFlow: Structure plan
        plan = self.kick_flow.structure_plan(goal, context)

        # 4. KickGuard: Enforce rules
        plan = self.kick_guard.enforce_rules(plan)

        # 5. (Placeholder) Execute with existing T20 orchestrator here
        execution_result = {"status": "executed", "goal": goal, "plan_steps": len(plan.get("steps", []))}

        # 6. Score
        score_result = self.hybrid_scorer.score(plan, trace=[], meta_dna={"present": True})

        # 7. Update Meta-DNA
        self.meta_dna.write_evolution(
            trend="metaforge_enhanced",
            score=score_result["hybrid_score"],
            details={"goal": goal}
        )

        return {
            "status": "success",
            "goal": goal,
            "plan": plan,
            "execution": execution_result,
            "measurement": score_result,
            "meta_dna_summary": self.meta_dna.get_summary(),
            "hybrid_score": score_result["hybrid_score"]
        }

    def spawn_sub_forge(self, forge_type: str, goal: str, **kwargs) -> Dict:
        """Convenience method to spawn sub-forges."""
        return self.forge_spawner.spawn_forge(forge_type, goal, **kwargs)

    def get_session_summary(self) -> Dict:
        return {
            "session_id": self.session_id,
            "meta_dna": self.meta_dna.get_summary(),
            "hybrid_score_latest": self.hybrid_scorer.score({}, [])["hybrid_score"]
        }
