from pydantic import BaseModel
from .ablilities import Ability


class SoftSkills(Ability):
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True