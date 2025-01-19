from typing import List
from pydantic import BaseModel
from sqlmodel import SQLModel

from domain.entities.skills.skill.skills import SkillTable
from domain.entities.skills.department.department_skills import DepartmentSkillTable
from domain.entities.skills.employee.employee_skills import EmployeeSkillTable

class CollectionModel(BaseModel):
    model_skill_reference: EmployeeSkillTable | DepartmentSkillTable
    skill_reference: SkillTable

class CollectionSkillsModel(BaseModel):
    soft_weight: float = 0
    hard_weight: float = 0
    total_weight: float = 0
    performance: float = 0 

class CollectorBase(BaseModel):
    model_reference: SQLModel
    model_skills: List[CollectionModel]
    skills_raiting: CollectionSkillsModel
    