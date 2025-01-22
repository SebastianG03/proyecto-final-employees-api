from sqlmodel import Field, SQLModel

from domain.entities.skills.skill.skills import SkillCategoryBase
from domain.entities.skills.employee.employee_domain import DomainBase
from domain.entities.employees.employees import EmployeeTable
from domain.entities.skills.skill.skills import SkillTable

class EmployeeSkillBase(DomainBase, SkillCategoryBase):
    pass

class EmployeeSkillTable(EmployeeSkillBase, table=True):
    SQLModel.__tablename__ = "employee_skills"
    id: int = Field(default=None, primary_key=True, index=True, unique=True)
    employee_id: int = Field(foreign_key="employees.id", nullable=False)    
    skill_id: int = Field(foreign_key="skills.id", nullable=False)
    
    
class EmployeeSkillPatch(EmployeeSkillBase):
    employee_id: int
    skill_id: int
    