"""
Valor Ops Panel: SQL Object Persistence Layer
Renders every domain entity as a self-contained, parameterized .sql file.
NOV TotCo / Weatherford-style declarative schema.
"""
import json
import os
from pathlib import Path
from datetime import datetime, timezone


SQL_OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "artifacts" / "sql_objects"


def ensure_output_dir():
    SQL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def sanitize(val):
    """Escape single quotes for SQL string literals."""
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "1" if val else "0"
    if isinstance(val, (int, float)):
        return str(val)
    return "'" + str(val).replace("'", "''") + "'"


# ── Schema Definitions (CREATE TABLE) ────────────────────────────

DDR_SCHEMA = """-- ══════════════════════════════════════════════════════════════
-- ZYP SQL Object: Daily Drilling Report (DDR)
-- Generated: {timestamp}
-- Standard: NOV TotCo / WITSML 2.1 Declarative Vernacular
-- ══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS ddr_reports (
    report_id           VARCHAR(64)   PRIMARY KEY,
    report_date         DATE          NOT NULL,
    wellbore_id         VARCHAR(64)   NOT NULL,
    measured_depth_ft   DECIMAL(10,2),
    rop_ft_hr           DECIMAL(8,2),
    wob_klbs            DECIMAL(8,2),
    rpm                 DECIMAL(6,1),
    torque_ft_lbs       DECIMAL(10,2),
    mud_weight_ppg      DECIMAL(6,2),
    ecd_ppg             DECIMAL(6,2),
    surface_pressure_psi DECIMAL(8,2),
    hook_load_klbs      DECIMAL(8,2),
    lambda_1            DECIMAL(12,8),
    delta_lambda_1      DECIMAL(12,8),
    holonomy_signature  VARCHAR(32)   DEFAULT 'trivial',
    route_decision      VARCHAR(16)   DEFAULT 'LOCAL',
    created_at          TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);
"""

AFE_SCHEMA = """-- ══════════════════════════════════════════════════════════════
-- ZYP SQL Object: Authorization for Expenditure (AFE)
-- Generated: {timestamp}
-- Standard: OG-EP Superintendent Declarative Vernacular
-- ══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS afe_line_items (
    afe_id              VARCHAR(64)   PRIMARY KEY,
    well_name           VARCHAR(128)  NOT NULL,
    phase               VARCHAR(32)   NOT NULL,
    budget_usd          DECIMAL(14,2) NOT NULL,
    actual_usd          DECIMAL(14,2) DEFAULT 0.00,
    variance_fraction   DECIMAL(6,4)  DEFAULT 0.0000,
    coherence_score     DECIMAL(8,6),
    lambda_1            DECIMAL(12,8),
    status              VARCHAR(16)   DEFAULT 'ACTIVE',
    authorized_by       VARCHAR(128)  NOT NULL,
    created_at          TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);
"""

SHAPE_PAIR_SCHEMA = """-- ══════════════════════════════════════════════════════════════
-- ZYP SQL Object: Shape Pairs (QLoRA Distillation Fuel)
-- Generated: {timestamp}
-- Standard: Wormhole-Path 1 Evidence Ledger
-- ══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS shape_pairs (
    pair_id             INTEGER       PRIMARY KEY AUTOINCREMENT,
    timestamp           TIMESTAMP     NOT NULL,
    cycle               INTEGER,
    wormhole_path       VARCHAR(32)   DEFAULT 'WORMHOLE-PATH1',
    delta_lambda_1      DECIMAL(12,8) NOT NULL CHECK(delta_lambda_1 >= 0),
    route               VARCHAR(16)   DEFAULT 'LOCAL',
    anomaly_prev        BOOLEAN       DEFAULT 0,
    anomaly_curr        BOOLEAN       DEFAULT 0,
    state_before_json   TEXT,
    state_after_json    TEXT,
    created_at          TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);
"""

INFLUX_ENVELOPE_SCHEMA = """-- ══════════════════════════════════════════════════════════════
-- ZYP SQL Object: Influx Envelope (Kick Detection Telemetry)
-- Generated: {timestamp}
-- Standard: WITSML 2.1 / Streamlined Construct Slide 8
-- ══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS influx_envelope (
    envelope_id         INTEGER       PRIMARY KEY AUTOINCREMENT,
    wellbore_id         VARCHAR(64)   NOT NULL,
    timestamp           TIMESTAMP     NOT NULL,
    axial_tension_klbs  DECIMAL(8,2),
    hook_load_klbs      DECIMAL(8,2),
    surface_pressure_psi DECIMAL(8,2),
    influx_volume_bbl   DECIMAL(8,3),
    pressure_spike      BOOLEAN       DEFAULT 0,
    anomaly_detected    BOOLEAN       DEFAULT 0,
    barrier_status      VARCHAR(20)   DEFAULT 'Primary',
    created_at          TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);
"""


def generate_schemas():
    """Write all CREATE TABLE schemas to sql_objects/."""
    ensure_output_dir()
    ts = datetime.now(timezone.utc).isoformat()
    schemas = {
        "001_ddr_reports.sql": DDR_SCHEMA.format(timestamp=ts),
        "002_afe_line_items.sql": AFE_SCHEMA.format(timestamp=ts),
        "003_shape_pairs.sql": SHAPE_PAIR_SCHEMA.format(timestamp=ts),
        "004_influx_envelope.sql": INFLUX_ENVELOPE_SCHEMA.format(timestamp=ts),
    }
    for fname, content in schemas.items():
        path = SQL_OUTPUT_DIR / fname
        path.write_text(content, encoding="utf-8")
    return list(schemas.keys())


def shape_pairs_to_sql(jsonl_path: str) -> str:
    """Convert shape_pairs.jsonl into INSERT statements."""
    ensure_output_dir()
    lines = Path(jsonl_path).read_text(encoding="utf-8").strip().split("\n")
    inserts = []
    for line in lines:
        if not line.strip():
            continue
        p = json.loads(line)
        inserts.append(
            f"INSERT INTO shape_pairs (timestamp, cycle, wormhole_path, delta_lambda_1, route, "
            f"anomaly_prev, anomaly_curr, state_before_json, state_after_json) VALUES ("
            f"{sanitize(p.get('timestamp',''))}, "
            f"{sanitize(p.get('cycle'))}, "
            f"{sanitize(p.get('wormhole_path','WORMHOLE-PATH1'))}, "
            f"{sanitize(p.get('delta_lambda_1', 0))}, "
            f"{sanitize(p.get('route','LOCAL'))}, "
            f"{sanitize(p.get('anomaly_prev', False))}, "
            f"{sanitize(p.get('anomaly_curr', False))}, "
            f"{sanitize(json.dumps(p.get('state_before',{})))}, "
            f"{sanitize(json.dumps(p.get('state_after',{})))});"
        )
    
    ts = datetime.now(timezone.utc).isoformat()
    header = f"-- Shape Pairs INSERT batch ({len(inserts)} rows)\n-- Generated: {ts}\n\n"
    sql = header + "\n".join(inserts)
    out_path = SQL_OUTPUT_DIR / "005_shape_pairs_data.sql"
    out_path.write_text(sql, encoding="utf-8")
    return str(out_path)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    
    files = generate_schemas()
    print(f"Generated {len(files)} SQL schema files:")
    for f in files:
        print(f"  - artifacts/sql_objects/{f}")
    
    data_path = Path(__file__).parent.parent.parent / "artifacts" / "shape_pairs.jsonl"
    if data_path.exists():
        out = shape_pairs_to_sql(str(data_path))
        print(f"  - {out} (INSERT batch)")
    
    print("SQL Object Persistence: COMPLETE")
