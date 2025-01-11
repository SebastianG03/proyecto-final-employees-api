from typing import List
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from entities.tables.business_tables import (
    DepartmentsHardSkillsModel,
    DepartmentsSoftSkillsModel,
    DepartmentModel
)
from entities.business.department import DepartmentsSkill
import entities.helpers.responses as resp 

def add_department_skills(
    department_id: int,
    hard_skills: List[DepartmentsSkill],
    soft_skills: List[DepartmentsSkill],
    session: Session
) -> JSONResponse:
    try:
        department = session.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()

        if not department: 
            raise resp.object_not_found_error(f"Department with id {department_id} not found")

        if len(hard_skills) > 0:
            _add_department_hard_skills(department_id=department_id, 
                                        skills=hard_skills,
                                        session=session)

        if len(soft_skills) > 0:
            _add_department_soft_skills(department_id=department_id,
                                        skills=soft_skills,
                                        session=session)
            
        return resp.created_response("Department skills added successfully")
    except Exception as err:
        raise resp.internal_server_error_response(err)
    
def update_department_skills(
    department_id: int,
    hard_skills: List[DepartmentsSkill],
    soft_skills: List[DepartmentsSkill],
    session: Session
) -> JSONResponse:
    try:
        department = session.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()

        if not department: 
            raise resp.object_not_found_error(f"Department with id {department_id} not found")

        if len(hard_skills) > 0:
            _add_department_hard_skills(department_id=department_id, 
                                        skills=hard_skills, 
                                        session=session, 
                                        update=True)

        if len(soft_skills) > 0:
            _add_department_soft_skills(department_id=department_id, 
                                        skills=soft_skills, 
                                        session=session, 
                                        update=True)
            
        return resp.successful_fetch_response("Department skills updated successfully")
    except Exception as err:
        raise resp.internal_server_error_response(err)
    
def get_department_skills(department_id: int, 
                          session: Session) -> JSONResponse | dict[str, list[dict[str, any]]]:
    try:
        department = session.query(DepartmentModel).filter(DepartmentModel.id == department_id).all()

        if not department: 
            return resp.object_not_found_error(f"Department with id {department_id} not found")
        
        department_hard_skills = (session
        .query(DepartmentsHardSkillsModel)
        .filter(DepartmentsHardSkillsModel.department_id == department_id)
        .all())
        department_soft_skills = (session
        .query(DepartmentsSoftSkillsModel)
        .filter(DepartmentsSoftSkillsModel.department_id == department_id)
        .all())
        
        
        return {
            "hard_skills": [skill.to_dict() for skill in department_hard_skills],
            "soft_skills": [skill.to_dict() for skill in department_soft_skills]
        }
    except Exception as err:
        return resp.internal_server_error_response(err)    
    
def delete_department_skills(department_id: int, 
                             skills_id: List[int], 
                             department_model: DepartmentsHardSkillsModel | DepartmentsSoftSkillsModel, 
                             session: Session):
    try:
        department = session.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()
        
        if not department:
            raise resp.object_not_found_error(f"Department with id {department_id} not found")
        
        for skill_id in skills_id:
            skill = (session.query(department_model)
                     .filter(department_model.skill_id == skill_id)
                     .filter(department_model.department_id == department_id)
                     .first())
            
            if not skill:
                raise resp.object_not_found_error(f"Skill with id {skill_id} not found")
            
            _delete_department_skill(department_model=skill, session=session)
        
        return resp.successful_fetch_response("Department hard skills deleted successfully")
        
    except Exception as err:
        raise resp.internal_server_error_response(err)

def _add_department_hard_skills(
    department_id: int,
    skills: List[DepartmentsSkill],
    session: Session,
    update: bool = False
):
    try: 
        for skill in skills:
            department_hard_skill = _set_skill_model(department_id=department_id, 
                                                     skill=skill, 
                                                     deparment_model=DepartmentsHardSkillsModel())
            _upload_data(department_model=department_hard_skill, 
                         session=session, 
                         update=update)
        return resp.successful_fetch_response(f'Department hard skills {"updated" if update else "added"} successfully')
    except Exception as err:
        raise resp.internal_server_error_response(err)
    
def _add_department_soft_skills(
    department_id: int,
    skills: List[DepartmentsSkill],
    session: Session,
    update: bool = False
):
    try: 
        for skill in skills:
            department_soft_skill  = _set_skill_model(department_id=department_id, 
                                                      skill=skill, 
                                                      deparment_model=DepartmentsSoftSkillsModel())
            _upload_data(department_model=department_soft_skill, 
                         session=session, 
                         update=update)
        return resp.successful_fetch_response(f'Department soft skills {"updated" if update else "added"} successfully')
    except Exception as err:
        raise resp.internal_server_error_response(err)
    

def _set_skill_model(
    department_id: int,
    skill: DepartmentsSkill, 
    deparment_model: DepartmentsHardSkillsModel | DepartmentsSoftSkillsModel
    ) ->  DepartmentsHardSkillsModel | DepartmentsSoftSkillsModel:
    deparment_model.department_id = department_id
    deparment_model.skill_id = skill.skill_id
    deparment_model.skill_priority = skill.skill_priority
    deparment_model.skill_segment = skill.skill_segment
    return deparment_model

def _upload_data(
    department_model: DepartmentsHardSkillsModel | DepartmentsSoftSkillsModel,
    session: Session,
    update: bool = False
):
    if not update:
        session.add(department_model)
    session.commit()
    if update:
        session.refresh(department_model)
        
def _delete_department_skill(department_model: DepartmentsHardSkillsModel | DepartmentsSoftSkillsModel, session: Session):
    session.delete(department_model)
    session.commit()