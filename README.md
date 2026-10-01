# Case Management System Backend (KPMG FDE Week 1 Technical Task)

A modular, testable, and production-quality Python backend for a Case Management System built using **FastAPI**, **SQLAlchemy 2.x**, **Pydantic v2**, and **SQLite / PostgreSQL**.

---

## 1. Project Overview
The Case Management System backend provides RESTful APIs for managing operational and customer cases. It allows creating, listing, retrieving, updating, and deleting case records with strict schema validation, robust exception handling, structured JSON logging, and comprehensive automated test coverage.

## 2. Architecture
The project follows a clean 3-tier modular architecture separating concerns across distinct layers:
- **API / Presentation Layer** (`app/api`): REST endpoints, HTTP status handling, and OpenAPI specifications.
- **Service / Business Logic Layer** (`app/services`): Enforces transaction boundaries, logging, error handling, and business operations.
- **Data Access & Persistence Layer** (`app/models`, `app/database`): SQLAlchemy ORM models, database engines, and session lifecycle management.
- **Data Transfer Objects (DTOs)** (`app/schemas`): Pydantic schemas separating API input/output contracts from database models.

```
+-------------------------------------------------------------+
|                      FastAPI Routes                         |
|           (GET/POST/PUT/DELETE /cases, GET /health)         |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     Pydantic Schemas                        |
|            (CaseCreate, CaseUpdate, CaseResponse)           |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     Case Service Layer                      |
|         (Transaction Management, Business Rules)            |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                   SQLAlchemy ORM Model                      |
|                       (Case Model)                          |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                 Relational Database Engine                  |
|               (SQLite Default / PostgreSQL)                 |
+-------------------------------------------------------------+
```

## 3. Technology Stack
- **Python**: 3.11+
- **Web Framework**: FastAPI
- **ASGI Server**: Uvicorn
- **ORM**: SQLAlchemy 2.x
- **Data Validation & Settings**: Pydantic v2 & Pydantic Settings
- **Database**: SQLite (Default for local development) & PostgreSQL compatible via `psycopg3`
- **Testing**: pytest, pytest-cov, HTTPX
- **Configuration & Environment**: python-dotenv / pydantic-settings
- **Logging**: Python `logging` module with structured JSON formatting

## 4. Project Structure
```
case-management-system/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application initialization & lifespan
│   ├── config.py            # Pydantic Settings configuration
│   ├── database.py          # SQLAlchemy engine & session dependency
│   ├── logging_config.py    # Structured JSON log formatter
│   ├── exceptions.py        # Custom exceptions & global HTTP error handlers
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── case.py          # SQLAlchemy Case database model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── case.py          # Pydantic DTO validation schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── case_service.py  # Service layer for CRUD & transactions
│   │
│   └── api/
│       ├── __init__.py
│       └── routes/
│           ├── __init__.py
│           ├── health.py    # GET /health endpoint
│           └── cases.py     # REST endpoints for /cases
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Isolated test DB & TestClient fixtures
│   ├── test_health.py       # Health endpoint unit tests
│   └── test_cases.py        # Comprehensive API & Service layer tests
│
├── scripts/
│   ├── schema.sql           # SQL DDL for database schema
│   └── queries.sql          # Documented SQL queries (CRUD, CTE, Window, JOINs)
│
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore rules
├── requirements.txt         # Project dependencies
└── README.md                # Technical documentation
```

## 5. Prerequisites
- Python 3.11 or higher
- Git

## 6. Virtual Environment Setup
Clone the repository and create a Python virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

## 7. Dependency Installation
Install required packages using `pip`:
```bash
pip install -r requirements.txt
```

## 8. Environment Configuration
Copy `.env.example` to `.env`:
```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```
Default `.env` configuration:
```env
DATABASE_URL=sqlite:///./case_management.db
APP_NAME=Case Management System
ENVIRONMENT=development
LOG_LEVEL=INFO
```
To use PostgreSQL, update `DATABASE_URL`:
```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/case_management_db
```

## 9. Database Setup
SQLite database tables are automatically initialized upon application startup (`app/main.py`).
For manual SQL setup or reference, execute `scripts/schema.sql` against your target database engine.

## 10. How to Run the Application
Start the Uvicorn development server:
```bash
# Direct run
uvicorn app.main:app --reload

# Or via Python module
python -m uvicorn app.main:app --reload
```
The application will start at `http://127.0.0.1:8000`.

## 11. How to Access API Documentation
FastAPI automatically generates interactive OpenAPI documentation:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
- **OpenAPI JSON**: `http://127.0.0.1:8000/openapi.json`

## 12. How to Run Tests
Execute unit and API integration tests using `pytest`:
```bash
pytest -v
```

## 13. How to Run Coverage
Generate test coverage metrics with `pytest-cov`:
```bash
# Command line report
pytest -v --cov=app --cov-report=term-missing

# HTML coverage report
pytest --cov=app --cov-report=html
```

## 14. API Endpoint Summary

| Method | Endpoint | Description | Status Codes |
|---|---|---|---|
| `GET` | `/health` | Service health status | `200 OK` |
| `POST` | `/cases` | Create a new case | `201 Created`, `422 Validation Error` |
| `GET` | `/cases` | Paginated list of cases (`skip`, `limit`) | `200 OK` |
| `GET` | `/cases/{case_id}` | Retrieve single case by ID | `200 OK`, `404 Not Found` |
| `PUT` | `/cases/{case_id}` | Full replacement update of a case | `200 OK`, `404 Not Found`, `422 Validation Error` |
| `DELETE` | `/cases/{case_id}` | Delete a case by ID | `204 No Content`, `404 Not Found` |

