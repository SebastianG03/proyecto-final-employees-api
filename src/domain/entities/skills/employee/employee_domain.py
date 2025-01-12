from sqlmodel import SQLModel


class DomainBase(SQLModel):
    domain: int
