-- =============================================================================
-- Case Management System - SQL Queries & Relational DB Examples
-- =============================================================================

-- 1. BASIC CRUD OPERATIONS
--------------------------------------------------------------------------------
-- Insert a new case
INSERT INTO cases (title, description, status, created_at, updated_at)
VALUES (
    'Database Connection Timeout',
    'Application failing to connect to PostgreSQL during peak load hours.',
    'OPEN',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Select all cases
SELECT id, title, description, status, created_at, updated_at
FROM cases
ORDER BY created_at DESC;

-- Update a case status
UPDATE cases
SET status = 'IN_PROGRESS', updated_at = CURRENT_TIMESTAMP
WHERE id = 1;

-- Delete a case
DELETE FROM cases
WHERE id = 1;


-- 2. FILTERING, SEARCHING & PAGINATION
--------------------------------------------------------------------------------
-- Filter by status and search title/description with pagination
SELECT id, title, status, created_at
FROM cases
WHERE status IN ('OPEN', 'IN_PROGRESS')
  AND (title LIKE '%Timeout%' OR description LIKE '%PostgreSQL%')
ORDER BY created_at DESC
LIMIT 10 OFFSET 0;


-- 3. AGGREGATION & GROUPING
--------------------------------------------------------------------------------
-- Count cases grouped by status
SELECT 
    status,
    COUNT(*) AS total_cases,
    MIN(created_at) AS oldest_case,
    MAX(created_at) AS newest_case
FROM cases
GROUP BY status
ORDER BY total_cases DESC;


-- 4. WINDOW FUNCTIONS
--------------------------------------------------------------------------------
-- Rank cases per status by creation timestamp using ROW_NUMBER() window function
SELECT 
    id,
    title,
    status,
    created_at,
    ROW_NUMBER() OVER (
        PARTITION BY status 
        ORDER BY created_at DESC
    ) AS status_rank
FROM cases;


-- 5. COMMON TABLE EXPRESSIONS (CTE)
--------------------------------------------------------------------------------
-- CTE calculating percentage distribution of cases across statuses
WITH StatusCounts AS (
    SELECT 
        status, 
        COUNT(*) AS status_count
    FROM cases
    GROUP BY status
),
TotalCount AS (
    SELECT COUNT(*) AS grand_total FROM cases
)
SELECT 
    sc.status,
    sc.status_count,
    tc.grand_total,
    ROUND(CAST(sc.status_count AS FLOAT) / tc.grand_total * 100, 2) AS percentage
FROM StatusCounts sc, TotalCount tc
WHERE tc.grand_total > 0;


-- 6. RELATIONAL JOIN (ILLUSTRATIVE DEMONSTRATION EXAMPLE)
--------------------------------------------------------------------------------
-- NOTE: The tables below ('case_comments' and 'users') are illustrative examples
-- created solely to demonstrate relational JOIN capabilities.
/*
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE case_comments (
    id INTEGER PRIMARY KEY,
    case_id INTEGER REFERENCES cases(id),
    user_id INTEGER REFERENCES users(id),
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
*/

-- Illustrative INNER JOIN query combining cases, comments, and users
/*
SELECT 
    c.id AS case_id,
    c.title AS case_title,
    c.status AS case_status,
    cm.comment_text,
    u.name AS commented_by,
    cm.created_at AS comment_time
FROM cases c
INNER JOIN case_comments cm ON c.id = cm.case_id
INNER JOIN users u ON cm.user_id = u.id
WHERE c.status = 'IN_PROGRESS'
ORDER BY cm.created_at DESC;
*/


-- 7. TRANSACTION HANDLING EXAMPLE
--------------------------------------------------------------------------------
-- Demonstrating explicit transaction control block
BEGIN TRANSACTION;

UPDATE cases 
SET status = 'RESOLVED', updated_at = CURRENT_TIMESTAMP 
WHERE id = 2;

-- Check constraint logic or rollback condition could occur here
-- If successful:
COMMIT;

-- If an error occurs:
-- ROLLBACK;
