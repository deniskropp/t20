# metaforge/hybrid_scorer.py
"""
HybridScorer: Primary quality metric combining Consistency + Engagement + Safety + Traceability + Modularity
For T20 + Unified MetaForge v1.0
"""

from typing import Any, Dict, Optional

class HybridScorer:
    """Computes hybrid score for plans, sessions, and forges."""

    def __init__(self):
        self.weights = {
            "consistency": 0.25,
            "engagement": 0.20,
            "safety": 0.20,
            "traceability": 0.15,
            "modularity": 0.10,
            "meta_dna_quality": 0.10
        }

    def score(self, plan: Dict, trace: Optional[List] = None, meta_dna: Optional[Dict] = None) -> Dict[str, Any]:
        """Compute hybrid score and breakdown."""
        # Simplified scoring logic (in real use, analyze actual artifacts)
        consistency = 0.88
        engagement = 0.85
        safety = 0.92
        traceability = 0.90
        modularity = 0.87
        meta_dna_q = 0.80 if meta_dna else 0.70

        total = (
            consistency * self.weights["consistency"] +
            engagement * self.weights["engagement"] +
            safety * self.weights["safety"] +
            traceability * self.weights["traceability"] +
            modularity * self.weights["modularity"] +
            meta_dna_q * self.weights["meta_dna_quality"]
        )

        return {
            "hybrid_score": round(total, 2),
            "breakdown": {
                "consistency": consistency,
                "engagement": engagement,
                "safety": safety,
                "traceability": traceability,
                "modularity": modularity,
                "meta_dna_quality": meta_dna_q
            },
            "weights": self.weights,
            "version": "1.0.0-t20"
        }

    def update_weights(self, new_weights: Dict):
        self.weights.update(new_weights)
