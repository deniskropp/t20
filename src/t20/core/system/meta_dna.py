"""Meta-DNA persistence layer for enrailed Unified MetaForge runs on t20.

Provides append-only logging of rail events, hybrid scores, and consent actions.
This module is intentionally lightweight and non-breaking.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class MetaDNA:
    """Persistent Meta-DNA logger for enrailed Unified MetaForge / OCS runs."""

    def __init__(self, session_id: str, base_path: Optional[Path] = None):
        self.session_id = session_id
        if base_path is None:
            # Default location mirrors t20 session structure
            self.base_path = Path("sessions") / session_id / ".meta-dna"
        else:
            self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.log_file = self.base_path / "rail_log.jsonl"

    def log_rail_event(
        self,
        rail: int,
        event: str,
        data: Optional[Dict[str, Any]] = None,
        hybrid_score: Optional[float] = None,
    ) -> None:
        """Log a rail transition or significant event."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "rail": rail,
            "event": event,
            "data": data or {},
            "hybrid_score": hybrid_score,
        }
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_rail_history(self) -> List[Dict[str, Any]]:
        """Return all logged rail events for this session."""
        if not self.log_file.exists():
            return []
        history: List[Dict[str, Any]] = []
        with self.log_file.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        history.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return history

    def get_latest_score(self) -> Optional[float]:
        """Return the most recent hybrid score recorded."""
        history = self.get_rail_history()
        for entry in reversed(history):
            if entry.get("hybrid_score") is not None:
                return entry["hybrid_score"]
        return None
