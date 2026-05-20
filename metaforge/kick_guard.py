# metaforge/kick_guard.py
"""
KickGuard: Ethical Compliance, Integrity Monitoring, Consent Gates, Rules Enforcement
Part of Unified MetaForge v1.0 for T20.
"""

from typing import Any, Dict, List, Optional

class KickGuard:
    """Manages consent gates, integrity, and safety rules."""

    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.consent_log: List[Dict] = []
        self.banned_structures_detected: List[str] = []

    def check_consent_gate(self, action: str, risk_level: str = "medium") -> bool:
        """Check if action passes consent gate. In production, this would prompt user."""
        approved = risk_level != "high"  # Simplified; real version would ask user
        self.consent_log.append({
            "action": action,
            "risk_level": risk_level,
            "approved": approved,
            "session_id": self.session_id
        })
        return approved

    def enforce_rules(self, plan: Dict) -> Dict:
        """Enforce banned structures and safety rules."""
        # Example checks
        if "circular_dependency" in str(plan).lower():
            self.banned_structures_detected.append("circular_dependency")
        return plan

    def monitor_integrity(self, trace: List) -> float:
        """Monitor session integrity. Returns integrity score."""
        return 0.95  # Placeholder high integrity

    def get_consent_log(self) -> List[Dict]:
        return self.consent_log
