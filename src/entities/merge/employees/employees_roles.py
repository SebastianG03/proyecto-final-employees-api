import enum

class EmployeeRoles(str, enum):
    ADMIN = "admin",
    TRAINEE = "trainee",
    TEAM_MANAGER = "team manager",
    DEPARTMENT_MANAGER = "department manager",
    INTERN = "intern"