from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from entities.tables.business_tables import DepartmentModel, PositionModel
from entities.business import Department, Position

## Department

def create_department(
    department: Department, 
    session: Session) -> dict[str, any]:
    department.name = department.name.strip()
    department.location = department.location.strip()
    
    department_data = department.model_dump()
    department_db = DepartmentModel(**department_data)
    
    session.add(department_db)
    session.commit()
    session.refresh(department_db)
    
    return department_data
    

def get_departments(session: Session) -> List[DepartmentModel]:
    departments = session.query(DepartmentModel).all()
    return departments

def update_department(id: int, name: str, location: str, session: Session):
    department_db = session.query(DepartmentModel).get(id)
    
    if department_db:
        # department_db.id = id
        department_db.name = name.strip()
        department_db.location = location.strip()
        
        session.commit()
        session.refresh(department_db)
    else:
        raise HTTPException(status_code=404, detail=f"Department with id {id} not found")
    return None

def delete_department(id: int, session: Session):
    department_db = session.query(DepartmentModel).get(id)
    
    if department_db:
        session.delete(department_db)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Department with id {id} not found")
    return None

##Positon

def create_position(
    position: Position,
    session: Session) -> dict[str, any]:
    position_db = PositionModel()
    position_db.name = position.name.strip()
    
    session.add(position_db)
    session.commit()
    session.refresh(position_db)
    

def get_positions(session: Session):
    positions = session.query(PositionModel).all()
    return positions

def update_position(id: int, name: str, session: Session):
    position_db = session.query(PositionModel).get(id)
    
    if position_db:
        position_db.id = id
        position_db.name = name
        
        session.commit()
        session.refresh(position_db)
    else: 
        raise HTTPException(status_code=404, detail=f"Department with id {id} not found")
    return position_db

        

def delete_position(id: int, session: Session):
    position_db = session.query(PositionModel).get(id)
    
    if position_db:
        session.delete(position_db)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Department with id {id} not found")
    return None
    