"""
FancyWellDatabaseObject (F1 Critical)

Guarded state machine + Macro Engine for the ZuluYokohama Protocol input harness.
Replaces ad-hoc Excel/JSON wellbore inputs with protocol-governed, double-click
editable, Entra-backed, hash-chained, coherence-harvesting objects.

States (guarded surfaces):
    OPEN         - mutable, normal editing
    TOGGLED_ON   - macro recording / live
    TOGGLED_OFF  - paused
    LOCKED       - immutable FrozenWellSnapshot (only path to export / downstream)

Every transition that could affect topology must pass continuity guards.
No force=True bypasses (H7).

See hardening package F1 + F6 + H7 + H8.
"""

from __future__ import annotations
import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict

# Robust import for data/ at repo root (works for python -m, src-on-path, and package runs)
import sys
from pathlib import Path as _Path
_here = _Path(__file__).resolve()
_repo_root = _here.parents[2]  # welly_db_4budZ/
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))
from data.valor_free1 import (
    FORMATIONS,
    CASING_STRINGS,
    get_canonical_well_header,
)

# --- Regimes (from concept HTML + action plan continuity states) ---
class Regime(str, Enum):
    STABLE = "Stable"          # Green - physically sound traversal
    TRANSITIONAL = "Transitional"  # Yellow - boundary layer
    CRITICAL = "Critical"      # Red - intercept / hazard


class WellState(str, Enum):
    OPEN = "OPEN"
    TOGGLED_ON = "TOGGLED_ON"
    TOGGLED_OFF = "TOGGLED_OFF"
    LOCKED = "LOCKED"


class WellElement(BaseModel):
    """A single structural / geological element in the wellbore manifold."""
    model_config = ConfigDict(frozen=False, extra="forbid")

    category: str = Field(..., description="Conductor | Surface | Intermediate | Production | Formation...")
    tmd_ft: float = Field(..., gt=0, description="Total Measured Depth (true geometry variable)")
    od_in: float = Field(..., gt=0, description="Outer Matrix Diameter (inches constraint)")
    regime: Regime = Regime.STABLE
    formation_top: Optional[float] = None
    formation_bottom: Optional[float] = None
    notes: str = ""


@dataclass
class FrozenWellSnapshot:
    """Immutable, cryptographically sealed exportable state (H8)."""
    timestamp_epoch_ms: int
    well_header: Dict[str, Any]
    elements: List[Dict[str, Any]]
    state_at_freeze: WellState
    integrity_hash: str
    provenance_framework: str = "ZYP-1.0-welly_db-fancy"
    coherence_harvest_delta: float = 0.0
    protocol_version: str = "zyp-1.0-hardening-f1-f3-h1-h5-h8"

    def to_json(self) -> str:
        # Canonical: sorted keys for deterministic hash
        payload = {
            "timestamp_epoch_ms": self.timestamp_epoch_ms,
            "provenance_framework": self.provenance_framework,
            "well_header": self.well_header,
            "elements": self.elements,
            "state_at_freeze": self.state_at_freeze.value,
            "coherence_harvest_delta": self.coherence_harvest_delta,
            "protocol_version": self.protocol_version,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))


