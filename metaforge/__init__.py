"""
T20 + Unified MetaForge v1.0 Adapter Layer
Provides 3-core delegation (KickForge / KickFlow / KickGuard),
persistent Meta-DNA, hybrid scoring, and universal sub-forge spawning.
"""

from .meta_dna import MetaDNA
from .hybrid_scorer import HybridScorer
from .kick_forge import KickForge
from .kick_flow import KickFlow
from .kick_guard import KickGuard
from .forge_spawner import ForgeSpawner

__version__ = "1.0.0-t20"
__all__ = [
    "MetaDNA",
    "HybridScorer",
    "KickForge",
    "KickFlow",
    "KickGuard",
    "ForgeSpawner",
]