from enum import Enum


class SkillsTypes(str, Enum.enum):
    SKILLS = "skills"
    DEPARTMENT = "department_skills"
    EMPLOYEE = "employee_skills"