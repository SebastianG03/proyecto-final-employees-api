from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import core.datasource.employee_datasource as ds
from entities.helpers.employee_collection import EmployeeValue
import entities.helpers.responses as resp
from core.services.logger_service import logger

from core.database.database import SessionLocal, get_session
from entities.employee.employee import Employee, EmployeeUpdate
from entities.tables import *
from core.services.user_service import user_service


employee_router = APIRouter(prefix="/employees", tags=["employees"])
        
        
#Crud empleados
@employee_router.get(
    "/employee/{id}", 
    status_code=status.HTTP_200_OK,
    )
def getEmployeeById(id: int, session: Session = Depends(get_session)):
    user = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        return ds.get_employee(id, session)
    except Exception as err:
        return resp.internal_server_error_response(err)

@employee_router.get(
    "/managers",
    status_code=status.HTTP_200_OK,
    )
def get_managers(session: Session = Depends(get_session)):   
    try:
        # user = user_service.get_user()
        # if not user:
        #     return resp.not_logged_response
        # if not user.is_admin:
        #     return resp.unauthorized_access_response
        
        return ds.get_managers(session)
        
    except Exception as err:
        return resp.internal_server_error_response(err)


@employee_router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    )
def get_employees(session: Session = Depends(get_session)):   
    try:
        # user = user_service.get_user()
        # if not user:
        #     return resp.not_logged_response
        # if not user.is_admin:
        #     return resp.unauthorized_access_response
        
        return ds.get_all_employees(session)
        
    except Exception as err:
        return resp.internal_server_error_response(err)
    
# Find by skills and weight
@employee_router.get(
    "/sort/employees/weight",
    status_code=status.HTTP_200_OK,
    )
def find_employees_by_weight(session: Session = Depends(get_session)):
    user = user_service.get_user()
    try:
        # if not user:
        #     return resp.not_logged_response
        # if not user.is_admin:
        #     return resp.unauthorized_access_response
        sorted_employees = ds.get_employees_by_weight(session)
        sorted_employees = _set_comments(sorted_employees)
        response = [employee.to_dict() for employee in sorted_employees]
        return response
    except Exception as err:
        return resp.internal_server_error_response(err)
    
@employee_router.get(
    "/sort/managers/weight",
    status_code=status.HTTP_200_OK,
    )
def find_managers_by_weight(session: Session = Depends(get_session)):
    # user = user_service.get_user()
    try:
        # if not user:
        #     return resp.not_logged_response
        # if not user.is_admin:
        #     return resp.unauthorized_access_response
        managers = get_managers(session)
        logger.info("Step 1: Get mangers")
        sorted_managers = ds.get_employees_by_weight(employees=managers, session=session)
        logger.info("Step 2: Sort mangers")
        sorted_managers = _set_comments(sorted_managers)
        logger.info("Sorted Managers")
        response = [manager.to_dict() for manager in sorted_managers]
        return response
        
    except Exception as err:
        return resp.internal_server_error_response(err)
    
    
@employee_router.get(
    "/find/by/hard-skill",
    status_code=status.HTTP_200_OK,
)
def find_employees_by_hard_skill(skill_id: int, session: Session = Depends(get_session)):
    user = user_service.get_user()
    try:
        # if not user:
        #     return resp.not_logged_response
        # if not user.is_admin:
        #     return resp.unauthorized_access_response
        sorted_employees = ds.get_employees_by_hard_skill(skill_id, session)
        sorted_employees = _set_comments(sorted_employees)
        response = [employee.to_dict() for employee in sorted_employees]
        return response
    except Exception as err:
        return resp.internal_server_error_response(err)
    
@employee_router.get(
    "/find/by/soft-skill",
    status_code=status.HTTP_200_OK,
)
def find_employees_by_soft_skill(skill_id: int, session: Session = Depends(get_session)):
    user = user_service.get_user()
    try:
        # if not user:
        #     return resp.not_logged_response
        # if not user.is_admin:
        #     return resp.unauthorized_access_response
        sorted_employees = ds.get_employees_by_soft_skill(skill_id, session)
        response = [employee.to_dict() for employee in sorted_employees]
        return response
    except Exception as err:
        return resp.internal_server_error_response(err)
    
    
def _set_comments(employees: List[EmployeeValue]):
    for employee in employees:
            soft_weight = employee.soft_weight
            hard_weight = employee.hard_weight
            total_weight = employee.weight
            comments = {
                "Total weight result:": comment_weight(total_weight),
                "Soft weight result:": comment_weight(soft_weight),
                "Hard weight result:": comment_weight(hard_weight),
            }
            employee.comment = str(comments)
    return employees
    
def comment_weight(weight: float):
    if weight < 10:
        return "Unknown"
    elif weight >= 10 and weight <= 100:
        return "Low relevance"
    elif weight > 100 and weight <= 350:
        return "Relevant"
    elif weight > 350 and weight <= 700:
        return "Essential"
    elif weight > 700:
        return "Priceless"