from sqlmodel import Field, SQLModel
from domain.entities.skills.types.skills_categories import SkillsCategories

class SkillCategoryBase(SQLModel):
    category: SkillsCategories

class SkillBase(SkillCategoryBase):
    name: str
    weight: float
    
    
class SkillTable(SkillBase, table=True):
    SQLModel.__tablename__ = "skills"    
    id: int = Field(default=None, primary_key=True, index=True, unique=True)

