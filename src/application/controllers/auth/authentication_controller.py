from datetime import timedelta
from fastapi import APIRouter, Response, status


from fastapi import Depends
from fastapi.responses import JSONResponse
from requests import Session


import core.datasource.employee_datasource as ds
import entities.helpers.responses as resp
from core.datasource.auth_datasource import (
    authenticate_user,
    # create_access_token
    )
from entities.employee.employee import Employee, EmployeeUpdate
from entities.auth.auth_data import ACCESS_TOKEN_EXPIRE_MINUTES
from entities.auth.token import Token
from entities.auth.user import LoginModel, User
from core.services.user_service import user_service
from core.database.database import get_session
from entities.tables.employee_tables import EmployeeModel
from entities.employee.workload import Workload

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/token")
def login_for_access_token(
    login_data: LoginModel) -> Token:
    try:
        user = authenticate_user(login_data.email, login_data.password)
        # token = create_access_token(user_data=user.to_dict(), 
        #                             expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        # token_data = Token(access_token=token, token_type="HS256")
        if not user:
            return resp.invalid_tokens_response
        
        employee_user: EmployeeUpdate = EmployeeUpdate(
            id=user.id,
            name=user.name,
            Password=user.password,
            email=user.email,
            phone=user.phone,
            workload=user.workload,
            Position=user.position_id,
            Department=user.department_id,
            Address=user.address,
            Salary=user.salary
        ) 
        user_service.set_user(user = User(user_data = employee_user))
        return resp.login_successful_response(user.to_dict()) 
    except Exception as err:
        return resp.internal_server_error_response(err)

@auth_router.get("/users/me/")
async def read_users_me():
    user = user_service.get_user()
    try:
        if user:
            data: EmployeeModel = user.user_data
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=user_service.user_json(),
            )
        else:
            return resp.not_logged_response
    except Exception as err:
        return resp.internal_server_error_response(err)
    
@auth_router.post(
    "/users/create",
    status_code=status.HTTP_201_CREATED,
    )
def create_user(employee: Employee, session: Session = Depends(get_session)):
    try:
        user = user_service.get_user()
        if user:
            return resp.already_logged_response
        
        validation = user_service.get_user_by_email(email=employee.email)
        if validation:
            return resp.user_exists_response
        
        if employee.workload.lower() not in Workload._value2member_map_:
            return resp.invalid_format_error_response(
                "Workload invalid. Value has to be one of this: 'no work', 'low', 'medium', 'high', 'overwork'."
                )
        
        ds.create_employee(employee, session)
        user = user_service.get_user_by_email(email=employee.email)
        # token = create_access_token(user_data=user.to_dict(), 
        #                             expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        # token_data = Token(access_token=token, token_type="HS256")
        
        employee_user: EmployeeUpdate = EmployeeUpdate(
            id=user.id,
            name=user.name,
            Password=user.password,
            email=user.email,
            phone=user.phone,
            workload=user.workload,
            Position=user.position_id,
            Department=user.department_id,
            Address=user.address,
            Salary=user.salary
        ) 
        user_service.set_user(user = User(user_data = employee_user))
             
        return Response(content="User created and logged.")
    except Exception as err:
        return resp.internal_server_error_response(err)
    
@auth_router.put(
    "/users/update/{id}",
    status_code=status.HTTP_200_OK,
    )
def updateEmployee(employee: EmployeeUpdate, 
                   session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    try:
        if user:
            return ds.update_employee(user.user_data.id, employee, session)
        else: 
            return resp.not_logged_response
    except Exception as err:
        return resp.internal_server_error_response(err)


@auth_router.get(
    "/users/logout",
    status_code=status.HTTP_200_OK,
)
def logout():
    user = user_service.get_user()
    
    try:
        if user:
            user_service.logout()
            resp.logout_response(True)

        return resp.logout_response(False)
    except Exception as err:
        return resp.internal_server_error_response(err)