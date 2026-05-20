"""
Meta-DNA — Persistent memory and evolution tracking for T20 + Unified MetaForge sessions.
Stores lineage, banned structures avoided, hybrid scores, cross-session learnings.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


class MetaDNA:
    def __init__(self, session_id: str, base_path: str = "sessions"):
        self.session_id = session_id
        self.base_path = base_path
        self.dna_path = os.path.join(base_path, session_id, "meta_dna.json")
        self.data: Dict[str, Any] = {
            "version": "1.0.0-t20",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "last_updated": None,
            "lineage": "T20 + Unified MetaForge v1.0",
            "archetype": "hybrid",
            "domain": "multi-agent-orchestration-framework",
            "all_time_trend": "evolving_from_specialized_to_universal",
            "banned_structures_avoided": [],
            "hybrid_scores": [],
            "evolution_notes": [],
            "cross_session_learnings": [],
            "meta_iterations": 0,
            "consent_level": "hybrid-confirmed",
        }
        self._ensure_dir()
        self._load_or_init()

    def _ensure_dir(self):
        os.makedirs(os.path.dirname(self.dna_path), exist_ok=True)

    def _load_or_init(self):
        if os.path.exists(self.dna_path):
            with open(self.dna_path, "r") as f:
                self.data.update(json.load(f))
        else:
            self._save()

    def _save(self):
        self.data["last_updated"] = datetime.utcnow().isoformat() + "Z"
        with open(self.dna_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def record_score(self, score: float, notes: str = ""):
        self.data["hybrid_scores"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "score": score,
            "notes": notes
        })
        self._save()

    def add_evolution_note(self, note: str):
        self.data["evolution_notes"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "note": note
        })
        self._save()

    def avoid_banned_structure(self, structure: str):
        if structure not in self.data["banned_structures_avoided"]:
            self.data["banned_structures_avoided"].append(structure)
        self._save()

    def increment_meta_iteration(self):
        self.data["meta_iterations"] += 1
        self._save()

    def add_cross_session_learning(self, learning: str):
        self.data["cross_session_learnings"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "learning": learning
        })
        self._save()

    def get_summary(self) -> Dict[str, Any]:
        scores = [s["score"] for s in self.data["hybrid_scores"]]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        return {
            "session_id": self.session_id,
            "meta_iterations": self.data["meta_iterations"],
            "avg_hybrid_score": round(avg_score, 2),
            "banned_avoided_count": len(self.data["banned_structures_avoided"]),
            "evolution_notes_count": len(self.data["evolution_notes"]),
            "last_updated": self.data["last_updated"],
        }

    def to_dict(self) -> Dict[str, Any]:
        return self.data.copy()
