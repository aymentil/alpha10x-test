from fastapi import APIRouter, Query
from typing import Literal
from src.services.external_service import ExternalService
from src.models.organization import OrganizationResponse


router = APIRouter()
external_service = ExternalService()

@router.get("/large_tech_companies")
async def get_large_tech_companies(
    size: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> OrganizationResponse:
    """
    Get list of organizations with pagination.
    
    Args:
        size: Number of items per page (1-100)
        offset: Number of items to skip
        
    Returns:
        Paginated list of large tech organizations
    """

    return await external_service.get_large_tech_companies(size=size, offset=offset)

