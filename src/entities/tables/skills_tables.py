from sqlalchemy import Column, Integer, String
from core.database.database import Base

class SoftSkillsModel(Base):
    __tablename__ = 'soft_skills'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(60), nullable=False)
    weight = Column(Integer, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'weight': self.weight
        }
    
class HardSkillsModel(Base):
    __tablename__ = 'hard_skills'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(60), nullable=False)
    weight = Column(Integer, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'weight': self.weight
        }