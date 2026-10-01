import logging
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class CaseNotFoundException(Exception):
    """Exception raised when a case is not found."""

    def __init__(self, case_id: int):
        self.case_id = case_id
        self.message = f"Case with id {case_id} was not found"
        super().__init__(self.message)


async def case_not_found_handler(request: Request, exc: CaseNotFoundException) -> JSONResponse:
    """Handler for CaseNotFoundException returning standard HTTP 404 error response."""
    logger.warning(f"Case not found: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": {
                "code": "CASE_NOT_FOUND",
                "message": exc.message
            }
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler for RequestValidationError returning standard HTTP 422 error response."""
    logger.warning(f"Validation error on {request.method} {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed for request parameter or body",
                "details": exc.errors()
            }
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for unhandled server exceptions returning standard HTTP 500 error response."""
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred"
            }
        },
    )
