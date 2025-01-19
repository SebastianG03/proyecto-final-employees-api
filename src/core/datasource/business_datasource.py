from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select

from domain.factory.business.business_factory import BusinessFactory
from domain.entities.business.types.business_components import BusinessComponents
from domain.entities.business.department.department import DepartmentTable, DepartmentBase
from domain.entities.business.position.position import PositionTable, BusinessBase
from domain.entities.types.request_types import RequestTypes

businessFactory = BusinessFactory()

## Department

def create_department(
    department: DepartmentBase, 
    session: Session) -> dict[str, any]:
    department_db: DepartmentTable = businessFactory.create(
        request_type=RequestTypes.TABLE_REQUESTS,
        type=BusinessComponents.DEPARTMENT,
        base_content=department
        )
    
    session.add(department_db)
    session.commit()
    session.refresh(department_db)
    
    return department_db
    

def get_departments(session: Session) -> List[DepartmentTable]:
    departments = session.exec(select(DepartmentTable)).all()
    return departments

def update_department(id: int, name: str, location: str, session: Session):
    department_db: DepartmentTable = session.get(DepartmentTable, id)
    if department_db:
        department_db.sqlmodel_update(DepartmentBase.model_dump(exclude_unset=True))
        
        session.add(department_db)
        session.commit()
        session.refresh(department_db)
        return department_db
    else:
        raise HTTPException(status_code=404, detail=f"Department with id {id} not found")
    return None

def delete_department(id: int, session: Session):
    department_db = session.get(DepartmentTable, id)
    
    if department_db:
        session.delete(department_db)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Department with id {id} not found")
    return None

##Positon

def create_position(
    position: PositionTable,
    session: Session) -> dict[str, any]:
    position_db = businessFactory.create(
        type=BusinessComponents.POSITION,
        request_type=RequestTypes.TABLE_REQUESTS,
        base_content=position
    )
    
    session.add(position_db)
    session.commit()
    session.refresh(position_db)
    

def get_positions(session: Session):
    positions = session.exec(select(PositionTable)).all()
    return positions

def update_position(id: int, name: str, session: Session):
    position_db = session.get(PositionTable, id)
    
    if position_db:
        position_db.sqlmodel_update(PositionTable.model_dump(exclude_unset=True))
        
        session.commit()
        session.refresh(position_db)
    else: 
        raise HTTPException(status_code=404, detail=f"Department with id {id} not found")
    return position_db

        

def delete_position(id: int, session: Session):
    position_db = session.get(PositionTable, id)
    
    if position_db:
        session.delete(position_db)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Department with id {id} not found")
    return None
    