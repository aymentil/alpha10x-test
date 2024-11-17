from typing import Dict, List, Tuple
import httpx
from fastapi import HTTPException, status
from src.core.config import settings
from src.models.organization import OrganizationBase, OrganizationResponse

class ExternalService:
    def __init__(self):
        self.base_url = settings.EXTERNAL_SERVICE_URL
        self.headers = {"api-key": settings.API_KEY}

    async def get_organizations(
        self,
        size: int = settings.DEFAULT_PAGE_SIZE,
        offset: int = 0
    ) -> OrganizationResponse:
        """
        Fetch organizations from external service with pagination.
        
        Args:
            size: Number of items per page
            offset: Number of items to skip
            
        Returns:
            Dictionary containing list of organizations and total count
        """
        # Build query parameters
        params = {
            "size": size,
            "offset": offset
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
                    total=data["total_records"],
                    average_employees=sum(org["employee_count"] for org in data["data"]) / len(data["data"])
                )

        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error communicating with external service: {str(e)}"
            )