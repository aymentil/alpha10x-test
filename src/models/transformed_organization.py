from pydantic import BaseModel
from typing import Optional, List

class TransformedOrganizationBase(BaseModel):
    name: str
    country: str
    employee_count: int
    is_large: bool

class TransformedOrganizationResponse(BaseModel):
    organizations: List[TransformedOrganizationBase]
    average_employees: Optional[float] = None