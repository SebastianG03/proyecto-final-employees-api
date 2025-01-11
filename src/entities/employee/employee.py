from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from entities.employee.workload import Workload
from .hard_skills import HardSkills
from .soft_skills import SoftSkills
# from uuid import UUID
# import uuid

class Employee(BaseModel):
    name: str = Field(
        min_length=6, 
        max_length=20, 
        alias="Name", 
        pattern="^[a-zA-Z]+[a-zA-Z ]*$", 
        title="Name",
        description="The name has to be a valid employee name")
    password: str = Field(
        min_length=8,
        max_length=20,
        alias="Password",
        title="Password",
        description="The password has to be a valid password with uppercase, lowercase, number, and special characters (@$!%*?&)"
    )
    email: EmailStr
    phone: Optional[str] = Field(
        alias="Phone", 
        description="The phone has to be a valid phone number.",
        min_length=8,
        max_length=18,
        pattern="^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$"
    )
    address: str = Field(
        min_length=3, 
        max_length=100, 
        alias="Address", 
        title="Address",
        description="The address has to be a valid address."
    )
    department_id: int = Field(
        gt=0, 
        lt=100,
        alias="Department", 
        description="The department has to be a valid department.",
    )
    position_id: int = Field(
        gt=0, 
        lt=100,
        alias="Position", 
        description="The position has to be a valid position.",
    )
    workload: Optional[str] = Field(
        alias="Workload", 
        examples=["No work", "low", "medium", "high", "overwork"],
        description="Can be no work, low, medium, high or overwork.",
    )
    salary: Optional[float] = Field(
        gt=0, 
        lt=100000,
        alias="Salary", 
        description="The salary has to be a valid salary (xxxxxx.xx)",
    ) 
    
    class Config:
        from_attributes=True
        arbitrary_types_allowed=True
        populate_by_name = True
        
    
    
class EmployeeUpdate(BaseModel):
    id: int 
    name: str = Field(
        min_length=6, 
        max_length=20, 
        alias="Name", 
        pattern="^[a-zA-Z]+[a-zA-Z ]*$", 
        title="Name",
        description="The name has to be a valid employee name")
    password: str = Field(
        min_length=8,
        max_length=20,
        alias="Password",
        title="Password",
        description="The password has to be a valid password with uppercase, lowercase, number, and special characters (@$!%*?&)"
    )
    email: EmailStr
    phone: Optional[str] = Field(
        alias="Phone", 
        description="The phone has to be a valid phone number.",
        min_length=8,
        max_length=18,
        pattern="^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$"
    )
    address: str = Field(
        min_length=3, 
        max_length=100, 
        alias="Address", 
        title="Address",
        description="The address has to be a valid address."
    )
    department_id: int = Field(
        gt=0, 
        lt=100,
        alias="Department", 
        description="The department has to be a valid department.",
    )
    position_id: int = Field(
        gt=0, 
        lt=100,
        alias="Position", 
        description="The position has to be a valid position.",
    )
    workload: Optional[str] = Field(
        alias="Workload", 
        examples=["No work", "low", "medium", "high", "overwork"],
        description="Can be no work, low, medium, high or overwork.",
    )
    salary: Optional[float] = Field(
        gt=0, 
        lt=100000,
        alias="Salary", 
        description="The salary has to be a valid salary (xxxxxx.xx)",
    ) 
    
    class Config:
        from_attributes=True
        arbitrary_types_allowed=True
        populate_by_name = True