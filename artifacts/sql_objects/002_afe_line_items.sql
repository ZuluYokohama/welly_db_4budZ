-- ══════════════════════════════════════════════════════════════
-- ZYP SQL Object: Authorization for Expenditure (AFE)
-- Generated: 2026-06-04T10:13:22.043042+00:00
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
