from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class EmployeeBase(SQLModel):
    name: str
    password: str
    role: str
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
    __tablename__ = "employees"
    id: int = Field(default=None, primary_key=True, index=True, unique=True)
    department_id: int = Field(foreign_key="departments.id", nullable=False)
    position_id: int = Field(foreign_key="positions.id", nullable=False)
    
    
class EmployeePatch(EmployeeBase):
    department_id: int
    position_id: int