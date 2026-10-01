import logging
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.case import Case
from app.schemas.case import CaseCreate, CaseUpdate
from app.exceptions import CaseNotFoundException

logger = logging.getLogger(__name__)


class CaseService:
    """Service layer for Case business logic and database CRUD operations."""

    @staticmethod
    def create_case(db: Session, case_in: CaseCreate) -> Case:
        """Creates a new case in the database."""
        logger.info(f"Creating new case with title: '{case_in.title}'")
        try:
            db_case = Case(
                title=case_in.title,
                description=case_in.description,
                status=case_in.status.value if hasattr(case_in.status, 'value') else case_in.status
            )
            db.add(db_case)
            db.commit()
            db.refresh(db_case)
            logger.info(f"Successfully created case ID {db_case.id}")
            return db_case
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error while creating case: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def get_case(db: Session, case_id: int) -> Case:
        """Retrieves a single case by ID or raises CaseNotFoundException."""
        logger.info(f"Retrieving case ID {case_id}")
        db_case = db.query(Case).filter(Case.id == case_id).first()
        if not db_case:
            raise CaseNotFoundException(case_id=case_id)
        return db_case

    @staticmethod
    def get_cases(db: Session, skip: int = 0, limit: int = 100) -> List[Case]:
        """Retrieves a paginated list of cases."""
        logger.info(f"Retrieving cases list (skip={skip}, limit={limit})")
        return db.query(Case).order_by(Case.id.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update_case(db: Session, case_id: int, case_in: CaseUpdate) -> Case:
        """Performs a full update/replacement of an existing case."""
        logger.info(f"Updating case ID {case_id}")
        db_case = CaseService.get_case(db, case_id)
        try:
            db_case.title = case_in.title
            db_case.description = case_in.description
            db_case.status = case_in.status.value if hasattr(case_in.status, 'value') else case_in.status
            db.commit()
            db.refresh(db_case)
            logger.info(f"Successfully updated case ID {case_id}")
            return db_case
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error while updating case ID {case_id}: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def delete_case(db: Session, case_id: int) -> None:
        """Deletes an existing case by ID."""
        logger.info(f"Deleting case ID {case_id}")
        db_case = CaseService.get_case(db, case_id)
        try:
            db.delete(db_case)
            db.commit()
            logger.info(f"Successfully deleted case ID {case_id}")
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error while deleting case ID {case_id}: {str(e)}", exc_info=True)
            raise
