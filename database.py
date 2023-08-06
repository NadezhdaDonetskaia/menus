from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import db_url


def get_db_url():
    return db_url


engine = create_engine(
    get_db_url(),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseDBModel = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
