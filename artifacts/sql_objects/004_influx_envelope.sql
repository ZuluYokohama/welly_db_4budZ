-- ══════════════════════════════════════════════════════════════
-- ZYP SQL Object: Influx Envelope (Kick Detection Telemetry)
-- Generated: 2026-06-04T10:13:22.043042+00:00
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
