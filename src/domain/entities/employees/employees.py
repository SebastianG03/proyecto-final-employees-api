from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from domain.entities.employees.employees_roles import EmployeeRoles
from domain.entities.business.department.department import DepartmentTable
from domain.entities.business.position.position import PositionTable 
from domain.helpers.common_metadata import schema_name, schema_info



class EmployeeBase(SQLModel):
    name: str
    password: str
    role: EmployeeRoles
    leadsTeam: bool
    email: EmailStr
    phone: Optional[str]
    address: str
    salary: float
    daily_hours: int = 8
    time_employee_months: int = 1
    performance: float = 0
    projects_completed: float = 0
    projects_cancelled: float = 0
    projects_rejected: float = 0
    pair_raiting: float = 0
    team_raiting: float = 0
    inmediate_boss_raiting: float = 0
    
    
class EmployeeTable(EmployeeBase, table=True):
    SQLModel.__tablename__ = "employees"
    SQLModel.__table_args__ = {"extend_existing": True}
    id: int = Field(default=None, primary_key=True, index=True, unique=True)
    department_id: int = Field(foreign_key="departments.id", nullable=False)
    position_id: int = Field(foreign_key="positions.id", nullable=False)
    
    
    
class EmployeePatch(EmployeeBase):
    department_id: int
    position_id: int