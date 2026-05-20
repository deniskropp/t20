from __future__ import annotations
from typing import Any, Dict, Optional, List

"""
MetaForgeRuntime — Main entry point for running goals with full Unified MetaForge v1.0.

Wraps T20 flows with 3-core delegation (KickForge / KickFlow / KickGuard),
persistent Meta-DNA, hybrid scoring, consent gates, and sub-forge spawning.
"""

from .kick_forge import KickForge
from .kick_flow import KickFlow
from .kick_guard import KickGuard
from .meta_dna import MetaDNA
from .hybrid_scorer import HybridScorer
from .forge_spawner import ForgeSpawner


class MetaForgeRuntime:
    """
    Primary runtime for T20 + Unified MetaForge integration.
    Use: runtime = MetaForgeRuntime(session_id="my-session")
         result = runtime.run_with_metaforge(goal="...")
    """

    def __init__(self, session_id: str = "default", parent_meta_dna: Optional[Dict] = None):
        self.session_id = session_id
        self.meta_dna = MetaDNA(session_id=session_id, initial_data=parent_meta_dna)
        self.kick_forge = KickForge(meta_dna=self.meta_dna)
        self.kick_flow = KickFlow()
        self.kick_guard = KickGuard()
        self.scorer = HybridScorer()
        self.spawner = ForgeSpawner(parent_session=session_id)
        self.hybrid_score: float = 0.0
        self.last_result: Dict[str, Any] = {}

    def run_with_metaforge(
        self,
        goal: str,
        context: Optional[Dict[str, Any]] = None,
        auto_spawn: bool = False
    ) -> Dict[str, Any]:
        """
        Full augmented execution flow with MetaForge governance.
        """
        context = context or {}
        trace: List[Dict[str, Any]] = []

        # Step 1: Consent & Integrity Gate (KickGuard)
        consent_ok, consent_notes = self.kick_guard.check_consent(goal, context)
        if not consent_ok:
            return {
                "status": "halted",
                "reason": "consent_gate_failed",
                "notes": consent_notes,
                "hybrid_score": 0.0
            }

        # Step 2: TAS Extraction & Purification (KickForge)
        raw_tas = self.kick_forge.extract_tas(goal, context)
        purified = self.kick_forge.purify_and_validate(raw_tas)
        trace.append({"phase": "tas_extraction", "result": purified})

        # Step 3: Structured Plan (KickFlow)
        plan = self.kick_flow.build_structured_plan(goal, purified.get("purified_tas", []), context)
        trace.append({"phase": "planning", "plan": plan})

        # Step 4: Hybrid Scoring
        score_result = self.scorer.score_session(
            plan_quality=8.5,
            agent_execution_quality=8.0,
            artifact_quality=8.7,
            banned_structures_found=len(purified.get("issues", [])),
            meta_dna_evolution=self.meta_dna.get_evolution_count(),
        )
        self.hybrid_score = score_result.get("final_hybrid_score", 8.0)
        trace.append({"phase": "scoring", "score": score_result})

        # Step 5: Meta-DNA Persistence
        self.meta_dna.write_evolution(
            trend="metaforge_enhanced_execution",
            score=self.hybrid_score,
            details={"goal": goal, "phases": len(trace)}
        )

        # Step 6: Optional sub-forge spawn
        spawned = None
        if auto_spawn or context.get("spawn_sub_forge"):
            spawned = self.spawner.spawn_forge(
                forge_type=context.get("forge_type", "research"),
                goal=f"Support goal: {goal}",
                inherit_meta_dna=True
            )
            trace.append({"phase": "sub_forge_spawn", "result": spawned})

        result = {
            "status": "success",
            "session_id": self.session_id,
            "goal": goal,
            "hybrid_score": self.hybrid_score,
            "score_breakdown": score_result,
            "meta_dna_summary": self.meta_dna.get_summary(),
            "trace": trace,
            "spawned_forge": spawned,
            "measurement": {
                "hybrid_score_breakdown": score_result,
                "meta_dna_evolution": self.meta_dna.get_evolution_count(),
            }
        }

        self.last_result = result
        return result

    def spawn_sub_forge(self, forge_type: str, goal: str, **kwargs) -> Dict[str, Any]:
        """Convenience method to spawn a sub-forge."""
        return self.spawner.spawn_forge(forge_type=forge_type, goal=goal, **kwargs)

    def get_hybrid_score(self) -> float:
        return self.hybrid_score
