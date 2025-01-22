from typing import List
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from domain.entities.skills.department.department_skills import (
    DepartmentSkillTable,
    DepartmentSkillPatch
    )
from domain.entities.types.request_types import RequestTypes
from domain.entities.skills.types.skills_types import SkillsTypes
from domain.factory.skill.skills_factory import SkillsFactory

import domain.helpers.responses as resp 

skills_factory = SkillsFactory()

def add_department_skills(
    department_id: int,
    skills: List[DepartmentSkillPatch],
    session: Session
    ) -> JSONResponse:
    try:
        department_skills = List[DepartmentSkillTable]
        for skill in skills:
            department_db =  skills_factory.create(
                request_type=RequestTypes.TABLE_REQUESTS,
                skill_type=SkillsTypes.DEPARTMENT,
                base_content=skill
            )
            department_skills.append(department_db)
        
        session.add_all(department_skills)
        session.commit()

        return resp.created_response("Department skills added successfully")
    except Exception as err:
        raise resp.internal_server_error_response(err)
    
def update_department_skills(
    department_id: int,
    updated_skills: List[DepartmentSkillPatch],
    session: Session
) -> JSONResponse:
    try:
        department_skills: list[DepartmentSkillTable] = session.exec(
            select(DepartmentSkillTable)
            .where(DepartmentSkillTable.department_id == department_id)
            ).all()
        department_skills = filter(lambda x: x.skill_id in [skill.skill_id for skill in updated_skills] , department_skills)
        department_skills = sorted(department_skills, key=lambda x: x.skill_id)
        updated_skills = sorted(updated_skills, key=lambda x: x.skill_id)
        
        for skill, department_skill in zip(updated_skills, department_skills):
            department_skill.sqlmodel_update(skill.model_dump(exclude_unset=True))
            session.add(department_skill)
            session.commit()
            session.refresh(department_skill)
                        
        return resp.successful_fetch_response("Department skills updated successfully")
    except Exception as err:
        raise resp.internal_server_error_response(err)
    
def get_department_skills(
    department_id: int, 
    session: Session) -> JSONResponse | List[DepartmentSkillTable]:
    try:
        departments: List[DepartmentSkillTable] = session.exec(
            select(DepartmentSkillTable)
            .where(DepartmentSkillTable.department_id == department_id)
            ).all()

        if not departments: 
            return resp.object_not_found_error(f"Department with id {department_id} not found")
        
        return departments
    except Exception as err:
        return resp.internal_server_error_response(err)    
    
def delete_department_skills(department_id: int, 
                             skills_id: List[int],
                             session: Session):
    try:
        departments_skills = session.exec(
            select(DepartmentSkillTable)
            .where(DepartmentSkillTable.department_id == department_id)
            .where(DepartmentSkillTable.skill_id in skills_id)
            )
        
        if not departments_skills:
            raise resp.object_not_found_error(f"Department with id {department_id} not found")
        
        for department_skill in departments_skills:
            _delete_department_skill(department_model=department_skill, session=session)
        
        return resp.successful_fetch_response("Department hard skills deleted successfully")
        
    except Exception as err:
        raise resp.internal_server_error_response(err)


def _delete_department_skill(department_model: DepartmentSkillTable, session: Session):
    session.delete(department_model)
    session.commit()