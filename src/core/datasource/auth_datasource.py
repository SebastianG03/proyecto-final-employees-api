from fastapi import HTTPException
from sqlmodel import Session


from core.services.user_service import UserService

from domain.entities.employees.employees import  EmployeeTable
from domain.entities.auth.user import User

def authenticate_user(email: str, password: str, session: Session) -> EmployeeTable | None:
    user_service: UserService = UserService() 
    user: EmployeeTable | None = user_service.get_user_by_email(email=email, session=session)
    if not user:
        return None
    if not password == user.password:
        return None
    return user

def get_current_active_user():
    user_service: UserService = UserService() 
    current_user = user_service.get_user()
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


