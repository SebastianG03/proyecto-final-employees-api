from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from domain.entities.skills.skill.skills import SkillBase, SkillTable
from domain.entities.skills.types.skills_categories import SkillsCategories
from core.database.database import get_session
from core.services.user_service import user_service
import core.datasource.skills_datasource as sd
import domain.helpers.responses as resp
from core.services.user_service import UserService

skills_router = APIRouter(prefix="/business/skills", tags=["skills"])
user_service = UserService()

@skills_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED
)
def create_skill(
    skill: SkillBase,
    session: Session = Depends(get_session)
):
    user = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        return sd.post_skills(
            skill=skill,
            session=session
        )
    except Exception as err:
        return resp.internal_server_error_response(err)

@skills_router.post(
    "/create/list",
    status_code=status.HTTP_201_CREATED
)
def create_skills(
    skills: List[SkillBase],
    session: Session = Depends(get_session)
):
    user = user_service.get_user()
    
    try:
        # if not user:
            # return resp.not_logged_response
        # if not user.is_admin:
            # return resp.unauthorized_access_response
        
        for skill in skills:
            sd.post_skills(
                skill, 
                session
            )
        return resp.created_response("Hard Skills created successfully") 
    except Exception as err:
        return resp.internal_server_error_response(err)


@skills_router.get(
    "/all",
    status_code=status.HTTP_200_OK
)
def get_skills(session: Session = Depends(get_session)):
    try:
        return sd.get_skills(session)
    except Exception as err:
        return resp.internal_server_error_response(err)
    
    
@skills_router.get(
    "/{category}/all",
    status_code=status.HTTP_200_OK
)
def get_skill_by_category(category: SkillsCategories, session: Session = Depends(get_session)):
    try:
        return sd.get_skills_by_category(category, session)
    except Exception as err:
        return resp.internal_server_error_response(err)
    

@skills_router.put(
    "/update/{id}",
    status_code=status.HTTP_202_ACCEPTED
)
def update_skill(
    id: int,
    skill: SkillBase,
    session: Session = Depends(get_session)
):
    user = user_service.get_user()

    try:        
        if not user:
            return resp.not_logged_response
        if not user.is_admin:
            return resp.unauthorized_access_response
        
        return sd.update_skills(id, skill, session)
    except Exception as err:
        return resp.internal_server_error_response(err)
