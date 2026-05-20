# metaforge/forge_spawner.py
"""
ForgeSpawner: Universal sub-forge spawning capability.
Allows T20 to spawn full research / code / workflow / story / custom / swarm forges.
"""

from typing import Any, Dict, Optional

class ForgeSpawner:
    """Spawns child forges while maintaining parent Meta-DNA and traceability."""

    def __init__(self, parent_session: str = "default"):
        self.parent_session = parent_session
        self.spawned_forges: List[Dict] = []

    def spawn_forge(self, forge_type: str, goal: str, inherit_meta_dna: bool = True, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Spawn a new sub-forge."""
        valid_types = ["research", "code", "workflow", "story", "custom", "swarm"]
        if forge_type not in valid_types:
            forge_type = "custom"

        child_forge = {
            "forge_type": forge_type,
            "goal": goal,
            "parent_session": self.parent_session,
            "inherit_meta_dna": inherit_meta_dna,
            "status": "spawned",
            "id": f"forge-{forge_type}-{len(self.spawned_forges)+1}",
            "context": context or {}
        }
        self.spawned_forges.append(child_forge)
        return child_forge

    def get_spawned_forges(self) -> List[Dict]:
        return self.spawned_forges

    def receive_results(self, forge_id: str, results: Any) -> bool:
        """Receive results back from a child forge."""
        for f in self.spawned_forges:
            if f["id"] == forge_id:
                f["status"] = "completed"
                f["results"] = results
                return True
        return False
