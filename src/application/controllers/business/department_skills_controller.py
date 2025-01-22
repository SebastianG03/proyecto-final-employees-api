from typing import List, Optional
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Session

from core.database.database import get_session
import core.datasource.department_skills_datasource as bd
import domain.helpers.responses as resp
from domain.entities.skills.department.department_skills import DepartmentSkillPatch, DepartmentSkillTable
from core.services.user_service import UserService

dep_skills_router = APIRouter(prefix="/business/departments/skills", tags=["department skills"])
user_service = UserService()


@dep_skills_router.get("/all", status_code=status.HTTP_200_OK)
def get_dep_hard_skills(
    department_id: int,
    session: Session = Depends(get_session)):
    try:
        response = bd.get_department_skills(department_id=department_id, session=session)
        
        if isinstance(response, dict):
            return resp.successful_fetch_response(response['hard_skills'])
        return response
    except Exception as err:
        return resp.internal_server_error_response(err)
    
@dep_skills_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_department_skills(
    department_id: int,
    dep_skill: List[DepartmentSkillPatch], 
    session: Session = Depends(get_session)):
    try:
        # user = user_service.get_user()
        
        # if not user:
        #     return resp.not_logged_response
        # if not user.is_admin:
        #     return resp.unauthorized_access_response
        
        return bd.add_department_skills(
            department_id=department_id,
            skills=dep_skill,
            session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)

@dep_skills_router.put("/update/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_department_skills(
    department_id: int,
    dep_skill: List[DepartmentSkillPatch],
    session: Session = Depends(get_session)
    ):
    try:
        user = user_service.get_user()
        
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        
        return bd.update_department_skills(
            department_id=department_id,
            updated_skills=dep_skill,
            session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)

@dep_skills_router.delete("/delete/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_department_skills(
    department_id: int,
    skills_id: List[int],
    session: Session = Depends(get_session)):
    try:
        user = user_service.get_user()
        
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        
        return bd.delete_department_skills(
            department_id=department_id,
            skills_id=skills_id,
            session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)