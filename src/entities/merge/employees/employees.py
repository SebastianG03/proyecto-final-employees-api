from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel


class EmployeeBase(SQLModel):
    name: str
    password: str
    email: EmailStr
    phone: Optional[str]
    address: str
    # deparment_id: int
    # position_id: int
    salary: float
    performance: float
    projects_completed: float
    projects_cancelled: float
    projects_rejected: float
    pair_raiting: float
    team_raiting: float
    inmediate_boss_raiting: float
    