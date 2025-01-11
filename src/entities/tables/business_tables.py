from sqlalchemy import Column, ForeignKey, Integer, String, Float
from core.database.database import Base


class DepartmentModel(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(60), nullable=False)
    location = Column(String(100), nullable=False)
    
class PositionModel(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(60), nullable=False)


class DepartmentsSoftSkillsModel(Base):
    __tablename__ = 'departments_soft_skills'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('soft_skills.id'), nullable=False)
    skill_priority = Column(Float, nullable=False)
    skill_segment = Column(Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'department_id': self.department_id,
            'skill_id': self.skill_id,
            'skill_priority': self.skill_priority,
            'skill_segment': self.skill_segment
        }
    
class DepartmentsHardSkillsModel(Base):
    __tablename__ = 'departments_hard_skills'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('hard_skills.id'), nullable=False)
    skill_priority = Column(Float, nullable=False)
    skill_segment = Column(Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'department_id': self.department_id,
            'skill_id': self.skill_id,
            'skill_priority': self.skill_priority,
            'skill_segment': self.skill_segment
        }