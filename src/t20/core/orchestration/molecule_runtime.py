"""Transform the existing t20 runtime into a MetaPlaybookRuntime molecule host.

Binds:
  runtime_gen.kl concepts   -> t20.core.* classes
  MetaPlaybookRuntime v1.0  -> 20-stage lattice + recycle kernel

This adapter is LLM-optional. Stages emit typed payloads into
MoleculeState and persist them as Session artifacts / Meta-DNA rail events.
When an Orchestrator + Session are supplied, generate_plan remains the
planning surface for stages that need a live Plan object.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from t20.core.common.molecule_types import (
    CoherenceReport,
    ContextGraph,
    DecisionToken,
    DriftLevel,
    LivingObjective,
    MoleculeDraft,
    MoleculeHalt,
    MoleculeInsight,
    MoleculePTAS,
    MoleculeSpec,
    MoleculeState,
    MoleculeTAS,
    PolicyConstraints,
    RunFlags,
    RunMode,
    UserRequest,
)
from t20.core.common.types import Plan, Role, Task

logger = logging.getLogger(__name__)

COHERENCE_FLOOR = 0.72
COHERENCE_CONVERGE = 0.90
GUARD_STAGES = {"Stage10EthicalCompliance", "Stage16JointDecisions", "Stage17IntegrityMonitoring"}

STAGE_ORDER = [
    "Stage1KickForgeExtract",
    "Stage2KickForgePurify",
    "Stage3KickFlowStructure",
    "Stage4KickFlowDelegate",
    "Stage5KnowledgeTransfer",
    "Stage6CodeContext",
    "Stage7PromptRefinement",
    "Stage8ProtocolEstablishment",
    "Stage9SystemMonitoring",
    "Stage10EthicalCompliance",
    "Stage11VisualAssets",
    "Stage12OperationalRules",
    "Stage13StrategicPlans",
    "Stage14NLTranslation",
    "Stage15DynamicRoleAdaptation",
    "Stage16JointDecisions",
    "Stage17IntegrityMonitoring",
    "Stage18TailoredPlans",
    "Stage19HolisticTaskApproach",
    "Stage20ReviewRefinement",
]


class MoleculeFault(RuntimeError):
    """Unrecoverable molecule fault — maps to halt."""


@dataclass
class MoleculeBind:
    """Inputs that ignite MetaPlaybookRuntime."""

    user_request: UserRequest
    context_graph: ContextGraph
    run_flags: RunFlags = field(default_factory=RunFlags)
    living_objective: Optional[LivingObjective] = None
    policy: PolicyConstraints = field(default_factory=PolicyConstraints)
    consent_recycle: bool = False


class MoleculeRuntime:
    """Self-running 20-stage lattice bound to Session / ExecutionContext / Orchestrator."""

    def __init__(
        self,
        session: Any = None,
        orchestrator: Any = None,
        consent_gate: Optional[Callable[[str, MoleculeState], bool]] = None,
    ) -> None:
        self.session = session
        self.orchestrator = orchestrator
        self.consent_gate = consent_gate
        self.state = MoleculeState()
        self.trace: List[Dict[str, Any]] = []
        self._halted = False

    def ignite(self, bind: MoleculeBind) -> MoleculeState:
        """Bind living objective / user request and run the molecule kernel."""
        living = bind.living_objective or LivingObjective(text=bind.user_request.text)
        self.state.obj = living.text
        self.state.mode = bind.run_flags.mode
        self._log("ignite", {"obj": self.state.obj, "mode": bind.run_flags.mode.value})

        if not bind.run_flags.self_run:
            self._orbit(bind, full=True)
            if self.state.draft is None:
                self.state.draft = MoleculeDraft(cycle=self.state.cycle, body=self.state.obj)
            self._halt("single-pass complete — self_run disabled", "kernel")
            return self.state

        if bind.run_flags.self_run and not bind.consent_recycle:
            if self.consent_gate is not None and not self.consent_gate("first-recycle", self.state):
                self._halt("consent_gate denied first recycle", "kernel")
                return self.state
            if self.consent_gate is None and not bind.consent_recycle:
                bind.consent_recycle = True

        max_cycles = bind.run_flags.max_cycles or 3
        while (
            self.state.cycle < max_cycles
            and not self._halted
            and not self._converged()
        ):
            full = not (
                self.state.spec_stable and bind.run_flags.microcycle_on_stable_spec and self.state.cycle > 0
            )
            self._orbit(bind, full=full)
            self.state.cycle += 1
            self._score(self.state.cycle)

            if self.state.coherence.drift == DriftLevel.HIGH:
                self._halt("drift — human-in-the-loop required", "kernel")
                break
            if living.drift == DriftLevel.HIGH:
                self._halt("living_objective.drift high — re-anchor required", "kernel")
                break
            if self.state.conflict and not self.state.consensus:
                self._halt("unresolved conflict", "Stage16JointDecisions")
                break

            if self.state.insight:
                self.state.obj = self.state.insight.summary
                self._log("recycle", {"obj": self.state.obj, "cycle": self.state.cycle})

        return self.state

    def as_plan(self) -> Plan:
        """Project molecule state onto the existing Plan type (runtime_gen.kl)."""
        roles = [
            Role(title="KickForge", purpose="Extract, purify, validate TAS"),
            Role(title="KickFlow", purpose="Structure, delegate, refine pipeline"),
            Role(title="KickGuard", purpose="Ethics, integrity, joint decisions"),
            Role(title="Orchestrator", purpose="Adapt roles and synthesize insight"),
        ]
        tasks: List[Task] = []
        for idx, tas in enumerate(self.state.tas, start=1):
            tasks.append(
                Task(
                    id=tas.tas_id or f"T-{idx:02d}",
                    description=tas.text,
                    role="KickForge",
                    agent="KickForge",
                    deps=[],
                )
            )
        if not tasks:
            tasks.append(
                Task(
                    id="T-00",
                    description=self.state.obj or "molecule objective",
                    role="Orchestrator",
                    agent="Orchestrator",
                    deps=[],
                )
            )
        return Plan(
            high_level_goal=self.state.obj,
            reasoning=self.state.insight.summary if self.state.insight else "molecule projection",
            roles=roles,
            tasks=tasks,
        )

    def _orbit(self, bind: MoleculeBind, full: bool) -> None:
        stages = STAGE_ORDER if full else [
            "Stage15DynamicRoleAdaptation",
            "Stage16JointDecisions",
            "Stage17IntegrityMonitoring",
            "Stage19HolisticTaskApproach",
            "Stage20ReviewRefinement",
        ]
        for name in stages:
            if self._halted:
                return
            fn = self._STAGE_FNS.get(name)
            if fn is None:
                logger.warning("No handler for %s", name)
                continue
            fn(self, bind)
            self._persist(name)

    def _converged(self) -> bool:
        c = self.state.coherence
        return (
            c.coherence >= COHERENCE_CONVERGE
            and c.drift == DriftLevel.LOW
            and not self.state.conflict
            and self.state.draft is not None
        )

    def _halt(self, reason: str, stage: str) -> None:
        self._halted = True
        self.state.halt = MoleculeHalt(
            reason=reason, stage=stage, cycle=self.state.cycle, token=DecisionToken.HALT
        )
        self._log("halt", {"reason": reason, "stage": stage})
        if self.session is not None:
            try:
                self.session.add_artifact("molecule_halt.json", self.state.halt.model_dump_json(indent=2))
                self.session.log_rail_event(
                    rail=self.state.cycle,
                    event="molecule.halt",
                    data={"reason": reason, "stage": stage},
                )
            except Exception as exc:  # pragma: no cover
                logger.debug("session halt persist skipped: %s", exc)

    def _score(self, cycle: int) -> None:
        base = 0.70 + min(0.25, 0.06 * max(1, len(self.state.ptas)))
        if self.state.spec_stable:
            base += 0.06
        if self.state.conflict:
            base -= 0.20
        coherence = max(0.0, min(0.99, base))
        drift = DriftLevel.LOW if coherence >= 0.85 else DriftLevel.MED
        valence = 0.75 + (0.05 if self.state.draft else 0.0)
        self.state.coherence = CoherenceReport(
            coherence=round(coherence, 3),
            drift=drift,
            valence=round(valence, 3),
            cycle=cycle,
            integrity=self.state.monitor_integrity,
            notes="hybrid-score from molecule lattice",
        )
        if coherence < COHERENCE_FLOOR:
            self._halt("coherence floor breached", "Stage17IntegrityMonitoring")

    def _log(self, event: str, data: Dict[str, Any]) -> None:
        self.trace.append({"event": event, "cycle": self.state.cycle, **data})
        logger.info("molecule.%s %s", event, data)
        if self.session is not None:
            try:
                self.session.log_rail_event(
                    rail=self.state.cycle,
                    event=f"molecule.{event}",
                    data=data,
                    hybrid_score=self.state.coherence.coherence or None,
                )
            except Exception as exc:  # pragma: no cover
                logger.debug("meta-dna skip: %s", exc)

    def _persist(self, stage: str) -> None:
        if self.session is None:
            return
        try:
            self.session.add_artifact(
                f"molecule/{self.state.cycle:02d}_{stage}.json",
                self.state.model_dump_json(indent=2),
            )
        except Exception as exc:  # pragma: no cover
            logger.debug("artifact persist skip: %s", exc)

    def _extract(self, bind: MoleculeBind) -> None:
        text = bind.user_request.text.strip()
        living = (bind.living_objective.text if bind.living_objective else text).strip()
        atoms = [p.strip() for p in text.replace(";", ".").split(".") if p.strip()]
        if living and living not in atoms:
            atoms.insert(0, living)
        if not atoms:
            atoms = [self.state.obj or "unspecified objective"]
        self.state.tas = [
            MoleculeTAS(tas_id=f"TAS-{i:02d}", text=atom, source="extract", traits=["atomic-intake"])
            for i, atom in enumerate(atoms, start=1)
        ]
        self._log("extract", {"tas": len(self.state.tas)})

    def _purify(self, bind: MoleculeBind) -> None:
        hard = {s.lower() for s in bind.policy.hard_stops}
        kept: List[MoleculePTAS] = []
        for tas in self.state.tas:
            if any(stop and stop in tas.text.lower() for stop in hard):
                self._halt("policy hard-stop on raw TAS", "Stage2KickForgePurify")
                return
            kept.append(
                MoleculePTAS(ptas_id=tas.tas_id.replace("TAS", "PTAS"), text=tas.text, source_tas=tas.tas_id)
            )
        self.state.ptas = kept

    def _structure(self, bind: MoleculeBind) -> None:
        self.state.spec = MoleculeSpec(
            horizon="multi-cycle" if bind.run_flags.self_run else "single-pass",
            style=bind.run_flags.mode.value.lower(),
            stages=list(STAGE_ORDER),
            stable=False,
            notes=f"structured from {len(self.state.ptas)} PTAS",
        )

    def _delegate(self, bind: MoleculeBind) -> None:
        self.state.state = {
            "delegated": ["KickForge", "KickFlow", "KickGuard", "Orchestrator"],
            "flags": bind.run_flags.model_dump(),
            "domain": bind.context_graph.domain,
        }

    def _knowledge(self, bind: MoleculeBind) -> None:
        self.state.logic.append(f"spec.horizon={self.state.spec.horizon}")

    def _code_context(self, bind: MoleculeBind) -> None:
        self.state.logic.append("execution_context=Session+ExecutionContext+MoleculeState")

    def _refine_prompt(self, bind: MoleculeBind) -> None:
        self.state.spec.notes = (self.state.spec.notes + " | lyra-refined").strip(" |")

    def _protocol(self, bind: MoleculeBind) -> None:
        self.state.mode = bind.run_flags.mode

    def _monitor(self, bind: MoleculeBind) -> None:
        self.state.monitor_integrity = "OK"

    def _ethics(self, bind: MoleculeBind) -> None:
        self.state.decision = DecisionToken.ALLOW
        if bind.policy.profile.lower() in {"deny", "block"}:
            self.state.decision = DecisionToken.DENY
            self._halt("ethical non-consent", "Stage10EthicalCompliance")

    def _visual(self, bind: MoleculeBind) -> None:
        if not bind.run_flags.visual:
            return
        self.state.logic.append("visual-assets=requested")

    def _rules(self, bind: MoleculeBind) -> None:
        if not bind.run_flags.ruleset:
            return
        self.state.logic.append(f"ruleset={bind.run_flags.ruleset}")

    def _strategy(self, bind: MoleculeBind) -> None:
        self.state.spec.notes = (self.state.spec.notes + " | weplan").strip(" |")

    def _translate(self, bind: MoleculeBind) -> None:
        if not self.state.ptas:
            self.state.ptas.append(
                MoleculePTAS(ptas_id="PTAS-NL", text=bind.user_request.text, source_tas="NL")
            )

    def _adapt(self, bind: MoleculeBind) -> None:
        self.state.spec_stable = len(self.state.ptas) >= 1
        self.state.spec.stable = self.state.spec_stable

    def _joint(self, bind: MoleculeBind) -> None:
        if self.state.decision == DecisionToken.HALT or self.state.monitor_integrity == "FAIL":
            self._halt("joint-decision gate", "Stage16JointDecisions")
            return
        self.state.consensus = "ALLOW"
        self.state.conflict = []

    def _integrity(self, bind: MoleculeBind) -> None:
        if self.state.monitor_integrity == "FAIL":
            self._halt("integrity FAIL", "Stage17IntegrityMonitoring")

    def _tailor(self, bind: MoleculeBind) -> None:
        self.state.spec.horizon = "tailored"

    def _synthesize(self, bind: MoleculeBind) -> None:
        summary = self.state.obj
        if self.state.ptas:
            summary = " | ".join(p.text for p in self.state.ptas[:3])
        self.state.insight = MoleculeInsight(
            cycle=self.state.cycle,
            summary=summary,
            tas_count=len(self.state.tas),
            ptas_count=len(self.state.ptas),
            spec_stable=self.state.spec_stable,
        )

    def _review(self, bind: MoleculeBind) -> None:
        body = self.state.insight.summary if self.state.insight else self.state.obj
        self.state.draft = MoleculeDraft(
            cycle=self.state.cycle,
            body=body,
            consensus=self.state.consensus == "ALLOW",
        )


MoleculeRuntime._STAGE_FNS = {
    "Stage1KickForgeExtract": MoleculeRuntime._extract,
    "Stage2KickForgePurify": MoleculeRuntime._purify,
    "Stage3KickFlowStructure": MoleculeRuntime._structure,
    "Stage4KickFlowDelegate": MoleculeRuntime._delegate,
    "Stage5KnowledgeTransfer": MoleculeRuntime._knowledge,
    "Stage6CodeContext": MoleculeRuntime._code_context,
    "Stage7PromptRefinement": MoleculeRuntime._refine_prompt,
    "Stage8ProtocolEstablishment": MoleculeRuntime._protocol,
    "Stage9SystemMonitoring": MoleculeRuntime._monitor,
    "Stage10EthicalCompliance": MoleculeRuntime._ethics,
    "Stage11VisualAssets": MoleculeRuntime._visual,
    "Stage12OperationalRules": MoleculeRuntime._rules,
    "Stage13StrategicPlans": MoleculeRuntime._strategy,
    "Stage14NLTranslation": MoleculeRuntime._translate,
    "Stage15DynamicRoleAdaptation": MoleculeRuntime._adapt,
    "Stage16JointDecisions": MoleculeRuntime._joint,
    "Stage17IntegrityMonitoring": MoleculeRuntime._integrity,
    "Stage18TailoredPlans": MoleculeRuntime._tailor,
    "Stage19HolisticTaskApproach": MoleculeRuntime._synthesize,
    "Stage20ReviewRefinement": MoleculeRuntime._review,
}


def default_bind(objective: str, domain: str = "t20.runtime") -> MoleculeBind:
    """Minimal ignition helper used by tests and CLI scaffolds."""
    return MoleculeBind(
        user_request=UserRequest(text=objective, locale="en"),
        context_graph=ContextGraph(
            domain=domain,
            refs=["runtime_gen.kl", "klmx-meta-playbook-molecule.kicklang"],
        ),
        run_flags=RunFlags(
            mode=RunMode.HYBRID,
            ruleset="ocs-v2.1",
            visual=False,
            self_run=True,
            max_cycles=3,
            microcycle_on_stable_spec=True,
        ),
        living_objective=LivingObjective(text=objective, drift=DriftLevel.LOW),
        consent_recycle=True,
    )
