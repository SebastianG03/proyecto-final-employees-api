from src.domain.factory.factory import FactoryBase
from src.domain.entities.skills.types.skills_types import SkillsTypes
from src.domain.entities.skills.department.department_skills import (
    DepartmentSkillBase, 
    DepartmentSkillTable,
    DepartmentSkillPatch
    )
from src.domain.entities.skills.employee.employee_skills import (
    EmployeeSkillBase,
    EmployeeSkillTable,
    EmployeeSkillPatch
    )
from src.domain.entities.skills.skill.skills import (
    SkillTypeBase,
    SkillTable,
    SkillBase)
from src.domain.entities.types.request_types import RequestTypes

class SkillsFactory(FactoryBase):
    
    
    def __init__(self):
        pass
    
    def create(
        self, 
        skill_type: SkillsTypes,
        request_type: RequestTypes
        ):
        if skill_type == SkillsTypes.DEPARTMENT:
            return self._get_request_type(
                request_type=request_type,
                table_type=DepartmentSkillTable,
                patch_type=DepartmentSkillPatch,
                get_type=DepartmentSkillTable
            )
        elif skill_type == SkillsTypes.EMPLOYEE:
            return self._get_request_type(
                request_type=request_type,
                table_type=EmployeeSkillTable,
                get_type=EmployeeSkillTable,
                patch_type=EmployeeSkillPatch
            )
        elif skill_type == SkillsTypes.SKILLS:
            return self._get_request_type(
                request_type=request_type,
                table_type=SkillTable,
                get_type=SkillTable,
                patch_type=SkillBase
            )