## 15. Example Requests and Responses

### 15.1 Create Case (`POST /cases`)
**Request**:
```http
POST /cases HTTP/1.1
Content-Type: application/json

{
  "title": "Database Connection Timeout",
  "description": "High latency observed on DB primary cluster.",
  "status": "OPEN"
}
```
**Response (`201 Created`)**:
```json
{
  "id": 1,
  "title": "Database Connection Timeout",
  "description": "High latency observed on DB primary cluster.",
  "status": "OPEN",
  "created_at": "2026-09-16T15:20:00+00:00",
  "updated_at": "2026-09-16T15:20:00+00:00"
}
```

### 15.2 List Cases (`GET /cases?skip=0&limit=10`)
**Response (`200 OK`)**:
```json
[
  {
    "id": 1,
    "title": "Database Connection Timeout",
    "description": "High latency observed on DB primary cluster.",
    "status": "OPEN",
    "created_at": "2026-09-16T15:20:00+00:00",
    "updated_at": "2026-09-16T15:20:00+00:00"
  }
]
```

### 15.3 Get Single Case (`GET /cases/1`)
**Response (`200 OK`)**:
```json
{
  "id": 1,
  "title": "Database Connection Timeout",
  "description": "High latency observed on DB primary cluster.",
  "status": "OPEN",
  "created_at": "2026-09-16T15:20:00+00:00",
  "updated_at": "2026-09-16T15:20:00+00:00"
}
```

### 15.4 Full Update Case (`PUT /cases/1`)
**Request**:
```http
PUT /cases/1 HTTP/1.1
Content-Type: application/json

{
  "title": "Database Connection Timeout - Resolved",
  "description": "Connection pool size increased to handle load spikes.",
  "status": "RESOLVED"
}
```
**Response (`200 OK`)**:
```json
{
  "id": 1,
  "title": "Database Connection Timeout - Resolved",
  "description": "Connection pool size increased to handle load spikes.",
  "status": "RESOLVED",
  "created_at": "2026-09-16T15:20:00+00:00",
  "updated_at": "2026-09-16T15:22:00+00:00"
}
```

### 15.5 Delete Case (`DELETE /cases/1`)
**Response (`204 No Content`)**:
*(Empty Body)*

## 16. Error-Handling Approach
The application enforces a uniform JSON error structure across all API error responses:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description of error"
  }
}
```
Standardized error codes:
- `CASE_NOT_FOUND` (404): Case ID does not exist in database.
- `VALIDATION_ERROR` (422): Invalid query parameter or request body payload.
- `INTERNAL_SERVER_ERROR` (500): Uncaught database or application exception. Internal stack traces are logged securely and never exposed to API clients.

## 17. Logging Approach
Applications logs are generated using Python's standard `logging` library configured via custom `JSONFormatter` (`app/logging_config.py`).
Each log entry outputs structured JSON containing:
```json
{
  "timestamp": "2026-09-16T15:20:00.123456+00:00",
  "level": "INFO",
  "logger": "app.services.case_service",
  "message": "Successfully created case ID 1"
}
```
Appropriate log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`) are applied to track application startup, case creation/retrieval/update/deletion, validation errors, and database rollback events.

## 18. Database & Schema Information
The core application schema consists of the normalized `cases` table:
- `id` (INTEGER, PK, Auto-increment)
- `title` (VARCHAR(255), Non-nullable, Indexed)
- `description` (TEXT, Non-nullable)
- `status` (VARCHAR(50), Non-nullable, Indexed, Check constraint: `OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`)
- `created_at` (TIMESTAMP WITH TIME ZONE, Default CURRENT_TIMESTAMP)
- `updated_at` (TIMESTAMP WITH TIME ZONE, Default CURRENT_TIMESTAMP, OnUpdate CURRENT_TIMESTAMP)

Advanced relational concepts (Aggregations, CTEs, Window Functions, JOINs, Transactions) are fully demonstrated in `scripts/queries.sql`.

## 19. Git Workflow
Development followed standard Git feature branch practices:
- **Feature Branch**: `project-setup`
- **Commit Boundaries**:
  1. Set up project structure, configuration, and dependencies (`requirements.txt`, `.gitignore`, `.env.example`).
  2. Implement database configuration (`app/database.py`) and SQLAlchemy model (`app/models/case.py`).
  3. Implement Pydantic schemas (`app/schemas/case.py`) and service layer (`app/services/case_service.py`).
  4. Add REST API endpoints (`app/api/routes`) and error/logging handlers (`app/exceptions.py`, `app/logging_config.py`).
  5. Add automated unit and integration tests (`tests/`).
  6. Add SQL DDL schema and demonstration query scripts (`scripts/`).
  7. Add comprehensive engineering documentation (`README.md`).

## 20. Assumptions and Limitations
1. **Database Engine**: SQLite is configured as local default for ease of setup. PostgreSQL driver (`psycopg3`) is included in `requirements.txt` to enable switching via `DATABASE_URL` without code changes.
2. **PUT Semantics**: `PUT /cases/{case_id}` acts as full entity replacement requiring `title`, `description`, and `status`.
3. **Illustrative JOINs**: Additional relational tables in `scripts/queries.sql` are clearly documented as illustrative demonstration schemas.
4. **Authentication**: Week 1 requirement explicitly excludes authentication/authorization mechanisms to maintain clean scope.