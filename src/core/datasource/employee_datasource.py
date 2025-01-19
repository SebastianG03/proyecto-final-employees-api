from typing import List
from sqlmodel import Session, select


from core.services.logger_service import logger

from domain.factory.employee.employees_factory import EmployeesFactory

from domain.entities.employees.employees import EmployeePatch, EmployeeTable
from domain.entities.skills.employee.employee_skills import EmployeeSkillTable
from domain.entities.types.request_types import RequestTypes
from domain.entities.skills.types.skills_categories import SkillsCategories
from domain.entities.skills.skill.skills import SkillTable

from domain.collection.employee_skills_collection import EmployeeSkillsCollection, EmployeeSkillsCollector, EmployeeSkillModel

factory: EmployeesFactory = EmployeesFactory()


def get_employee(
    id: int,
    session: Session
    ) -> EmployeeTable:
    employee = session.get(EmployeeTable, id)
    return employee

def get_managers(session: Session) -> List[EmployeeTable]:
    employees = session.exec(select(EmployeeTable)
                            .where(EmployeeTable.leadsTeam == True)
                            .offset(0)
                            .limit(100)).all()
    return employees        

def get_all_employees(session: Session) -> List[EmployeeTable]: 
    employees = session.exec(select(EmployeeTable)
                 .offset(0)
                 .limit(100)).all()
    return employees

def create_employee(
        employee: EmployeePatch,
        session: Session
        ) -> EmployeeTable:
    employee_db: EmployeeTable = factory.create(
        requestType=RequestTypes.TABLE_REQUESTS,
        base_content=employee
        )
    session.add(employee_db)
    session.commit()
    session.refresh(employee_db)
    return employee_db
    

def update_employee(
    id: int, 
    employee: EmployeePatch, 
    session: Session
    ) -> EmployeeTable:
    employee_db: EmployeeTable = session.get(EmployeeTable, id)
    employee_db.sqlmodel_update(employee.model_dump(exclude_unset=True))
    
    session.add(employee_db)
    session.commit()
    session.refresh(employee_db)
    return employee_db


def delete_employee(id: int, session: Session):
    employee = session.get(EmployeeTable, id)
    session.delete(employee)
    session.commit()

### Sort employees methods


def get_employees_by_weight(
    session: Session,
    employees: List[EmployeeTable] = []) -> List[EmployeeSkillsCollector]:
    initial_collection = List[EmployeeSkillsCollector]()
    
    for employee in employees:
        employee_skills = session.exec(select(EmployeeSkillTable)
                              .where(EmployeeSkillTable.employee_id == employee.id)
                              ).all()
        skills_ids = [skill.skill_id for skill in employee_skills]
        skills = session.exec(select(SkillTable)
                              .where(SkillTable.id in skills_ids)
                              ).all()
        skills_model = [EmployeeSkillModel(skill_reference=skill, model_skill_reference=employee_skill) 
                        for skill, employee_skill in zip(skills, employee_skills)]
        initial_collection.append(EmployeeSkillsCollector(
            model_reference=employee, 
            model_skills=skills_model
            ))
    
    employees_collection = EmployeeSkillsCollection(initial_collection)
    employees_collection.calculate_total_weight()
    return employees_collection.sort_by_weight()

def get_employees_by_skill_type(session: Session, skill_type: SkillsCategories = SkillsCategories.SOFT):
    employees = get_all_employees(session)
    initial_collection = List[EmployeeSkillsCollector]()
    
    for employee in employees:
        employee_skills = session.exec(select(EmployeeSkillTable)
                              .where(EmployeeSkillTable.employee_id == employee.id)
                              ).all()
        skills_ids = [skill.skill_id for skill in employee_skills]
        skills = session.exec(select(SkillTable)
                              .where(SkillTable.id in skills_ids)
                              ).all()
        skills_model = [EmployeeSkillModel(skill_reference=skill, model_skill_reference=employee_skill) 
                        for skill, employee_skill in zip(skills, employee_skills)]
        initial_collection.append(EmployeeSkillsCollector(
            model_reference=employee, 
            model_skills=skills_model
            ))
    
    employees_collection = EmployeeSkillsCollection(initial_collection)
    employees_collection.calculate_weight(skill_type)
    if skill_type == SkillsCategories.SOFT:
        return sorted(employees_collection.collection, key=lambda x: x.skills_raiting.soft_weight, reverse=True)
    else:
        return sorted(employees_collection.collection, key=lambda x: x.skills_raiting.hard_weight, reverse=True)    
    return employees_collection