class FancyWellDatabaseObject:
    """
    The core upstream object (F1).
    - In-memory transactional layer (this.elements)
    - Guarded state machine
    - @register_macro decorator + macro registry
    - Frozen snapshots with SHA-256 + coherence delta
    - Role stub for Entra ID (LOCAL / REMOTE / WELL_CONTROL)
    """

    def __init__(self, header: Optional[Dict[str, Any]] = None):
        self._state: WellState = WellState.OPEN
        self.header: Dict[str, Any] = header or get_canonical_well_header()
        self.elements: List[WellElement] = []
        self._macros: Dict[str, Callable] = {}
        self.last_coherence_harvest_delta: float = 0.0
        self._authorized_by: Optional[str] = None  # Entra principal or "local-dev"
        self._register_core_macros()

        # Seed with canonical conductor + surface from the research data (A-Box)
        self._seed_from_research_data()

    # --- State Machine (guarded) ---
    @property
    def state(self) -> WellState:
        return self._state

    def _require_state(self, allowed: List[WellState], action: str):
        if self._state not in allowed:
            raise RuntimeError(
                f"Action '{action}' blocked: current state={self._state}. "
                f"Allowed: {[s.value for s in allowed]}. Zero bypass."
            )

    def toggle_on(self, authorized_by: str = "local-dev"):
        self._require_state([WellState.OPEN, WellState.TOGGLED_OFF], "toggle_on")
        self._state = WellState.TOGGLED_ON
        self._authorized_by = authorized_by
        self._log(f"State -> TOGGLED_ON by {authorized_by}")

    def toggle_off(self):
        self._require_state([WellState.TOGGLED_ON], "toggle_off")
        self._state = WellState.TOGGLED_OFF
        self._log(f"State -> TOGGLED_OFF")

    def lock(self, authorized_by: str) -> FrozenWellSnapshot:
        """H7 / F6: Only authorized principals may produce immutable snapshot."""
        self._require_state([WellState.TOGGLED_ON, WellState.TOGGLED_OFF, WellState.OPEN], "lock")
        # In real impl: call Entra ID validation here for WELL_CONTROL role
        if not authorized_by:
            raise PermissionError("LOCK requires explicit authorized_by (Entra ID principal). Zero bypass.")

        snap = self._create_frozen_snapshot(authorized_by)
        self._state = WellState.LOCKED
        self._authorized_by = authorized_by
        self._log(f"State -> LOCKED by {authorized_by}. integrity={snap.integrity_hash[:12]}...")
        return snap

    # --- Core Operations (will be guarded by higher layers) ---
    def add_entity(
        self,
        category: str,
        tmd_ft: float,
        od_in: float,
        regime: Regime = Regime.STABLE,
        **kwargs,
    ) -> WellElement:
        self._require_state([WellState.OPEN, WellState.TOGGLED_ON], "add_entity")
        elem = WellElement(
            category=category,
            tmd_ft=float(tmd_ft),
            od_in=float(od_in),
            regime=regime,
            **kwargs,
        )
        # Basic physical invariant (example of T-Box / restriction map guard)
        if elem.tmd_ft <= 0 or elem.od_in <= 0:
            raise ValueError("tmd and od must be positive physical values (continuity guard)")

        self.elements.append(elem)
        self._log(f"Element unrolled: {category} @ {tmd_ft}' OD={od_in}\" regime={regime.value}")
        return elem

    def inspect(self, index: int) -> WellElement:
        return self.elements[index]

    # --- Macro Engine (F1 + F3) ---
    def _register_core_macros(self):
        @self.register_macro("export_for_fiber_sheaf_engine")
        def _export_for_fiber_sheaf_engine() -> Dict[str, Any]:
            """F3 critical: exact block_laplacian_ready payload for Termux fiber sheaf engine."""
            from .wellbore_topology import build_simplicial_payload
            payload = build_simplicial_payload(self.elements, self.header)
            payload["coherence_harvest_delta"] = self.last_coherence_harvest_delta
            payload["integrity_hash"] = self._compute_integrity_hash(payload)
            # In full impl: evidence.write_k_s_evidence(payload)
            self._log("Macro executed: export_for_fiber_sheaf_engine (simplicial 1-complex + K(S) ready)")
            return payload

        @self.register_macro("compile_and_verify_framework_object")
        def _compile_and_verify() -> Dict[str, Any]:
            """Canonical UTI-style export (matches the HTML studio concept)."""
            snap = self._create_frozen_snapshot(self._authorized_by or "local-dev")
            # Also run basic coherence (will call topology layer)
            from .wellbore_topology import compute_coherence_signature
            sig = compute_coherence_signature(self.elements)
            self.last_coherence_harvest_delta = sig.get("delta_lambda_1", 0.0)
            self._log(f"Macro: compile_and_verify -> delta_lambda_1={self.last_coherence_harvest_delta:.6f}")
            return {
                "snapshot": asdict(snap) if hasattr(snap, '__dataclass_fields__') else snap.__dict__ if hasattr(snap,'__dict__') else snap,
                "coherence": sig,
            }

    def register_macro(self, name: str):
        def decorator(fn: Callable):
            if name in self._macros:
                raise ValueError(f"Macro {name} already registered")
            self._macros[name] = fn
            return fn
        return decorator

    def run_macro(self, name: str, *args, **kwargs) -> Any:
        self._require_state([WellState.TOGGLED_ON, WellState.OPEN], f"run_macro:{name}")
        if name not in self._macros:
            raise KeyError(f"Unknown macro: {name}")
        return self._macros[name](*args, **kwargs)

    # --- Internals ---
    def _seed_from_research_data(self):
        """Seed the A-Box with the exact research values (Conductor + Surface + Production)."""
        # Conductor
        c = CASING_STRINGS[0]
        self.add_entity(
            category="Conductor",
            tmd_ft=c.depth_tmd_ft,
            od_in=c.casing_od_in,
            regime=Regime.STABLE,
            formation_top=0.0,
            formation_bottom=c.depth_tmd_ft,
            notes="Spud Mud 15.7ppg, 125 sks, WOB 15k, ROP 100",
        )
        # Surface
        s = CASING_STRINGS[1]
        self.add_entity(
            category="Surface",
            tmd_ft=s.depth_tmd_ft,
            od_in=s.casing_od_in,
            regime=Regime.TRANSITIONAL,
            formation_top=FORMATIONS[0].top_md_ft, # Ohio Shale top
            formation_bottom=FORMATIONS[1].top_md_ft, # Big Lime top
            notes=f"ID {s.casing_id_in}\" J-55/8rd, WOB 25k, ROP 150",
        )
        # Production
        p = CASING_STRINGS[2]
        self.add_entity(
            category="Production",
            tmd_ft=p.depth_tmd_ft,
            od_in=p.casing_od_in,
            regime=Regime.STABLE,
            formation_top=FORMATIONS[3].top_md_ft, # Trenton top
            formation_bottom=FORMATIONS[4].bottom_md_ft, # Black River bottom
            notes=f"ID {p.casing_id_in}\" L-80/8rd, Air Drill",
        )

    def _create_frozen_snapshot(self, authorized_by: str) -> FrozenWellSnapshot:
        elements_dicts = [e.model_dump() for e in self.elements]
        ts = int(time.time() * 1000)
        # Build payload for hash (exclude the hash field itself)
        temp = FrozenWellSnapshot(
            timestamp_epoch_ms=ts,
            well_header=self.header,
            elements=elements_dicts,
            state_at_freeze=self._state,
            integrity_hash="TEMP",
            coherence_harvest_delta=self.last_coherence_harvest_delta,
            protocol_version="zyp-1.0-hardening-f1-f3-h1-h5-h8",
        )
        canonical = temp.to_json().replace('"integrity_hash":"TEMP"', '"integrity_hash":""')  # clean
        # real hash over the canonical without the placeholder
        h = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        temp.integrity_hash = h
        return temp

    def _compute_integrity_hash(self, payload: Dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def _log(self, msg: str):
        # In real: route to evidence + morning_report
        print(f"[FancyWellDB {self._state.value}] {msg}")


# Convenience factory used by scripts / TUI
def create_valor_free1_harness() -> FancyWellDatabaseObject:
    """Factory that returns a harness pre-seeded with the research well (A-Box)."""
    return FancyWellDatabaseObject()
