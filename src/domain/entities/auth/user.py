from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from domain.entities.employees.employees import EmployeeTable

class User(BaseModel):
    user_data: EmployeeTable
    is_admin: bool = False
    connection_time: datetime
    expire_time: datetime
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        
class LoginModel(BaseModel):
    email: EmailStr = Field(
        title= "Email",
        alias= "Email",
        description= "Write the employee email"
    )
    password: str = Field(
        min_length=8, 
        max_length=20, 
        alias="Password", 
        title="Password",
        description="Write a valid password between 8 and 20 characters"
        )
    
    class Config:
        from_attributes=True
        arbitrary_types_allowed=True