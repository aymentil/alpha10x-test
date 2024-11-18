from fastapi import APIRouter, Query
from typing import Literal
from src.services.external_service import ExternalService
from src.models.transformed_organization import TransformedOrganizationResponse

router = APIRouter()
external_service = ExternalService()

@router.get("/transformed_organizations")
async def get_transformed_organizations(
    size: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    min_employees: int = Query(default=0, ge=0),
    country: str = Query(default=None),
) -> TransformedOrganizationResponse:
    """
    Get list of transformed organizations with pagination.
    
    Args:
        size: Number of items per page (1-100)
        offset: Number of items to skip
        min_employees: Minimum number of employees
        country: Filter by country
        sort_by: Sort by field (None, employee_count, founded)
        sort_order: Sort order (asc, desc)
        
    Returns:
        Paginated list of transformed organizations
    """

    return await external_service.get_transformed_organizations(size=size, offset=offset, min_employees=min_employees, country=country, sort_by='employee_count', sort_order='desc')