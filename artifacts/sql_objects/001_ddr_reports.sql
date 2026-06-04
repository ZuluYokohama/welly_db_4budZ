-- ══════════════════════════════════════════════════════════════
-- ZYP SQL Object: Daily Drilling Report (DDR)
-- Generated: 2026-06-04T10:13:22.043042+00:00
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
