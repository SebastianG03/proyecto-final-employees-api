from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select

from domain.entities.skills.types.skills_categories import SkillsCategories
from domain.entities.skills.types.skills_types import SkillsTypes
from domain.entities.skills.skill.skills import SkillTable
from domain.entities.skills.employee.employee_skills import EmployeeSkillPatch, EmployeeSkillTable
from domain.entities.employees.employees import EmployeeTable

from domain.collection.employee_skills_collection import (
    EmployeeSkillsCollection, 
    EmployeeSkillModel,
    EmployeeSkillsCollector)

from domain.factory.skill.skills_factory import SkillsFactory
from domain.entities.types.request_types import RequestTypes

from core.services.logger_service import logger
from core.datasource.skills_datasource import get_hard_skills_by_ids, get_soft_skills_by_ids
from core.datasource.department_skills_datasource import get_department_skills 



factory = SkillsFactory()

def get_user_skills(
    employee_id: int,
    category: SkillsCategories, 
    session: Session) -> List[EmployeeSkillTable]:
    result = session.exec(
        select(EmployeeSkillTable)
        .where(EmployeeSkillTable.employee_id == employee_id)
        .where(EmployeeSkillTable.category == category)
    ).all()
    return result


def post_user_skill(
    skill: EmployeeSkillPatch,
    session: Session
) -> EmployeeSkillTable:
    skill_db = factory.create(
        request_type=RequestTypes.PATCH,
        skill_type=SkillsTypes.EMPLOYEE,
        base_content=skill
    )
    session.add(skill_db)
    session.commit()
    session.refresh(skill_db)
    
    return skill_db
    
def update_user_skills(
    employee_id: int,
    skill_id: int,
    employee_skill: EmployeeSkillPatch,
    session: Session):
        original_skill: EmployeeSkillTable = session.exec(
            select(EmployeeSkillTable)
            .where(EmployeeSkillTable.employee_id == employee_id)
            .where(EmployeeSkillTable.skill_id == skill_id)
            .limit(1)
        ).one()
        original_skill.sqlmodel_update(employee_skill.model_dump(exclude_unset=True))
        if original_skill:
            session.add(original_skill)
            session.commit()
            session.refresh(original_skill)
            return original_skill
        else:
            raise HTTPException(status_code=404, detail=f"Soft Skill with id {id} not found")
    
def delete_user_skills(employee_id: int, skills_ids: List[int], session: Session):
    skills = session.exec(
        select(EmployeeSkillTable)
        .where(EmployeeSkillTable.employee_id == employee_id)
        .where(EmployeeSkillTable.skill_id in skills_ids)
    ).all()
    
    for skill in skills:
        session.delete(skill)
        session.commit()

### Employee weight methods

def get_employees_weight(session: Session) -> List[EmployeeSkillsCollector]:
    employee_skills = session.exec(
        select(EmployeeSkillTable)
    ).all()
    employee = session.exec(
        select(EmployeeSkillTable)
        ).all()
    skills_ids = [skill.skill_id for skill in employee_skills]
    skills = session.exec(
        select(SkillTable)
        .where(SkillTable.id in skills_ids)
    ).all()
    
    employee_skill_models = [
        EmployeeSkillModel(skill_reference=skill, model_skill_reference=employee_skill) 
        for skill, employee_skill in zip(skills, employee_skills)
        ]
    
    
    collector = EmployeeSkillsCollector(model_reference=employee, model_skills=employee_skill_models)
    collection = EmployeeSkillsCollection(collection=[collector])
    collection.calculate_total_weight()
    return collection.collection
    


def get_employee_total_weight(employee_id: int, session: Session) -> float:
    return _calculate_employee_weight(employee_id=employee_id, session=session)


def get_skills_weight(
    employee_id: int,
    session: Session,
    skill_category: SkillsCategories
):
    employee_skills = session.exec(
        select(EmployeeSkillTable)
        .where(EmployeeSkillTable.employee_id == employee_id)
    ).all()
    employee = session.get(EmployeeTable, employee_id)
    skills_ids = [skill.skill_id for skill in employee_skills]
    skills = session.exec(
        select(SkillTable)
        .where(SkillTable.id in skills_ids)
    ).all()
    
    employee_skill_models = [
        EmployeeSkillModel(skill_reference=skill, model_skill_reference=employee_skill) 
        for skill, employee_skill in zip(skills, employee_skills)
        ]
    
    
    collector = EmployeeSkillsCollector(model_reference=employee, model_skills=employee_skill_models)
    collection = EmployeeSkillsCollection(collection=[collector])
    collection.calculate_weight(skill_type=skill_category)
    
    if skill_category == SkillsCategories.HARD:
        return collection.collection[0].skills_raiting.hard_weight
    return collection.collection[0].skills_raiting.soft_weight
    

def _calculate_employee_weight(employee_id: int, session: Session):
    employee_skills = session.exec(
        select(EmployeeSkillTable)
        .where(EmployeeSkillTable.employee_id == employee_id)
    ).all()
    employee = session.get(EmployeeTable, employee_id)
    skills_ids = [skill.skill_id for skill in employee_skills]
    skills = session.exec(
        select(SkillTable)
        .where(SkillTable.id in skills_ids)
    ).all()
    
    employee_skill_models = [
        EmployeeSkillModel(skill_reference=skill, model_skill_reference=employee_skill) 
        for skill, employee_skill in zip(skills, employee_skills)
        ]
    
    
    collector = EmployeeSkillsCollector(model_reference=employee, model_skills=employee_skill_models)
    collection = EmployeeSkillsCollection(collection=[collector])
    collection.calculate_total_weight()
    return collection.collection[0].skills_raiting.total_weight
    
