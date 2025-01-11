from sqlmodel import Field
from src.entities.merge.business.business import BusinessBase

class PositionBase(BusinessBase):
    pass

class PositionTable(PositionBase):
    id: int =  Field(default=None, primary_key=True, index=True, unique=True)