from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


import core.datasource.employee_skills_datasource as ds
from core.database.database import get_session
from core.services.user_service import user_service

import entities.helpers.responses as resp
from entities.auth.user import User
from entities.employee.ablilities import EmployeeAbility
from entities.tables.employee_skills_tables import EmployeeHardSkillsModel, EmployeeSoftSkillsModel


employee_skills_router = APIRouter(prefix="/employee/skills", tags=["employee skills"])

#Weight
@employee_skills_router.get("/weight")
def get_user_weight(session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    
    if not user:
        return resp.not_logged_response
    
    weight = ds.get_employee_weight(employee_id= user.user_data.id, session=session)
    range = "Unknown"
    if weight >= 0.15 and weight <= 1:
        range = "Low relevance"
    elif weight > 1 and weight <= 5:
        range = "Relevant"
    elif weight > 5 and weight <= 10:
        range = "Essential"
    elif weight > 10:
        range = "Priceless"
    
    return {
        "weight": weight,
        "Rango": range,
    }



#Soft user skills

@employee_skills_router.get("/weight/soft")
def get_user_soft_weight(session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    
    if not user:
        return resp.not_logged_response
    
    weight = ds.get_skills_weight(employee_id=user.user_data.id,
                                  session=session,
                                  employee_skill_model=EmployeeSoftSkillsModel)
    range = "Unknown"
    if weight >= 10 and weight <= 100:
        range = "Low relevance"
    elif weight > 100 and weight <= 350:
        range = "Relevant"
    elif weight > 350 and weight <= 700:
        range = "Essential"
    elif weight > 700:
        range = "Priceless"
    
    return {
        "weight": weight,
        "Rango": range,
    }



@employee_skills_router.get("/soft/all")
def get_user_soft_skills(session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    
    if not user:
        return resp.not_logged_response
    return ds.get_user_soft_skills(employee_id= user.user_data.id, session=session)


@employee_skills_router.post("/soft/create")
def post_user_soft_skills(
    soft_skills: List[EmployeeAbility],
    session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        if len(soft_skills) == 0 or len(soft_skills) > 30:
            return resp.invalid_format_error_response("You have to select at least 1 and at most 20 soft skills.")
        response: dict[str, any] = {}
        for skill in soft_skills:
            response = ds.post_user_soft_skills(
                employee_id=user.user_data.id, 
                soft_skill=skill,
                session=session)
        return resp.created_response(response)
        
    except Exception as err:
        return resp.internal_server_error_response(err)

@employee_skills_router.put("/soft/update")
def update_user_soft_skills(
    soft_skill_id: int,
    domain: int, 
    session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        return ds.update_user_soft_skills(
            employee_id=user.user_data.id,
            soft_skill_id=soft_skill_id,
            domain=domain, session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)

@employee_skills_router.delete("/soft/delete")
def delete_user_soft_skills(
    ids: List[int], 
    session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        return ds.delete_user_soft_skills(ids=ids, session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)

#Hard user skills

@employee_skills_router.get("/weight/hard")
def get_user_hard_weight(session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    
    if not user:
        return resp.not_logged_response
    
    weight = ds.get_skills_weight(employee_id=user.user_data.id,
                                  session=session,
                                  employee_skill_model=EmployeeHardSkillsModel)
    range = "Unknown"
    if weight >= 10 and weight <= 100:
        range = "Low relevance"
    elif weight > 100 and weight <= 350:
        range = "Relevant"
    elif weight > 350 and weight <= 700:
        range = "Essential"
    elif weight > 700:
        range = "Priceless"
    
    return {
        "weight": weight,
        "Rango": range,
    }


@employee_skills_router.get("/hard/all")
def get_user_soft_skills(session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    
    if not user:
        return resp.not_logged_response
    return ds.get_user_hard_skills(employee_id= user.user_data.id, session=session)
    
@employee_skills_router.post("/hard/create")
def post_user_hard_skills(
    hard_skills: List[EmployeeAbility],
    session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    try:
        if not user:
            return resp.not_logged_response
        if len(hard_skills) == 0 or len(hard_skills) > 30:
            return resp.invalid_format_error_response("You have to select at least 1 and at most 20 hard skills.")
        
        response: dict[str, any] = {}
        for skill in hard_skills:
            response = ds.post_user_hard_skills(
                employee_id=user.user_data.id, 
                hard_skill=skill, 
                session=session)
        return resp.created_response(response)
    except Exception as err:
        return resp.internal_server_error_response(err)

@employee_skills_router.put("/hard/update")
def update_user_hard_skills(
    hard_skill_id: int,
    domain: int, 
    session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    try:
        if user:
            return ds.update_user_hard_skills(
                employee_id=user.user_data.id, 
                hard_skill_id=hard_skill_id, 
                domain=domain, 
                session=session)
        return resp.not_logged_response
    except Exception as err:
        return resp.internal_server_error_response(err)
    
@employee_skills_router.delete("/hard/delete")
def delete_user_hard_skills(
    ids: List[int], 
    session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    try:
        if user:
            return ds.delete_user_hard_skills(ids=ids, session=session)
        return resp.not_logged_response
    except Exception as err:
        return resp.internal_server_error_response(err)
