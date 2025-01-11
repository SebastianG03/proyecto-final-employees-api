from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.database.database import get_session
from core.services.user_service import user_service
import core.datasource.department_skills_datasource as bd
import entities.helpers.responses as resp
from entities.business.department import DepartmentsSkill
from entities.tables.business_tables import DepartmentsHardSkillsModel, DepartmentsSoftSkillsModel

dep_skills_router = APIRouter(prefix="/business/departments/skills", tags=["department skills"])

### Hard Skills
@dep_skills_router.get("/hard/all", status_code=status.HTTP_200_OK)
def get_dep_hard_skills(department_id: int, session: Session = Depends(get_session)):
    try:
        response = bd.get_department_skills(department_id=department_id, session=session)
        
        if isinstance(response, dict):
            return resp.successful_fetch_response(response['hard_skills'])
        return response
    except Exception as err:
        return resp.internal_server_error_response(err)

@dep_skills_router.post("/create/hard", status_code=status.HTTP_201_CREATED)
def create_dep_hard_skills(department_id: int, 
                           dep_skill: List[DepartmentsSkill], 
                           session: Session = Depends(get_session)):
    try:
        # user = user_service.get_user()
        
        # if not user:
        #     return resp.not_logged_response
        # if not user.is_admin:
        #     return resp.unauthorized_access_response
        
        return bd.add_department_skills(department_id=department_id, hard_skills=dep_skill, soft_skills=[], session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)

@dep_skills_router.put("/update/hard/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_dep_hard_skills(department_id: int, dep_skill: List[DepartmentsSkill], session: Session = Depends(get_session)):
    try:
        user = user_service.get_user()
        
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        
        return bd.update_department_skills(department_id=department_id, hard_skills=dep_skill, soft_skills=[], session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)

@dep_skills_router.delete("/delete/hard/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_dep_hard_skills(department_id: int, session: Session = Depends(get_session)):
    try:
        user = user_service.get_user()
        
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        
        return bd.delete_department_skills(department_id=department_id, department_model=DepartmentsHardSkillsModel, session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)


### Soft skills
@dep_skills_router.get("/soft/all", status_code=status.HTTP_200_OK)
def get_dep_soft_skills(department_id: int, session: Session = Depends(get_session)):
    try:
        response = bd.get_department_skills(department_id=department_id, session=session)
        
        if isinstance(response, dict):
            return resp.successful_fetch_response(response['soft_skills'])
        return response
    except Exception as err:
        return resp.internal_server_error_response(err)

@dep_skills_router.post("/create/soft", status_code=status.HTTP_201_CREATED)
def create_dep_soft_skills(department_id: int, dep_skill: List[DepartmentsSkill], session: Session = Depends(get_session)):
    try:
        # user = user_service.get_user()
        
        # if not user:
        #     return resp.not_logged_response
        # if not user.is_admin:
        #     return resp.unauthorized_access_response
        
        return bd.add_department_skills(department_id=department_id, hard_skills=[], soft_skills=dep_skill, session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)

@dep_skills_router.put("/update/soft/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_dep_soft_skills(department_id: int, dep_skill: List[DepartmentsSkill], session: Session = Depends(get_session)):
    try:
        user = user_service.get_user()
        
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        
        return bd.update_department_skills(department_id=department_id, hard_skills=[], soft_skills=dep_skill, session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)

@dep_skills_router.delete("/delete/soft/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_dep_soft_skills(department_id: int, session: Session = Depends(get_session)):
    try:
        user = user_service.get_user()
        
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        
        return bd.delete_department_skills(department_id=department_id, department_model=DepartmentsSoftSkillsModel, session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)