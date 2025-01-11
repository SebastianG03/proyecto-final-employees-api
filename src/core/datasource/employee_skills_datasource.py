from typing import List
from fastapi import HTTPException
from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from entities.tables.employee_tables import EmployeeModel
from entities.tables.skills_tables import HardSkillsModel, SoftSkillsModel
from entities.tables.employee_skills_tables import EmployeeHardSkillsModel, EmployeeSoftSkillsModel
from entities.employee.ablilities import EmployeeAbility
from entities.business.department import DepartmentsSkill

from core.services.logger_service import logger
from core.datasource.skills_datasource import get_hard_skills_by_ids, get_soft_skills_by_ids
from core.datasource.department_skills_datasource import get_department_skills 

### User Skills table

def get_user_soft_skills(
    employee_id: int, 
    session: Session) -> List[EmployeeSoftSkillsModel]:
    result = session.query(EmployeeSoftSkillsModel).where(
        EmployeeSoftSkillsModel.employee_id == employee_id).all()
    return result

def get_user_hard_skills(
    employee_id: int, 
    session: Session) -> List[EmployeeHardSkillsModel]:
    result = session.query(EmployeeHardSkillsModel).where(
        EmployeeHardSkillsModel.employee_id == employee_id).all()
    return result

### Calculate employee weight

def get_employee_weight(employee_id: int, session: Session) -> float:
    return _calculate_employee_weight(employee_id=employee_id, session=session)

def _calculate_employee_weight(employee_id: int, session: Session):
    employee_data: EmployeeModel = session.query(EmployeeModel).get(employee_id)
    department_id = employee_data.department_id
    
    employee_hard_skills = get_user_hard_skills(employee_id=employee_id, session=session)
    employee_soft_skills = get_user_soft_skills(employee_id=employee_id, session=session)
    
    if len(employee_hard_skills) == 0 and len(employee_soft_skills) == 0:
        return 0
    
    department_skills = get_department_skills(department_id=department_id, session=session)
    department_hard_skills: List[DepartmentsSkill] = []
    department_soft_skills: List[DepartmentsSkill] = []
    
    logger.info('Is instance of dict: ', isinstance(department_skills, dict))
    if isinstance(department_skills, dict):
        department_hard_skills = [DepartmentsSkill(**skill) for skill in department_skills['hard_skills']]
        department_soft_skills = [DepartmentsSkill(**skill) for skill in department_skills['soft_skills']]
        logger.info('Hard and soft skills uploaded. Length (hard, soft): ', len(department_hard_skills), len(department_soft_skills))
    
    
    soft_skills_ids = [skill.soft_skill_id for skill in employee_soft_skills]
    hard_skills_ids = [skill.hard_skill_id for skill in employee_hard_skills]
    
    soft_skills = get_soft_skills_by_ids(soft_skills_ids, session)
    hard_skills = get_hard_skills_by_ids(hard_skills_ids, session)
    
    weight = 0
    
    soft_weight = get_soft_skills_weight(employee_soft_skills, soft_skills, department_soft_skills)
    hard_weight = get_hard_skills_weight(employee_hard_skills, hard_skills, department_hard_skills)
    
    weight = soft_weight + hard_weight
    return weight / 100


def get_skills_weight(
    employee_id: int,
    session: Session,
    employee_skill_model: EmployeeSoftSkillsModel | EmployeeHardSkillsModel
):
    employee_data: EmployeeModel = session.query(EmployeeModel).get(employee_id)
    department_id = employee_data.department_id
    department_skills = get_department_skills(department_id=department_id, session=session)
    department_hard_skills: List[DepartmentsSkill] = []
    department_soft_skills: List[DepartmentsSkill] = []
    
    
    if employee_skill_model == EmployeeSoftSkillsModel:
        employee_soft_skills = get_user_soft_skills(employee_id=employee_id, session=session)
        if len(employee_soft_skills) == 0:
            return 0
        
        if isinstance(department_skills, dict):
            department_soft_skills = [DepartmentsSkill(**skill) for skill in department_skills['soft_skills']]
            logger.info('Hard and soft skills uploaded. Length (hard, soft): ', len(department_hard_skills), len(department_soft_skills))
        
        soft_skills_ids = [skill.soft_skill_id for skill in employee_soft_skills]
        soft_skills = get_soft_skills_by_ids(soft_skills_ids, session)
    
        return get_soft_skills_weight(employee_soft_skills, soft_skills, department_soft_skills)
        
    
        
    if employee_skill_model == EmployeeHardSkillsModel:
        employee_hard_skills = get_user_hard_skills(employee_id=employee_id, session=session)
        if len(employee_hard_skills) == 0:
            return 0
        if isinstance(department_skills, dict):
            department_hard_skills = [DepartmentsSkill(**skill) for skill in department_skills['hard_skills']]
            logger.info('Hard and soft skills uploaded. Length (hard, soft): ', len(department_hard_skills), len(department_soft_skills))
        hard_skills_ids = [skill.hard_skill_id for skill in employee_hard_skills]
        hard_skills = get_hard_skills_by_ids(hard_skills_ids, session)
        return get_hard_skills_weight(employee_hard_skills, hard_skills, department_hard_skills)
    
    
    

