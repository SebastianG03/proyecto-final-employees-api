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
    performance: float
    projects_completed: float
    projects_cancelled: float
    projects_rejected: float
    pair_raiting: float
    team_raiting: float
    inmediate_boss_raiting: float
    
    
class EmployeeTable(EmployeeBase, table=True):
    __tablename__ = "employees"
    id: int = Field(default=None, primary_key=True, index=True, unique=True)
    department_id: int = Field(foreign_key="departments.id", nullable=False)
    position_id: int = Field(foreign_key="positions.id", nullable=False)
    
    
class EmployeePatch(EmployeeBase):
    department_id: int
    position_id: int