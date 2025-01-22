from enum import Enum

class EmployeeRoles(str, Enum):
    ADMIN = "admin"
    TRAINEE = "trainee"
    TEAM_MANAGER = "team manager"
    DEPARTMENT_MANAGER = "department manager"
    INTERN = "intern"