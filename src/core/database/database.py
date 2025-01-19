from sqlmodel import SQLModel, Session

from src.core.database.engine import engine

def create_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
        

