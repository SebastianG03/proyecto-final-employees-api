from typing import Optional
from pydantic import BaseModel, Field


class Department(BaseModel):
    # id: str
    name: str = Field(
        min_length=3,
        max_length=55,
        alias="Name",
        pattern="^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ'’-]+(?: [a-zA-ZáéíóúÁÉÍÓÚñÑüÜ'’-]+)*$",
        title="Name",
        description="The name has to be a valid department name",
    )
    location: str = Field(
        min_length=3,
        max_length=95,
        alias="Location",
        title="Location",
        description="The location has to be a valid location",
    )
    
    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        populate_by_name = True
        

class DepartmentsSkill(BaseModel):
    
    department_id: Optional[int]
    skill_id: int
    skill_priority: float = Field(
        default=0.1,
        gt=0,
        le=1.0,
        description="Priority of the skill in the department (Must be between 0 - 1)"
    )
    skill_segment: float = Field(
        default=0.1,
        gt=0,
        lt=1,
        description="Recomended proportion of the employees with that skill in the department (Must be between 0 - 1)"
    ) 
    
    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        populate_by_name = True
    
    