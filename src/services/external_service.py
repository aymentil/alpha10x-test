from typing import Dict, List, Tuple, Optional
import httpx
from fastapi import HTTPException, status
from src.core.config import settings
from src.models.organization import OrganizationBase, OrganizationResponse
from src.models.transformed_organization import TransformedOrganizationBase, TransformedOrganizationResponse

class ExternalService:
    def __init__(self):
        self.base_url = settings.EXTERNAL_SERVICE_URL
        self.headers = {"api-key": settings.API_KEY}

    async def get_organizations(
        self,
        size: int = settings.DEFAULT_PAGE_SIZE,
        offset: int = 0,
        min_employees: int = 0,
        country: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> OrganizationResponse:
        """
        Fetch organizations from external service with pagination.
        
        Args:
            size: Number of items per page
            offset: Number of items to skip
            min_employees: Minimum number of employees
            country: Filter by country
            sort_by: Sort by field (None, employee_count, founded)
            sort_order: Sort order (asc, desc)
            
        Returns:
            Dictionary containing list of organizations and total count
        """
        # Validate sort_by parameter
        if sort_by not in {None, "employee_count", "founded"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sort_by parameter. Must be one of None, 'employee_count', or 'founded'."
            )

        # Build query parameters
        params = {
            "size": size,
            "offset": offset,
            "min_employees": min_employees,
            "country": country,
            "sort_by": sort_by,
            "sort_order": sort_order
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/data",
                    params=params,
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                return OrganizationResponse(
                    organizations=[OrganizationBase(**org) for org in data["data"]],
                    average_employees=sum(org["employee_count"] for org in data["data"]) / len(data["data"]) if len(data["data"]) else 0
                )

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error communicating with external service: {str(e)}"
            )
    
    async def get_transformed_organizations(
        self,
        size: int = settings.DEFAULT_PAGE_SIZE,
        offset: int = 0,
        min_employees: int = 0,
        country: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> TransformedOrganizationResponse:
        """
        Fetch organizations from external service, transform the data, and return it.
        
        Args:
            size: Number of items per page
            offset: Number of items to skip
            min_employees: Minimum number of employees
            country: Filter by country
            sort_by: Sort by field (None, employee_count, founded)
            sort_order: Sort order (asc, desc)
            
        Returns:
            Dictionary containing list of transformed organizations and total count
        """
        # Fetch organizations
        organization_response = await self.get_organizations(
            size=size,
            offset=offset,
            min_employees=min_employees,
            country=country,
            sort_by=sort_by,
            sort_order=sort_order
        )

        # Transform the data
        transformed_organizations = [
            TransformedOrganizationBase(
                name=org.name,
                country=org.country,
                employee_count=org.employee_count,
                is_large=org.employee_count >= 1000,
            )
            for org in organization_response.organizations
        ]

        return TransformedOrganizationResponse(
            organizations=transformed_organizations,
            average_employees=organization_response.average_employees
        )
    
    