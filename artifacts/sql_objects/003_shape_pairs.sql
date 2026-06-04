-- ══════════════════════════════════════════════════════════════
-- ZYP SQL Object: Shape Pairs (QLoRA Distillation Fuel)
-- Generated: 2026-06-04T10:13:22.043042+00:00
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
