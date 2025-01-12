from pydantic import BaseModel
from src.domain.entities.business.department.department import DepartmentTable
from src.domain.entities.skills.department.department_skills import DepartmentSkillTable
from src.domain.entities.skills.skill.skills import SkillTable

class DepartmentSkillsEntity(BaseModel):
    department: DepartmentTable
    department_skill: DepartmentSkillTable
    skill: SkillTable

class DepartmentSkillsCollection(list[DepartmentSkillsEntity]):
    def append():
        pass
    def delete():
        pass
    
    def sort():
        pass
    
    def delete_where():
        pass
    
    def find():
        pass     