from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from domain.entities.business.department.department import DepartmentBase, DepartmentTable
from core.database.database import get_session
from core.services.user_service import UserService
import core.datasource.business_datasource as bd
import domain.helpers.responses as resp

department_router = APIRouter(prefix="/business/departments", tags=["departments"])
user_service = UserService()

@department_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED
    )
def post_department(
    department: DepartmentTable,
    session: Session = Depends(get_session)):
    user = user_service.get_user()
    
    
    try:
        # if not user:
        #     return resp.not_logged_response
        # if not user.is_admin:
        #     return resp.unauthorized_access_response
        return bd.create_department(department, session)
    except Exception as err:
        return resp.internal_server_error_response(err)
        
@department_router.post(
    "/create/list",
    status_code=status.HTTP_201_CREATED
    )
def post_department(
    departments: List[DepartmentBase],
    session: Session = Depends(get_session)):
    user = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        for department in departments:
            bd.create_department(department, session)
        return resp.created_response("Departments created successfully")
    except Exception as err:
        return resp.internal_server_error_response(err)
        

@department_router.get(
    "/all",
    status_code=status.HTTP_200_OK
)
def get_departments(
    session: Session = Depends(get_session)
):
    return bd.get_departments(session)

@department_router.put(
    "/update/{id}",
    status_code=status.HTTP_202_ACCEPTED
)
def update_department(  
    id: int,
    department: DepartmentBase,
    session: Session = Depends(get_session)
    ):
    user = user_service.get_user()
    is_admin = user.is_admin
    
    try:
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        
        return bd.update_department(
            id=id,
            department=department,
            session=session)
        
    except Exception as err:
        return resp.internal_server_error_response(err) 