def get_soft_skills_weight(
    employee_soft_skills: List[EmployeeSoftSkillsModel], 
    soft_skills: List[SoftSkillsModel],
    department_soft_skills: List[DepartmentsSkill]):
    soft_weight = 1
    soft_total_weight = len(soft_skills) * 10
    for employee_skill, skill, dep_skills in zip(employee_soft_skills, soft_skills, department_soft_skills):
        soft_weight += _calculate_skill_weight(skill.weight, employee_skill.domain, dep_skills.skill_priority)
    
    return soft_weight / soft_total_weight


    

def get_hard_skills_weight(
    employee_hard_skills: List[EmployeeHardSkillsModel], 
    hard_skills: List[HardSkillsModel],
    department_hard_skills: List[DepartmentsSkill]):
    hard_weight = 1
    hard_total_weight = len(hard_skills) * 10
    for employee_skill, skill, dep_skills in zip(employee_hard_skills, hard_skills, department_hard_skills):
        hard_weight += _calculate_skill_weight(skill.weight, employee_skill.domain, dep_skills.skill_priority)
    
    return hard_weight / hard_total_weight

def _calculate_skill_weight(weight: int, domain: int, skill_priority: float) -> float:
    return weight * domain * skill_priority

### Post employee Skills 

def post_user_soft_skills(
    employee_id: int, 
    soft_skill: EmployeeAbility,
    session: Session
) -> dict[str, any]:
    
    skills = get_user_soft_skills(employee_id=employee_id, session=session)
    
    soft_skill_db = EmployeeSoftSkillsModel()
    soft_skill_db.employee_id = employee_id
    soft_skill_db.domain = soft_skill.domain
    soft_skill_db.soft_skill_id = soft_skill.id
    
    session.add(soft_skill_db)
    session.commit()
    
    return {
        'response:': "Skills uploaded"
    }
    
def update_user_soft_skills(
    employee_id: int,
    skills_id: int,
    domain: int,
    session: Session):
        statement = session.query(EmployeeSoftSkillsModel).where(
            EmployeeSoftSkillsModel.employee_id == employee_id and
            EmployeeSoftSkillsModel.soft_skill_id == skills_id )
        result = session.execute(statement)
        skills_db = result.scalars().first()

        if skills_db:
            skills_db.id = id
            skills_db.name = skills_id
            skills_db.domain = domain

            session.commit()
            session.refresh(skills_db)
        else:
            raise HTTPException(status_code=404, detail=f"Soft Skill with id {id} not found")
        return skills_db
    
def delete_user_soft_skills(ids: List[int], session: Session):
    statement = session.query(EmployeeSoftSkillsModel).filter(EmployeeSoftSkillsModel.soft_skill_id.in_(ids))
    result = session.execute(statement)
    skills_db = result.scalars().all()
    session.delete_all(skills_db)
    session.commit()
    
### User hard skills

def post_user_hard_skills(
    employee_id: int, 
    hard_skill: EmployeeAbility,
    session: Session
) -> dict[str, any]:
    skills = get_user_hard_skills(employee_id=employee_id, session=session)
    
    hard_skill_db = EmployeeHardSkillsModel()
    hard_skill_db.employee_id = employee_id
    hard_skill_db.domain = hard_skill.domain
    hard_skill_db.hard_skill_id = hard_skill.id
    
    session.add(hard_skill_db)
    session.commit()
    
    return {
        'response:': "Skills uploaded"
    }
    
def update_user_hard_skills(
    employee_id: int,
    skills_id: int,
    domain: int,
    session: Session):
        statement = session.query(EmployeeHardSkillsModel).where(
            EmployeeHardSkillsModel.employee_id == employee_id and
            EmployeeHardSkillsModel.hard_skill_id == skills_id )
        result = session.execute(statement)
        skills_db = result.scalars().first()

        if skills_db:
            skills_db.id = id
            skills_db.name = skills_id
            skills_db.domain = domain

            session.commit()
            session.refresh(skills_db)
        else:
            raise HTTPException(status_code=404, detail=f"Hard Skill with id {id} not found")
        return skills_db
    
def delete_user_hard_skills(ids: List[int], session: Session):
    statement = session.query(EmployeeHardSkillsModel).filter(EmployeeHardSkillsModel.hard_skill_id.in_(ids))
    result = session.execute(statement)
    skills_db = result.scalars().all()
    session.delete_all(skills_db)
    session.commit()