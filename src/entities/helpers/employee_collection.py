from pydantic import BaseModel
from entities.tables.employee_tables import EmployeeModel

class EmployeeValue(BaseModel) :
    employee: EmployeeModel
    weight: float
    soft_weight: float = 0
    hard_weight: float = 0
    comment: str = ""
    
    
    def to_dict(self):
        employee_dict = self.employee.to_dict()
        employee_dict.pop("soft_skills")
        employee_dict.pop("hard_skills")
        return {
            "employee": employee_dict,
            "weight": self.weight,
            "soft_weight": self.soft_weight,
            "hard_weight": self.hard_weight,
            "comment": self.comment
        }
    
    class Config:
        from_attributes=True
        arbitrary_types_allowed=True
        populate_by_name = True
        
    
