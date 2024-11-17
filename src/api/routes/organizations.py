from fastapi import APIRouter, Query
from src.services.external_service import ExternalService
from src.models.organization import OrganizationResponse


router = APIRouter()
external_service = ExternalService()

@router.get("/organizations")
async def get_organizations(
    size: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    min_employees: int = Query(default=0, ge=0),
    country: str = Query(default=None)
) -> OrganizationResponse:
    """
    Get list of organizations with pagination.
    
    Args:
        size: Number of items per page (1-100)
        offset: Number of items to skip
        
    Returns:
        Paginated list of organizations
    """

    return await external_service.get_organizations(size=size, offset=offset, min_employees=min_employees, country=country)
