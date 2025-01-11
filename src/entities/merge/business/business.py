from sqlmodel import SQLModel


class BusinessBase(SQLModel):
    name: str