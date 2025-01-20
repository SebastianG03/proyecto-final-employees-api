from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


import core.datasource.employee_skills_datasource as ds
from core.database.database import get_session
from core.services.user_service import user_service

import domain.helpers.responses as resp
from domain.entities.auth.user import User
from domain.entities.skills.employee.employee_skills import EmployeeSkillPatch, EmployeeSkillTable
from domain.entities.skills.types.skills_categories import SkillsCategories

employee_skills_router = APIRouter(prefix="/employee/skills", tags=["employee skills"])

@employee_skills_router.get("/weight")
def get_user_total_weight(session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    
    if not user:
        return resp.not_logged_response
    
    weight = ds.get_employee_total_weight(employee_id= user.user_data.id, session=session)
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

@employee_skills_router.get("/weight/{category}")
def get_user_weight_by_category(
    category: SkillsCategories,
    session: Session = Depends(get_session)
    ):
    user: User = user_service.get_user()
    
    if not user:
        return resp.not_logged_response
    
    weight = ds.get_skills_weight(
        employee_id=user.user_data.id,
        session=session,
        category=category)
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

@employee_skills_router.get("/all")
def get_user_skills_by_category(
    category: SkillsCategories,
    session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    
    if not user:
        return resp.not_logged_response
    return ds.get_user_skills(employee_id= user.user_data.id, category=category, session=session)


@employee_skills_router.post("/create")
def post_user_skill(
    skills: List[EmployeeSkillPatch],
    session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        if len(skills) == 0 or len(skills) > 30:
            return resp.invalid_format_error_response("You have to select at least 1 and at most 20 skills.")
        for skill in skills:
            response = ds.post_user_skill(
                skill=skill,
                session=session)
        return resp.created_response(response)
        
    except Exception as err:
        return resp.internal_server_error_response(err)

@employee_skills_router.put("/update")
def update_user_skills(
    employee_skill: EmployeeSkillPatch,
    skill_id: int,
    domain: int, 
    session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    
    try:
        if not user:
            return resp.not_logged_response
        return ds.update_user_skills(
            employee_skill=employee_skill,
            employee_id=user.user_data.id,
            skill_id=skill_id,
            session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)

@employee_skills_router.delete("/delete")
def delete_user_skills(
    skills_ids: List[int], 
    session: Session = Depends(get_session)):
    user: User = user_service.get_user()
    try:
        if not user:
            return resp.not_logged_response
        return ds.delete_user_skills(user.user_data.id, skills_ids=skills_ids, session=session)
    except Exception as err:
        return resp.internal_server_error_response(err)