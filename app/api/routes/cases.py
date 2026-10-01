from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.case import CaseCreate, CaseUpdate, CaseResponse
from app.services.case_service import CaseService

router = APIRouter(prefix="/cases", tags=["Cases"])


@router.post(
    "",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new case",
    description="Creates a new case with the provided title, description, and status."
)
def create_case(
    case_in: CaseCreate,
    db: Session = Depends(get_db)
):
    """Endpoint to create a new case."""
    return CaseService.create_case(db=db, case_in=case_in)


@router.get(
    "",
    response_model=List[CaseResponse],
    status_code=status.HTTP_200_OK,
    summary="List all cases",
    description="Retrieves a paginated list of cases."
)
def get_cases(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
    db: Session = Depends(get_db)
):
    """Endpoint to list cases with pagination."""
    return CaseService.get_cases(db=db, skip=skip, limit=limit)


@router.get(
    "/{case_id}",
    response_model=CaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Get case details by ID",
    description="Retrieves specific details for a single case by ID."
)
def get_case(
    case_id: int,
    db: Session = Depends(get_db)
):
    """Endpoint to get details of a case by ID."""
    return CaseService.get_case(db=db, case_id=case_id)


@router.put(
    "/{case_id}",
    response_model=CaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Update/replace an existing case",
    description="Performs a full replacement update of an existing case."
)
def update_case(
    case_id: int,
    case_in: CaseUpdate,
    db: Session = Depends(get_db)
):
    """Endpoint to fully update an existing case."""
    return CaseService.update_case(db=db, case_id=case_id, case_in=case_in)


@router.delete(
    "/{case_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a case",
    description="Deletes an existing case by ID."
)
def delete_case(
    case_id: int,
    db: Session = Depends(get_db)
):
    """Endpoint to delete a case by ID."""
    CaseService.delete_case(db=db, case_id=case_id)
    return None
