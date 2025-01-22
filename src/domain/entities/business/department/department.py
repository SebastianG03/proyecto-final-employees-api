from sqlmodel import Field, SQLModel
from domain.entities.business.business import BusinessBase 
from domain.helpers.common_metadata import schema_info, schema_name

class DepartmentBase(BusinessBase):
    location: str
    
class DepartmentTable(DepartmentBase, table=True):
    SQLModel.__tablename__ = "departments"
    id: int = Field(default=None, primary_key=True)