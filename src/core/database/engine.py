from sqlmodel import create_engine

sqlite_file_name = "employeesdbv2.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True)