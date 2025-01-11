from pydantic import BaseModel, Field


class Ability(BaseModel):
    name: str = Field()
    weight: int = Field(
        min = 1,
        max = 100,
        title = "weight",
        description = "Weight of the ability (1 - 100)"
    )
    
class EmployeeAbility(BaseModel):
    id: int
    domain: int = Field(
        min = 1,
        max = 10,
        title = "domain",
        description = "Domain of the ability (1-10)"
    )