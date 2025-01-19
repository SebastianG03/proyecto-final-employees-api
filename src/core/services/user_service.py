import base64
from datetime import datetime, timedelta, timezone
from sqlmodel import select, Session
from core.services.logger_service import logger

from domain.entities.auth.user import User
from domain.entities.employees.employees import EmployeeTable
from domain.entities.employees.employees_roles import EmployeeRoles
from domain.entities.business.department.department import DepartmentTable
from domain.entities.business.position.position import PositionTable

from domain.entities.interfaces.singleton import FactorySingleton

import domain.helpers.responses as resp 

from core.database.database import SessionLocal


class UserService(metaclass = FactorySingleton):
    def __init__(self):
        self.user: User | None = None
    
    def get_user_by_email(self, email: str, session: Session) -> EmployeeTable | None:
        result: EmployeeTable | None = session.exec(
            select(EmployeeTable)
            .where(EmployeeTable.email == email)
            .limit(1)
        ).one_or_none()
        if result:
            return result
        return None
        
    def set_user(self, employee: EmployeeTable):
        connection_time = datetime.now(timezone.utc)
        expired_time = connection_time + timedelta(minutes=30)
        self.user = User(
            connection_time=connection_time,
            expire_time=expired_time,
            is_admin= employee.leadsTeam,
            user_data=employee
        )
        
    def logout(self):
        self.user = None
    
    def get_user(self) -> User | None : 
        actual_time = datetime.now(timezone.utc)
        if not self.user:
            return None
        
        if self.user.expire_time > actual_time:
            return self.user
        else:
            self.logout()
            return None
            
    
    def user_json(self, session: Session) -> dict:
        if self.user is None:
            return {}
        employee: EmployeeTable = self.user.user_data
        department: DepartmentTable = session.get(DepartmentTable, employee.department_id)
        position: PositionTable = session.get(PositionTable, employee.position_id)
        employee_data = employee.model_dump()
        employee_data.pop("department_id")
        employee_data.pop("position_id")
        employee_data["department"] = department.name
        employee_data["position"] = position.name
        return employee_data
    