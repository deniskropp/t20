"""Molecule-facing runtime types that bind KickLang MetaPlaybookRuntime to t20.

These models sit *beside* the existing Plan/Task/Role/AgentOutput types
(runtime_gen.kl / t20.core.common.types) rather than replacing them.
They carry the klmx payload namespaces used by the self-running molecule.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RunMode(str, Enum):
    STRICT = "Strict"
    CREATIVE = "Creative"
    FLUID = "Fluid"
    SWARM = "Swarm"
    SWARMF = "SwarmF"
    HYBRID = "Hybrid"


class DriftLevel(str, Enum):
    LOW = "low"
    MED = "med"
    HIGH = "high"


class DecisionToken(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    HALT = "HALT"
    REVIEW = "REVIEW"


class UserRequest(BaseModel):
    text: str
    locale: Optional[str] = None


class ContextGraph(BaseModel):
    domain: str
    refs: List[str] = Field(default_factory=list)


class RunFlags(BaseModel):
    mode: RunMode = RunMode.HYBRID
    ruleset: Optional[str] = "ocs-v2.1"
    visual: bool = False
    self_run: bool = True
    max_cycles: int = 3
    microcycle_on_stable_spec: bool = True


class PolicyConstraints(BaseModel):
    profile: str = "ocs-v2.1"
    hard_stops: List[str] = Field(default_factory=list)


class LivingObjective(BaseModel):
    text: str
    valence: Optional[float] = 0.8
    drift: DriftLevel = DriftLevel.LOW


class CoherenceReport(BaseModel):
    coherence: float = 0.0
    drift: DriftLevel = DriftLevel.MED
    valence: float = 0.0
    cycle: int = 0
    integrity: str = "OK"
    notes: str = ""


class MoleculeTAS(BaseModel):
    """Task-Agnostic Step extracted from a user request / living objective."""

    tas_id: str
    text: str
    source: str = "user_request"
    traits: List[str] = Field(default_factory=list)


class MoleculePTAS(BaseModel):
    """Purified TAS after policy and consent gates."""

    ptas_id: str
    text: str
    source_tas: str
    purified: bool = True


class MoleculeSpec(BaseModel):
    """Pipeline specification produced by KickFlow structure/delegate stages."""

    horizon: str = "single-pass"
    style: str = "hybrid-ocs"
    stages: List[str] = Field(default_factory=list)
    stable: bool = False
    notes: str = ""


class MoleculeInsight(BaseModel):
    cycle: int
    summary: str
    tas_count: int = 0
    ptas_count: int = 0
    spec_stable: bool = False


class MoleculeDraft(BaseModel):
    cycle: int
    body: str
    consensus: bool = True


class MoleculeHalt(BaseModel):
    reason: str
    stage: str
    cycle: int
    token: DecisionToken = DecisionToken.HALT


class MoleculeState(BaseModel):
    """Session-local molecule bus — maps data/* namespaces."""

    obj: str = ""
    tas: List[MoleculeTAS] = Field(default_factory=list)
    ptas: List[MoleculePTAS] = Field(default_factory=list)
    spec: MoleculeSpec = Field(default_factory=MoleculeSpec)
    state: Dict[str, Any] = Field(default_factory=dict)
    logic: List[str] = Field(default_factory=list)
    insight: Optional[MoleculeInsight] = None
    draft: Optional[MoleculeDraft] = None
    consensus: Optional[str] = None
    conflict: List[str] = Field(default_factory=list)
    coherence: CoherenceReport = Field(default_factory=CoherenceReport)
    halt: Optional[MoleculeHalt] = None
    cycle: int = 0
    mode: RunMode = RunMode.HYBRID
    decision: DecisionToken = DecisionToken.ALLOW
    monitor_integrity: str = "OK"
    spec_stable: bool = False
