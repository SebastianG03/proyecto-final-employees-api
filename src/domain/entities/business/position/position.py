from sqlmodel import Field
from domain.entities.business.business import BusinessBase

class PositionBase(BusinessBase):
    pass

class PositionTable(PositionBase):
    __tablename__ = "positions"
    id: int =  Field(default=None, primary_key=True, index=True, unique=True)