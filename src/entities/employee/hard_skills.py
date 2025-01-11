from .ablilities import Ability


class HardSkills(Ability):
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True