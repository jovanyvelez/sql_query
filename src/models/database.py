
import os
from dotenv import load_dotenv

from sqlmodel import create_engine, Session

from typing import Generator

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL, echo=True)

class Database:
    def __init__(self, engine):
        self.engine = engine

    # Para uso con FastAPI Depends
    def get_session(self) -> Generator[Session, None, None]:
        session = Session(self.engine)
        try:
            yield session
        finally:
            print("Closing session")
            session.close()


db = Database(engine)
