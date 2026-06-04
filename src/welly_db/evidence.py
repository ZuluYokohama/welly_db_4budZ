"""
evidence.py

Writers for K(S) evidence, shape_pairs, and integrity artifacts (H2, H4, H8).

All artifacts must be canonical (sorted keys), carry protocol_version + integrity_hash.
omega_crystal_gate (CI) will later iterate these and enforce uniformity + positive delta.
"""

from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ARTIFACTS_DIR = Path(__file__).resolve().parents[2] / "artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def _canonical_json(obj: Dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _write_json(path: Path, payload: Dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = _canonical_json(payload)
    path.write_text(text, encoding="utf-8")
    return text


def write_k_s_evidence(payload: Dict[str, Any], run_id: str | None = None) -> Path:
    """Write the block_laplacian_ready + coherence evidence artifact."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    rid = run_id or ts
    fname = f"K_S_evidence_{rid}.json"
    p = ARTIFACTS_DIR / fname
    full = {
        **payload,
        "evidence_type": "K_S_evidence",
        "generated_at": ts,
        "run_id": rid,
    }
    _write_json(p, full)
    return p


def append_shape_pair(
    problem: str,
    resolved_coherence: str,
    delta: float,
    pre_state: Dict,
    post_state: Dict,
    path: Path | None = None,
) -> Path:
    """Append to shape_pairs.jsonl only when delta >= 0 (protocol rule)."""
    if delta < -1e-12:
        raise ValueError("Shape pair rejected: delta_lambda_1 must be >= 0 (zero bypass on degrading harvest)")
    p = path or (ARTIFACTS_DIR / "shape_pairs.jsonl")
    p.parent.mkdir(parents=True, exist_ok=True)
    rec = {
        "problem": problem,
        "resolved_coherence": resolved_coherence,
        "delta": delta,
        "pre": pre_state,
        "post": post_state,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    with p.open("a", encoding="utf-8") as f:
        f.write(_canonical_json(rec) + "\n")
    return p


def write_frozen_snapshot_artifact(snapshot: Any, run_id: str | None = None) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    rid = run_id or ts
    p = ARTIFACTS_DIR / f"frozen_snapshot_{rid}.json"
    if hasattr(snapshot, "to_json"):
        text = snapshot.to_json()
        p.write_text(text, encoding="utf-8")
    else:
        _write_json(p, snapshot if isinstance(snapshot, dict) else snapshot.__dict__)
    return p
