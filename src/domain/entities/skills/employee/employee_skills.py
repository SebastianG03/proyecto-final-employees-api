from sqlmodel import Field, SQLModel

from src.domain.entities.skills.skill.skills import SkillTypeBase
from src.domain.entities.skills.employee.employee_domain import DomainBase

class EmployeeSkillBase(DomainBase, SkillTypeBase):
    pass

class EmployeeSkillTable(EmployeeSkillBase, table=True):
    __tablename__ = "employee_skills"
    id: int = Field(default=None, primary_key=True, index=True, unique=True)
    employee_id: int = Field(foreign_key="employees.id", nullable=False)    
    skill_id: int = Field(foreign_key="skills.id", nullable=False)
    
    
class EmployeeSkillPatch(EmployeeSkillBase):
    employee_id: int
    skill_id: int
    