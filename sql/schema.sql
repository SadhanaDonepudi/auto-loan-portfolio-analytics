-- PostgreSQL-compatible DDL (also runs on SQLite, used locally because
-- PostgreSQL is unavailable in this environment).
CREATE TABLE IF NOT EXISTS loans (
    loan_id TEXT PRIMARY KEY,
    vintage INTEGER NOT NULL,
    term_months INTEGER NOT NULL CHECK (term_months IN (36, 48, 60, 72, 84)),
    vehicle_type TEXT NOT NULL CHECK (vehicle_type IN ('New', 'Used')),
    credit_score INTEGER NOT NULL,
    credit_band TEXT NOT NULL,
    orig_balance NUMERIC(12, 2) NOT NULL,
    interest_rate NUMERIC(5, 2) NOT NULL,
    is_30d_delinquent INTEGER NOT NULL CHECK (is_30d_delinquent IN (0, 1)),
    is_60d_delinquent INTEGER NOT NULL CHECK (is_60d_delinquent IN (0, 1)),
    prepaid INTEGER NOT NULL CHECK (prepaid IN (0, 1))
);
CREATE INDEX IF NOT EXISTS idx_loans_vintage ON loans (vintage);
CREATE INDEX IF NOT EXISTS idx_loans_term_credit ON loans (term_months, credit_score);
