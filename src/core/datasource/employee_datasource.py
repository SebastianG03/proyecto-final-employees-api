from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from entities.employee.employee import Employee, EmployeeUpdate
from entities.tables import *
from entities.helpers.employee_collection import EmployeeValue

from core.services.user_service import user_service
from core.datasource.employee_skills_datasource import (
    get_employee_weight,
    get_skills_weight
    )
from core.services.logger_service import logger

from entities.auth.auth_data import ADMIN_ROLES, ALGORITHM, SECRET_KEY



def get_employee(
    id: int,
    session: Session) -> EmployeeModel:
    employee = session.query(EmployeeModel).get(id) 

    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with id {id} not found")
    return employee

def get_managers(session: Session) -> List[EmployeeModel]:
    
    employees = session.query(EmployeeModel).all()
    managers: List[EmployeeModel] = []

    for employee in employees:
        position_id = employee.position_id
        position: PositionModel = session.query(PositionModel).get(position_id)
        position_name = set(position.name.split())
        
        if any(role in position_name for role in ADMIN_ROLES):
            managers.append(employee)
        
    return managers
        

def get_all_employees(session: Session) -> List[EmployeeModel]: 
    task_list = session.query(EmployeeModel).all() 
    return task_list

def create_employee(
        employee: Employee,
        session: Session) -> dict[str, any]:
    try:
        result = user_service.get_user_by_email(employee.email)
        if result:
            raise HTTPException(status_code=400, detail=f"Employee with email {employee.email} already exists")
        employee_data = employee.model_dump()
        employee_db = EmployeeModel(**employee_data)

        session.add(employee_db)
        session.commit()
        session.refresh(employee_db)

        return employee_data
    except Exception as err:
        raise err

def update_employee(
    id: int, 
    employee: EmployeeUpdate, 
    session: Session) -> dict[str, any]:
    employee_db = session.query(EmployeeModel).get(id)  # Get given id

    if employee_db:
        employee.id = id
        employee_data = employee.model_dump()

        employee_db = EmployeeModel(**employee_data)
        
        for key, value in employee_data.items():
            setattr(employee_db, key, value)
    
        employee_db = employee_data
        session.commit()
        session.refresh(employee_db)
    else:
        raise HTTPException(status_code=404, detail=f"Employee with id {id} not found")

    return employee_db

def delete_employee(id: int, session: Session):
    employee_db = session.query(EmployeeModel).get(id)
    if employee_db:
        session.delete(employee_db)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Employee with id {id} not found")
    return None

### Sort employees methods

def _sort_employees_by_weight(employees: List[EmployeeModel], session: Session) -> List[EmployeeValue]:
    employee_values: List[EmployeeValue]= []

    for employee in employees:
        weight = get_employee_weight(employee.id, session)
        soft_weight = get_skills_weight(employee_id=employee.id,
                                       session=session,
                                       employee_skill_model=EmployeeSoftSkillsModel)
        hard_weight = get_skills_weight(employee_id=employee.id,
                                        session=session,
                                        employee_skill_model=EmployeeHardSkillsModel)
        employee_val = EmployeeValue(employee=employee, 
                                     weight=weight,
                                     hard_weight=hard_weight,
                                     soft_weight=soft_weight)
        employee_values.append(employee_val)
    
    sorted_employees = sorted(employee_values, key=lambda x: x.weight, reverse=True)
    return sorted_employees

def get_employees_by_weight(
    session: Session,
    employees: List[EmployeeModel] = []) -> List[EmployeeValue]:
    if len(employees) == 0:
        employees = get_all_employees(session)
    logger.info('Sorting Employees: ', employees)
    sorted_employees = _sort_employees_by_weight(employees, session)
    logger.info('Sorted Employees: ', sorted_employees)
    return sorted_employees

def get_employees_by_soft_skill(skill_id: int, session: Session) -> List[EmployeeValue]:
    employees: List[EmployeeModel] = get_all_employees(session)
    employee_soft_skills: List[EmployeeSoftSkillsModel] = session.query(EmployeeSoftSkillsModel).all()
    
    if len(employees) == 0 or len(employee_soft_skills) == 0:
        logger.info('No employees found')
        return []
    
    # TODO Optimizar para evitar iteraciones innecesarias
    employees_ids: List[int] = [ employee.employee_id for employee in employee_soft_skills if employee.soft_skill_id == skill_id] 
        
    employee_filtered: List[EmployeeModel] = []
    
    for employee in employees:
        id: int = employee.id
        if id in employees_ids:
            employee_filtered.append(employee)
        
    return _sort_employees_by_weight(employee_filtered, session)

def get_employees_by_hard_skill(skill_id: int, session: Session) -> List[EmployeeValue]:
    employees: List[EmployeeModel] = get_all_employees(session)
    employee_hard_skills: List[EmployeeHardSkillsModel] = session.query(EmployeeHardSkillsModel).all()
    
    if len(employees) == 0 or len(employee_hard_skills) == 0:
        logger.info('No employees found')
        return []
    
    # TODO Optimizar para evitar iteraciones innecesarias
    employees_ids: List[int] = [ employee.employee_id for employee in employee_hard_skills if employee.hard_skill_id == skill_id] 
        
    employee_filtered: List[EmployeeModel] = []
    
    for employee in employees:
        id: int = employee.id
        if id in employees_ids:
            employee_filtered.append(employee)
        
    return _sort_employees_by_weight(employee_filtered, session)