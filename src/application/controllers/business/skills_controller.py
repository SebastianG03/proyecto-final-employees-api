from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from entities.employee import HardSkills, SoftSkills
from core.database.database import get_session
from core.services.user_service import user_service
import core.datasource.skills_datasource as sd
import entities.helpers.responses as resp


skills_router = APIRouter(prefix="/business/skills", tags=["skills"])

#Hard Skills
@skills_router.post(
    "/hard/create",
    status_code=status.HTTP_201_CREATED
)
def create_hard_skill(
    skill: HardSkills,
    session: Session = Depends(get_session)
):
    user = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        return sd.post_hard_skills(
            skill, session
        )
    except Exception as err:
        return resp.internal_server_error_response(err)

@skills_router.post(
    "/hard/create/list",
    status_code=status.HTTP_201_CREATED
)
def create_hard_skill(
    skills: List[HardSkills],
    session: Session = Depends(get_session)
):
    user = user_service.get_user()
    
    try:
        # if not user:
            # return resp.not_logged_response
        # if not user.is_admin:
            # return resp.unauthorized_access_response
        
        for skill in skills:
            sd.post_hard_skills(
                skill, session
            )
        return resp.created_response("Hard Skills created successfully") 
    except Exception as err:
        return resp.internal_server_error_response(err)


@skills_router.get(
    "/hard/all",
    status_code=status.HTTP_200_OK
)
def get_hard_skills(session: Session = Depends(get_session)):
    try:
        return sd.get_hard_skills(session)
    except Exception as err:
        return resp.internal_server_error_response(err)
    
@skills_router.put(
    "/hard/update/{id}",
    status_code=status.HTTP_202_ACCEPTED
)
def update_hard_skill(
    id: int,
    skill: HardSkills,
    session: Session = Depends(get_session)
):
    user = user_service.get_user()

    try:        
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        
        return sd.update_hard_skills(id, skill, session)
    except Exception as err:
        return resp.internal_server_error_response(err)

#Soft Skills

@skills_router.post(
    "/soft/create",
    status_code=status.HTTP_201_CREATED
)
def create_soft_skill(
    skill: SoftSkills,
    session: Session = Depends(get_session)
):
    user = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        
        return sd.post_soft_skills(
            skill, session
        )
        
    except Exception as err:
        return resp.internal_server_error_response(err) 

@skills_router.post(
    "/soft/create/list",
    status_code=status.HTTP_201_CREATED
)
def create_soft_skill(
    skills: List[SoftSkills],
    session: Session = Depends(get_session)
):
    user = user_service.get_user()
    
    try:
        # if not user:
            # return resp.not_logged_response
        # if not user.is_admin:
            # return resp.unauthorized_access_response
        
        for skill in skills:
            sd.post_soft_skills(
                skill, session
            )
        return resp.created_response("Soft Skills created successfully")
    except Exception as err:
        return resp.internal_server_error_response(err) 


@skills_router.get(
    "/soft/all",
    status_code=status.HTTP_200_OK
)
def get_soft_skills(session: Session = Depends(get_session)):
    return sd.get_soft_skills(session)
        
@skills_router.put(
    "/soft/update/{id}",
    status_code=status.HTTP_202_ACCEPTED
)
def update_soft_skill(
    id: int,
    skill: SoftSkills,
    session: Session = Depends(get_session)
):
    user = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        
        return sd.update_soft_skills(id, skill, session)
    except Exception as err:
        return resp.internal_server_error_response(err)