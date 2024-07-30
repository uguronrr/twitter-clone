from sqlmodel import SQLModel, create_engine, Session
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

conn_str = f"sqlite:///{BASE_DIR}/twiterdb.db"
engine = create_engine(conn_str, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session