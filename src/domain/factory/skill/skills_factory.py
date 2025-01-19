from sqlmodel import SQLModel
from domain.factory.factory import FactoryBase
from domain.entities.skills.types.skills_types import SkillsTypes
from domain.entities.skills.department.department_skills import (
    DepartmentSkillTable,
    DepartmentSkillPatch
    )
from domain.entities.skills.employee.employee_skills import (
    EmployeeSkillTable,
    EmployeeSkillPatch
    )
from domain.entities.skills.skill.skills import (
    SkillCategoryBase,
    SkillTable,
    SkillBase)
from domain.entities.types.request_types import RequestTypes

class SkillsFactory(FactoryBase):
    
    def create(
        self, 
        skill_type: SkillsTypes,
        request_type: RequestTypes,
        base_content: SQLModel   
        ) -> SkillCategoryBase:
        if skill_type == SkillsTypes.DEPARTMENT:
            return self._get_request_type(
                request_type=request_type,
                table_type=DepartmentSkillTable,
                patch_type=DepartmentSkillPatch,
                get_type=DepartmentSkillTable,
                base_content=base_content
            )
        elif skill_type == SkillsTypes.EMPLOYEE:
            return self._get_request_type(
                request_type=request_type,
                table_type=EmployeeSkillTable,
                get_type=EmployeeSkillTable,
                patch_type=EmployeeSkillPatch,
                base_content=base_content
            )
        elif skill_type == SkillsTypes.SKILLS:
            return self._get_request_type(
                request_type=request_type,
                table_type=SkillTable,
                get_type=SkillTable,
                patch_type=SkillBase,
                base_content=base_content
            )