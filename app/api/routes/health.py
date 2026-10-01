from fastapi import APIRouter, status

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Check service health",
    description="Returns the current health status of the Case Management API service."
)
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
