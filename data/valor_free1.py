"""
Valor Energy Partners — State Free #1
API # 34-141-2-0059-00-00
Busckskin Township, Ross County, Ohio
NAD 27

Extracted from Action Plan From Research Documents.pdf (the canonical A-Box seed).
This is the "ground truth" physical manifold used for all topological synthesis,
sheaf construction, and coherence harvesting in this harness.

DO NOT mutate these values without a new locked snapshot + evidence trail.
"""

from __future__ import annotations
from typing import List, Dict
from pydantic import BaseModel, Field


class Formation(BaseModel):
    name: str
    top_md_ft: float
    bottom_md_ft: float


class CasingString(BaseModel):
    phase: str
    hole_diam_in: float
    casing_od_in: float
    casing_id_in: float | None = None
    weight_lb_per_ft: float
    grade_conn: str
    depth_tmd_ft: float
    depth_tvd_ft: float
    cement_sks: float | None = None
    cement_ppg: float | None = None
    cement_type: str | None = None
    wob_klbs: float | None = None


# === FORMATIONS (Table 1) ===
FORMATIONS: List[Formation] = [
    Formation(name="Ohio Shale", top_md_ft=130.0, bottom_md_ft=268.0),
    Formation(name="Big Lime", top_md_ft=268.0, bottom_md_ft=716.0),
    Formation(name="Packer Shell", top_md_ft=800.0, bottom_md_ft=828.0),
    Formation(name="Trenton Limestone", top_md_ft=1944.0, bottom_md_ft=2114.0),
    Formation(name="Black River Group", top_md_ft=2114.0, bottom_md_ft=2458.0),
]

# === MECHANICAL CASING / HOLE (Table 2, reconstructed from WBD sheet) ===
CASING_STRINGS: List[CasingString] = [
    CasingString(
        phase="Conductor",
        hole_diam_in=17.5,
        casing_od_in=13.375,
        casing_id_in=12.615, # J-55 54# has 12.615 CSG ID
        weight_lb_per_ft=54.0,
        grade_conn="J-55 / 8rd",
        depth_tmd_ft=114.0,
        depth_tvd_ft=114.0,
        cement_sks=125.0,
        cement_ppg=15.7,
        cement_type="Spud Mud",
        wob_klbs=15.0,
    ),
    CasingString(
        phase="Surface",
        hole_diam_in=12.25,
        casing_od_in=7.0,
        casing_id_in=6.366, # J-55 23# has 6.366 CSG ID
        weight_lb_per_ft=23.0,
        grade_conn="J-55 / 8rd",
        depth_tmd_ft=359.0,
        depth_tvd_ft=359.0,
        cement_sks=266.0,
        cement_ppg=15.7,
        cement_type="Spud Mud",
        wob_klbs=25.0,
    ),
    CasingString(
        phase="Production",
        hole_diam_in=6.0,
        casing_od_in=4.5,
        casing_id_in=3.875, # L-80 11.6# has 3.875 CSG ID
        weight_lb_per_ft=11.6,
        grade_conn="L-80 / 8rd",
        depth_tmd_ft=2000.0,
        depth_tvd_ft=2000.0,
        cement_sks=765.0,
        cement_ppg=14.8, # Tail is 14.8, Lead is 12
        cement_type="Air Drill",
        wob_klbs=None, # XX in sheet
    ),
]

# Quick lookup maps (for T-Box style invariants)
FORMATION_BY_NAME: Dict[str, Formation] = {f.name: f for f in FORMATIONS}
CASING_BY_PHASE: Dict[str, CasingString] = {c.phase: c for c in CASING_STRINGS}


def get_canonical_well_header() -> Dict:
    """Returns the immutable header facts (part of A-Box)."""
    return {
        "api": "34-141-2-0059-00-00",
        "well_name": "State Free #1",
        "operator": "Valor Energy Partners",
        "location": {
            "township": "Busckskin",
            "county": "Ross",
            "state": "Ohio",
            "crs": "NAD 27",
        },
        "gl_ft": 906.0,   # Ground Level
        "kb_ft": 8.0,     # Kelly Bushing (approx from source tables)
    }


def get_formations_as_dicts() -> List[Dict]:
    return [f.model_dump() for f in FORMATIONS]


def get_casing_as_dicts() -> List[Dict]:
    return [c.model_dump() for c in CASING_STRINGS]
