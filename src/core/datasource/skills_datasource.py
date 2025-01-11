from typing import List
from fastapi import HTTPException
from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from entities.tables.skills_tables import HardSkillsModel, SoftSkillsModel
from entities.tables.employee_skills_tables import EmployeeHardSkillsModel, EmployeeSoftSkillsModel
from entities.employee.hard_skills import HardSkills
from entities.employee.soft_skills import SoftSkills
from core.services.logger_service import logger


### Hard skills table
def post_hard_skills(
    hard_skill: HardSkills, 
    session: Session) -> dict[str, any]:
    hard_skills_db = HardSkillsModel()
    hard_skills_db.name = hard_skill.name
    hard_skills_db.weight = hard_skill.weight
    
    session.add(hard_skills_db)
    session.commit()
    session.refresh(hard_skills_db)
    
    return hard_skill.model_dump()

def get_hard_skills(session: Session) -> List[HardSkillsModel]:
    hard_skills = session.query(HardSkillsModel).all()
    return hard_skills

def get_hard_skills_by_ids(ids: List[int], session: Session) -> List[HardSkillsModel]:
    hard_skills = session.query(HardSkillsModel).filter(HardSkillsModel.id.in_(ids)).all()
    logger.info('Hard Skills: ', hard_skills)
    return hard_skills


def update_hard_skills(id: int, skills: HardSkills, session: Session):
    skills_db = session.execute(HardSkillsModel).get(id)
    
    if skills_db:
        skills_db.id = id
        skills_db.name = skills.name
        skills_db.weight = skills.weight
        
        session.commit()
        session.refresh(skills_db)
    else:
        raise HTTPException(status_code=404, detail=f"Hard Skill with id {id} not found")
    return skills_db


### Soft Skils Table
def post_soft_skills(
    soft_skill: SoftSkills, 
    session: Session) -> dict[str, any]:
    soft_skills_db = SoftSkillsModel()
    soft_skills_db.name = soft_skill.name
    soft_skills_db.weight = soft_skill.weight
    
    session.add(soft_skills_db)
    session.commit()
    session.refresh(soft_skills_db)
    
    return soft_skill.model_dump()

def get_soft_skills(session: Session) -> List[SoftSkillsModel]:
    soft_skills = session.query(SoftSkillsModel).all()
    return soft_skills

def get_soft_skills_by_ids(ids: List[int], session: Session) -> List[SoftSkillsModel]:
    soft_skills = session.query(SoftSkillsModel).filter(SoftSkillsModel.id.in_(ids)).all()
    logger.info('Soft Skills: ', soft_skills)
    return soft_skills

def update_soft_skills(id: int, skills: SoftSkills, session: Session):
    skills_db = session.execute(SoftSkillsModel).get(id)
    
    if skills_db:
        skills_db.id = id
        skills_db.name = skills.name
        skills_db.weight = skills.weight
        
        session.commit()
        session.refresh(skills_db)
    else:
        raise HTTPException(status_code=404, detail=f"Soft Skill with id {id} not found")
    return skills_db
