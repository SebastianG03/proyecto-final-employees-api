from sqlmodel import Field, SQLModel


class SkillCategoryBase(SQLModel):
    category: str

class SkillBase(SkillCategoryBase):
    name: str
    weight: float
    
    
class SkillTable(SkillBase, table=True):
    __tablename__ = "skills"    
    id: int = Field(default=None, primary_key=True, index=True, unique=True)

