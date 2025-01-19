from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select

from core.services.logger_service import logger

from domain.entities.skills.skill.skills import SkillTable, SkillBase
from domain.entities.skills.types.skills_types import SkillsTypes
from domain.entities.skills.types.skills_categories import SkillsCategories
from domain.entities.types.request_types import RequestTypes 
from domain.factory.skill.skills_factory import SkillsFactory

skills_factory = SkillsFactory()

def post_skills(
    skill: SkillTable, 
    session: Session) -> SkillTable:
    skill_db = skills_factory.create(
        request_type=RequestTypes.TABLE_REQUESTS,
        skill_type=SkillsTypes.SKILLS,
        base_content=skill
    )
    
    session.add(skill_db)
    session.commit()
    session.refresh(skill_db)
    
    return skill_db

def get_skills(session: Session) -> List[SkillTable]:
    skills = session.exec(select(SkillTable)).all()
    logger.info('Skills: ', skills)
    return skills

def get_skills_by_category(category: SkillsCategories, session: Session) -> List[SkillTable]:
    skills = session.exec(
        select(SkillTable)
        .where(SkillTable.category == category)
    ).all()
    logger.info('Skills: ', skills)
    return skills

def get_skills_by_ids(ids: List[int], session: Session) -> List[SkillTable]:
    skills = session.exec(
        select(SkillTable)
        .where(SkillTable.id in ids)
        ).all()
    logger.info('Skills: ', skills)
    return skills


def update_skills(id: int, skills: SkillBase, session: Session):
    skills_db = session.get(SkillTable, id)
    
    if skills_db:
        skills_db.sqlmodel_update(skills.model_dump(exclude_unset=True))
        
        session.add(skills_db)
        session.commit()
        session.refresh(skills_db)
    else:
        raise HTTPException(status_code=404, detail=f"Hard Skill with id {id} not found")
    return skills_db


