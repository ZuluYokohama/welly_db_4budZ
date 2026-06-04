# welly_db_4budZ

**FancyWellDatabaseObject • Input Standardization Harness for the ZuluYokohama Protocol**

> "Mathematics are the Operating System. Zero Bypass. Full Structure."

This repository is the upstream wellbore database / input harness realizing the **FancyWellDatabaseObject** (F1) and supporting features/hardenings (F2–F7, H1–H8) specified in the *ZuluYokohama Protocol Feature & Compute Logic Hardening Request Package* (June 2026, Ashram Development Track, PR #1 / SETUP-PHASE-0).

It draws directly from the full research corpus:

- OFFICE365-VEP-OILFIELDoPS-WELLBORE-&-STANDALONE-DATABASE-SOFTWARE-OBJECT-PLAN-CONCEPT-1.pdf (the standalone topological studio concept)
- Action Plan From Research Documents.pdf (Valor Energy Partners State Free #1 well data + Pi harness + 10-Gate Falsification + Prime Crystal Engine / ATFT)
- ZuluYokohama_Protocol_Feature_Compute_Hardening_Request_Package-1.pdf (the spec this implements)
- Review and Suggestion Layer Development.pdf (Jones Framework, TAPO-DL, Cartan-Topos, Persistent Fiber Homology, Holonomy-Regularized Loss, OG-EP Superintendent)
- LLM V&V Toolchain Optimization Strategies.pdf (AxiomZ, Forge Architecture, Agentic Triad, Wormhole-Path distillation, SurfaceEnclosure, KV Governor)
- ZuluYokohama Protocol refactoring- .pdf (the 5-step SCAN-SHAPE-HEAT-STRIKE-SHIP execution protocol + GeometryHarvester integration)

## Non-Negotiables (Protocol Invariants)
- **Zero Bypass**: No `force=True`. Every mutation/lock/export goes through guarded surfaces + A4-style continuity checks (spectral gap + trivial holonomy).
- **Evidence at Every Step**: K(S) evidence, shape pairs (only on Δλ₁ ≥ 0), integrity hashes (SHA-256 over canonical sorted JSON), coherence_harvest_delta on every locked snapshot.
- **Guarded State Machine**: OPEN → TOGGLED_ON → TOGGLED_OFF → LOCKED (immutable FrozenWellSnapshot).
- **Simplicial Native Handoff (F3)**: `export_for_fiber_sheaf_engine()` emits exact `block_laplacian_ready` payload consumable by Termux fiber-sheaf / block K(S) engine with zero translation.
- **Correct Fiber Sheaf Laplacian (H1/H5)**: Proper block construction (diagonal = sum restriction maps; off-diagonal = −weight × cross-term). Never Gram matrix.
- **Mathematics over Heuristics**: TAPO boxes, 10-Gate / omega_crystal_gate discipline, Dirichlet energy, persistent (co)homology signals.
- **Edge-Native / Termux Compatible**: Minimal deps (pydantic + numpy + scipy). 6GB UMA envelope mindset. No heavy frameworks on hot paths.

## Current Phase
Phase 1 — Input Harness Foundation (per hardening roadmap). Delivers the clean, coherence-gated WellGraph / FancyWellDatabaseObject that replaces ad-hoc Excel/CSV for downstream Prime Crystal Engine / og-ep-superintendent / Bipartite Router.

## Key Data
Valor Energy Partners — State Free #1 (API # 34-141-2-0059-00-00, Busckskin Twp, Ross County, Ohio, NAD27).

See `data/valor_free1.py` for the canonical formations + mechanical casing strings used as A-Box seed.

## Quick Start (after deps)
```powershell
cd welly_db_4budZ
pip install -r requirements.txt
python -m src.welly_db          # or python scripts/run_studio.py
```

See `docs/PROTOCOLS.md` and `docs/HARDENING_ALIGNMENT.md` for exact mapping to F1–F7 / H1–H8 and review-layer suggestions.

## Artifacts
- `artifacts/wellbore_studio.html` — the self-contained dark-mode Topological App Studio (vanilla, zero-dep) from the OBJECT-PLAN-CONCEPT (runnable by double-click).
- `artifacts/*.json` — canonical UTI exports + K(S) evidence examples.

## Execution Protocol (from refactoring note)
Always: SCAN (ingest point cloud) → SHAPE (build sheaf + restriction maps) → HEAT (spectral / zeta) → STRIKE (10-Gate / A4 falsification) → SHIP (distill + evidence + locked snapshot).

This is not "editing a spreadsheet". This is **Topological Synthesis on a live wellbore manifold**.

---

**Related (external)**: https://github.com/ZuluYokohama/zulu-yokohama-protocol (main protocol + fiber sheaf engine on Termux)

" The mathematics are the operating system. Zero bypass. Full structure. Recursive improvement. "
