from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from core.database.database import Base
from entities.employee.workload import Workload


class EmployeeModel(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), nullable=False)
    email = Column(String(120), nullable=False)
    password = Column(String(50), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=False)
    workload = Column(String(60), nullable=True)
    salary = Column(Float, nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(120), nullable=True)
    soft_skills = relationship("SoftSkillsModel", secondary="employee_soft_skills")
    hard_skills = relationship("HardSkillsModel", secondary="employee_hard_skills")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department_id": self.department_id,
            "position_id": self.position_id,
            "workload": self.workload, 
            "salary": self.salary,
            "phone": self.phone,
            "address": self.address,
            "soft_skills": [skill.to_dict() for skill in self.soft_skills],
            "hard_skills": [skill.to_dict() for skill in self.hard_skills]
        }