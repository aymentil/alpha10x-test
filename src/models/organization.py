from pydantic import BaseModel
from typing import Optional, List

class OrganizationBase(BaseModel):
    name: str
    country: str
    employee_count: int
    industry: str
    founded: int

class OrganizationResponse(BaseModel):
    organizations: List[OrganizationBase]
    average_employees: Optional[float] = None