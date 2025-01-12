from sqlmodel import Field, SQLModel


class SkillTypeBase(SQLModel):
    type: str

class SkillBase(SkillTypeBase):
    name: str
    weight: float
    
    
class SkillTable(SkillBase, table=True):
    __tablename__ = "skills"    
    id: int = Field(default=None, primary_key=True, index=True, unique=True)

