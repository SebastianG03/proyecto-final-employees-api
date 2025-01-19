from sqlmodel import Field
from domain.entities.business.business import BusinessBase 


class DepartmentBase(BusinessBase):
    location: str
    
class DepartmentTable(DepartmentBase):
    __tablename__ = "departments"
    id: int = Field(default=None, primary_key=True, index=True, unique=True)