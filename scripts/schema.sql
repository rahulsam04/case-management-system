-- =============================================================================
-- Case Management System - Database Schema Definition (DDL)
-- Compatible with SQLite and PostgreSQL
-- =============================================================================

-- Drop table if exists for clean schema recreation
DROP TABLE IF EXISTS cases;

-- Main Cases Table
CREATE TABLE cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- For PostgreSQL, replace with: SERIAL PRIMARY KEY or BIGSERIAL
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_cases_status CHECK (status IN ('OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'))
);

-- Performance Indexes
CREATE INDEX idx_cases_title ON cases(title);
CREATE INDEX idx_cases_status ON cases(status);
CREATE INDEX idx_cases_created_at ON cases(created_at);
