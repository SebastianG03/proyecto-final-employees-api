from sqlmodel import Field, SQLModel

from domain.entities.skills.skill.skills import SkillCategoryBase, SkillTable
from domain.entities.business.department.department import DepartmentTable

class DepartmentSkillBase(SkillCategoryBase):
    skill_priority: float
    skill_segment: float
    
class DepartmentSkillTable(DepartmentSkillBase, table=True):
    SQLModel.__tablename__ = "departments_skills"
    id: int = Field(default=None, primary_key=True)
    skill_id: int = Field(foreign_key="skills.id", nullable=False)
    department_id: int = Field(foreign_key="departments.id", nullable=False) 
    
class DepartmentSkillPatch(DepartmentSkillBase):
    skill_id: int
    department_id: int
    