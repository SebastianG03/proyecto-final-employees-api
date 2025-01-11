from sqlmodel import Field
from src.entities.merge.business.business import BusinessBase 

class DepartmentBase(BusinessBase):
    location: str
    
class DepartmentTable(DepartmentBase):
    id: int = Field(default=None, primary_key=True, index=True, unique=True)