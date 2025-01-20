from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import core.datasource.employee_datasource as ds
from domain.entities.employees.employees import EmployeePatch, EmployeeTable
from domain.entities.employees.employees_roles import EmployeeRoles
from domain.entities.skills.types.skills_categories import SkillsCategories
import domain.helpers.responses as resp
from core.services.logger_service import logger

from core.database.database import SessionLocal, get_session
from core.services.user_service import UserService


employee_router = APIRouter(prefix="/employees", tags=["employees"])
user_service = UserService()
        
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
        return ds.get_employees_by_weight(session=session)
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
        logger.info("Sorted Managers")
        return sorted_managers
        
    except Exception as err:
        return resp.internal_server_error_response(err)
    
    
@employee_router.get(
    "/find/by/skill",
    status_code=status.HTTP_200_OK,
)
def find_employees_by_skill_type(category: SkillsCategories, session: Session = Depends(get_session)):
    user = user_service.get_user()
    try:
        # if not user:
        #     return resp.not_logged_response
        # if not user.is_admin:
        #     return resp.unauthorized_access_response
        sorted_employees = ds.get_employees_by_skill_type(skill_type=category, session=session)
        response = [employee.to_dict() for employee in sorted_employees]
        return response
    except Exception as err:
        return resp.internal_server_error_response(err)