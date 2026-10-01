import pytest
from unittest.mock import MagicMock
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.case import CaseCreate, CaseUpdate
from app.services.case_service import CaseService
from app.exceptions import CaseNotFoundException
from app.database import get_db
from app.models.case import Case
from app.main import app


def test_create_case_valid(client):
    """Test creating a case with valid data."""
    payload = {
        "title": "System Outage",
        "description": "Server rack 4 in datacenter B is offline.",
        "status": "OPEN"
    }
    response = client.post("/cases", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["status"] == payload["status"]
    assert "created_at" in data
    assert "updated_at" in data


def test_create_case_invalid_status(client):
    """Test creating a case with an invalid status enum value."""
    payload = {
        "title": "System Outage",
        "description": "Server rack offline.",
        "status": "INVALID_STATUS"
    }
    response = client.post("/cases", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_case_missing_required_data(client):
    """Test creating a case with missing required fields."""
    payload = {
        "title": "Missing description"
        # status and description omitted
    }
    response = client.post("/cases", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_get_all_cases_and_pagination(client):
    """Test retrieving cases with skip and limit query parameters."""
    # Seed 5 cases
    for i in range(1, 6):
        client.post("/cases", json={
            "title": f"Case {i}",
            "description": f"Description {i}",
            "status": "OPEN"
        })

    # Test limit=2
    response = client.get("/cases?skip=0&limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2

    # Test skip=3, limit=10
    response_skip = client.get("/cases?skip=3&limit=10")
    assert response_skip.status_code == status.HTTP_200_OK
    data_skip = response_skip.json()
    assert len(data_skip) == 2


def test_get_existing_case(client):
    """Test retrieving an existing single case by ID."""
    create_res = client.post("/cases", json={
        "title": "Hardware Failure",
        "description": "Disk drive crashed.",
        "status": "IN_PROGRESS"
    })
    case_id = create_res.json()["id"]

    response = client.get(f"/cases/{case_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == case_id
    assert data["title"] == "Hardware Failure"
    assert data["status"] == "IN_PROGRESS"


def test_get_nonexistent_case_returns_404(client):
    """Test retrieving a non-existent case returns HTTP 404 with standard error body."""
    response = client.get("/cases/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "CASE_NOT_FOUND"
    assert "99999" in data["error"]["message"]


def test_update_existing_case_full(client):
    """Test performing a full replacement update (PUT) on an existing case."""
    create_res = client.post("/cases", json={
        "title": "Initial Title",
        "description": "Initial Description",
        "status": "OPEN"
    })
    case_id = create_res.json()["id"]

    update_payload = {
        "title": "Updated Title",
        "description": "Updated Description",
        "status": "RESOLVED"
    }
    response = client.put(f"/cases/{case_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == case_id
    assert data["title"] == update_payload["title"]
    assert data["description"] == update_payload["description"]
    assert data["status"] == update_payload["status"]


def test_update_nonexistent_case_returns_404(client):
    """Test updating a non-existent case returns HTTP 404."""
    update_payload = {
        "title": "Updated Title",
        "description": "Updated Description",
        "status": "RESOLVED"
    }
    response = client.put("/cases/88888", json=update_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["error"]["code"] == "CASE_NOT_FOUND"


def test_delete_existing_case(client):
    """Test deleting an existing case returns 204 No Content."""
    create_res = client.post("/cases", json={
        "title": "Temporary Case",
        "description": "To be deleted.",
        "status": "OPEN"
    })
    case_id = create_res.json()["id"]

    delete_res = client.delete(f"/cases/{case_id}")
    assert delete_res.status_code == status.HTTP_204_NO_CONTENT
    assert delete_res.text == ""

    # Verify case no longer exists
    get_res = client.get(f"/cases/{case_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_case_returns_404(client):
    """Test deleting a non-existent case returns 404 Not Found."""
    response = client.delete("/cases/77777")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["error"]["code"] == "CASE_NOT_FOUND"


def test_validation_errors(client):
    """Test string length validation errors."""
    payload = {
        "title": "",
        "description": "Valid description",
        "status": "OPEN"
    }
    response = client.post("/cases", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_database_rollback_on_service_exception():
    """Test service layer exception handling and transaction rollback on database failure."""
    mock_db = MagicMock()
    mock_db.add.side_effect = SQLAlchemyError("Database error simulation")

    case_in = CaseCreate(
        title="Error Case",
        description="Will trigger DB error",
        status="OPEN"
    )

    with pytest.raises(SQLAlchemyError):
        CaseService.create_case(db=mock_db, case_in=case_in)
    mock_db.rollback.assert_called_once()

    # Test update rollback
    mock_db_update = MagicMock()
    mock_case = Case(id=1, title="T", description="D", status="OPEN")
    mock_db_update.query.return_value.filter.return_value.first.return_value = mock_case
    mock_db_update.commit.side_effect = SQLAlchemyError("Update DB error")

    update_in = CaseUpdate(title="T2", description="D2", status="CLOSED")
    with pytest.raises(SQLAlchemyError):
        CaseService.update_case(db=mock_db_update, case_id=1, case_in=update_in)
    mock_db_update.rollback.assert_called_once()

    # Test delete rollback
    mock_db_delete = MagicMock()
    mock_db_delete.query.return_value.filter.return_value.first.return_value = mock_case
    mock_db_delete.delete.side_effect = SQLAlchemyError("Delete DB error")

    with pytest.raises(SQLAlchemyError):
        CaseService.delete_case(db=mock_db_delete, case_id=1)
    mock_db_delete.rollback.assert_called_once()


def test_case_model_repr():
    """Test Case model __repr__ output."""
    case = Case(id=42, title="Test Case", description="Desc", status="OPEN")
    assert "<Case id=42 title='Test Case' status='OPEN'>" in repr(case)


def test_get_db_dependency():
    """Test get_db dependency lifecycle."""
    gen = get_db()
    session = next(gen)
    assert session is not None
    try:
        next(gen)
    except StopIteration:
        pass


def test_generic_500_exception_handler():
    """Test unhandled exception handler returns HTTP 500 error contract."""
    from unittest.mock import patch
    no_raise_client = TestClient(app, raise_server_exceptions=False)
    with patch("app.services.case_service.CaseService.get_cases", side_effect=Exception("Unexpected crash")):
        response = no_raise_client.get("/cases")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        data = response.json()
        assert data["error"]["code"] == "INTERNAL_SERVER_ERROR"
