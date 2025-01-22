from sqlmodel import Field, SQLModel
from domain.entities.business.business import BusinessBase
from domain.helpers.common_metadata import schema_info, schema_name

class PositionBase(BusinessBase):
    pass

class PositionTable(PositionBase, table=True):
    SQLModel.__tablename__ = "positions"
    id: int =  Field(default=None, primary_key=True)