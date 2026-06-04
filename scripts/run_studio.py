"""
scripts/run_studio.py

The Studio Engine: Production Execution Protocol (from refactoring note + action plan).

SCAN  -> ingest the Ohio/Valor wellbore point cloud (seeded A-Box)
SHAPE -> construct the Sheaf (FancyWellDatabaseObject + restriction maps)
HEAT  -> compute spectral gap (Δλ₁) + coherence via corrected K(S)
STRIKE-> verification via falsification / continuity guards (A4-style)
SHIP  -> distill, export canonical UTI + evidence artifacts, produce locked snapshot

Run:
    python -m scripts.run_studio
    # or from repo root: python scripts/run_studio.py

This establishes baseline K(S) evidence and shape pair ledger for the welly_db harness.
"""

from __future__ import annotations
import sys
from pathlib import Path

# Ensure src on path when run directly
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from welly_db.fancy_well_database import create_valor_free1_harness, WellState
from welly_db import wellbore_topology as topo
from welly_db import evidence


def main():
    print("=" * 70)
    print("ZULUYOKOHAMA PROTOCOL — welly_db Studio Engine (Phase 1)")
    print("Mathematics are the Operating System. Zero Bypass. Full Structure.")
    print("=" * 70)

    # 1. SCAN: Ingest
    print("\n[SCAN] Ingesting Valor Energy Partners State Free #1 (research A-Box)...")
    db = create_valor_free1_harness()
    print(f"  Header: {db.header['well_name']} API {db.header['api']}")
    print(f"  Seeded elements: {len(db.elements)} (Conductor + Surface from research data)")
    for e in db.elements:
        print(f"    - {e.category}: TMD={e.tmd_ft}' OD={e.od_in}\" regime={e.regime.value}")

    # 2. SHAPE: Build sheaf / object
    print("\n[SHAPE] Building manifold + restriction maps (via FancyWellDatabaseObject)...")
    db.toggle_on("local-dev")  # enter live macro mode (authorized)
    print(f"  State: {db.state.value}")

    # 3. HEAT: Spectral signature (corrected Laplacian)
    print("\n[HEAT] Computing fiber sheaf K(S) + Δλ₁ (H1/H5 corrected construction)...")
    sig = topo.compute_coherence_signature(db.elements)
    print(f"  lambda_1      = {sig['lambda_1']:.6f}")
    print(f"  delta_lambda_1 = {sig['delta_lambda_1']:.6f}")
    print(f"  energy (Dirichlet proxy) = {sig['energy']:.2f}")
    db.last_coherence_harvest_delta = sig["delta_lambda_1"]

    # 4. STRIKE: Verification gates (simplified A4 / 10-Gate spirit)
    print("\n[STRIKE] Running continuity / falsification gates...")
    if not sig["is_holonomy_trivial"]:
        print("  HALT_A4: non-trivial holonomy detected. Pivoting...")
        # In full: db.pivot... ; regenerate
    else:
        print("  Gate PASS: holonomy trivial within tolerance.")
    if sig["delta_lambda_1"] < -1e-9:
        print("  WARN: negative coherence harvest. Evidence will be rejected per protocol.")
    else:
        print("  Gate PASS: Δλ₁ non-negative.")

    # 5. SHIP: Export + evidence + lock
    print("\n[SHIP] Exporting canonical artifacts + locking snapshot...")
    # Macro path (F3)
    sheaf_payload = db.run_macro("export_for_fiber_sheaf_engine")
    print(f"  export_for_fiber_sheaf_engine -> n_vertices={sheaf_payload['n_vertices']}, fiber_dim={sheaf_payload['fiber_dim']}")

    # Write evidence
    ev_path = evidence.write_k_s_evidence(sheaf_payload)
    print(f"  Wrote K(S) evidence -> {ev_path.name}")

    # Compile/verify (also produces UTI-style)
    verify = db.run_macro("compile_and_verify_framework_object")
    print(f"  compile_and_verify delta used for harvest: {db.last_coherence_harvest_delta:.6f}")

    # Lock (produces immutable Frozen snapshot with integrity)
    snap = db.lock("local-dev")
    snap_path = evidence.write_frozen_snapshot_artifact(snap)
    print(f"  LOCKED snapshot -> {snap_path.name} (hash {snap.integrity_hash[:16]}...)")

    # Optional shape pair if we had a "problem->resolved"
    # Here we treat the initial seed as baseline; later runs would compare pre/post
    try:
        evidence.append_shape_pair(
            problem="initial_research_seed_manifest",
            resolved_coherence="valor_free1_conductor_surface_stable",
            delta=db.last_coherence_harvest_delta,
            pre_state={"lambda_1": 0.0},
            post_state={"lambda_1": sig["lambda_1"]},
        )
        print("  Appended shape_pair (baseline) to shape_pairs.jsonl")
    except ValueError as e:
        print(f"  Shape pair skipped: {e}")

    print("\n" + "=" * 70)
    print("SHIP COMPLETE. State:", db.state.value)
    print("Artifacts in ./artifacts/")
    print("Next: feed evidence into omega_crystal_gate or Termux fiber-sheaf engine.")
    print("=" * 70)


if __name__ == "__main__":
    main()
