"""
KickForge — TAS Extraction, Purification, Validation & Measurement.
Adapts T20's existing GPTASe / uTASe layer with MetaForge discipline.
"""

from typing import List, Dict, Any, Optional
from .hybrid_scorer import HybridScorer
from .meta_dna import MetaDNA


class KickForge:
    def __init__(self, meta_dna: Optional[MetaDNA] = None):
        self.meta_dna = meta_dna or MetaDNA("default")
        self.scorer = HybridScorer()
        self.banned_structures = [
            "circular_dependency_without_guard",
            "missing_consent_gate",
            "hardcoded_agent_names",
            "no_persist_layer",
            "plot_holes_unresolved",
        ]

    def extract_tas(self, goal: str, context: Dict[str, Any] = None) -> List[str]:
        """
        Enhanced TAS extraction.
        In real integration, this would call/enhance T20's existing TAS logic.
        """
        # Placeholder: In production, delegate to or wrap T20's GPTASe / uTASe
        base_steps = [
            f"Analyze goal: {goal}",
            "Break into Task-Agnostic Steps (TAS)",
            "Identify required agent roles",
            "Generate execution plan",
            "Validate plan against banned structures",
            "Execute with traceability",
            "Score & persist Meta-DNA",
        ]
        if context and context.get("complex"):
            base_steps.insert(2, "Perform deep domain research")
            base_steps.append("Spawn sub-forge if goal complexity high")
        return base_steps

    def purify_and_validate(self, tas_list: List[str]) -> Dict[str, Any]:
        """Purify TAS list and check for banned structures."""
        purified = [step.strip() for step in tas_list if step.strip()]
        issues = []

        for banned in self.banned_structures:
            if any(banned in str(step).lower() for step in purified):
                issues.append(banned)
                self.meta_dna.avoid_banned_structure(banned)

        return {
            "purified_tas": purified,
            "banned_issues_found": issues,
            "clean": len(issues) == 0,
        }

    def measure_and_score(self, plan: Dict[str, Any], execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Run hybrid scoring and record in Meta-DNA."""
        score_result = self.scorer.score_session(
            plan_quality=plan.get("quality", 8.0),
            agent_execution_quality=execution_results.get("avg_agent_quality", 8.0),
            artifact_quality=execution_results.get("artifact_quality", 8.5),
            banned_structures_found=len(execution_results.get("issues", [])),
            traceability_score=9.0,
            modularity_notes="adapter_layer",
        )

        final_score = score_result["final_hybrid_score"]
        self.meta_dna.record_score(final_score, "KickForge measurement")

        return {
            "hybrid_score_breakdown": score_result,
            "meta_dna_summary": self.meta_dna.get_summary(),
        }

    def validate_forge_candidate(self, candidate: Dict[str, Any]) -> bool:
        """Quick validation for any proposed sub-forge or plan."""
        if candidate.get("contains_banned", False):
            return False
        if candidate.get("hybrid_score", 0) < 7.0:
            return False
        return True
