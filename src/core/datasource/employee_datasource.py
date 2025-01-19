from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select


from core.services.logger_service import logger

from domain.factory.employee.employees_factory import EmployeesFactory

from domain.entities.employees.employees import EmployeePatch, EmployeeTable
from domain.entities.employees.employees_roles import EmployeeRoles
from domain.entities.types.request_types import RequestTypes

from domain.collection.employee_skills_collection import EmployeeSkillsCollection, EmployeeSkillsCollector

factory: EmployeesFactory = EmployeesFactory()


def get_employee(
    id: int,
    session: Session
    ) -> EmployeeTable:
    employee = session.get(EmployeeTable, id)
    return employee

def get_managers(session: Session) -> List[EmployeeTable]:
    employees = session.exec(select(EmployeeTable)
                            .where(EmployeeTable.leadsTeam == True)
                            .offset(0)
                            .limit(100)).all()
    return employees        

def get_all_employees(session: Session) -> List[EmployeeTable]: 
    employees = session.exec(select(EmployeeTable)
                 .offset(0)
                 .limit(100)).all()
    return employees

def create_employee(
        employee: EmployeePatch,
        session: Session
        ) -> EmployeeTable:
    employee_db: EmployeeTable = factory.create(
        requestType=RequestTypes.TABLE_REQUESTS,
        base_content=employee
        )
    session.add(employee_db)
    session.commit()
    session.refresh(employee_db)
    return employee_db
    

def update_employee(
    id: int, 
    employee: EmployeePatch, 
    session: Session
    ) -> EmployeeTable:
    employee_db: EmployeeTable = session.get(EmployeeTable, id)
    employee_db.sqlmodel_update(employee.model_dump(exclude_unset=True))
    
    session.add(employee_db)
    session.commit()
    session.refresh(employee_db)
    return employee_db


def delete_employee(id: int, session: Session):
    employee = session.get(EmployeeTable, id)
    session.delete(employee)
    session.commit()

### Sort employees methods


def get_employees_by_weight(
    session: Session,
    employees: List[EmployeeTable] = []):
    initial_collection = List[EmployeeSkillsCollector]()
    
    for employee in employees:
        initial_collection.append(EmployeeSkillsCollector())

def get_employees_by_skill_type(skill_id: int, session: Session):
    pass
