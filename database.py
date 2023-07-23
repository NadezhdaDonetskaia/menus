import asyncpg
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os
load_dotenv()


db_url = os.getenv("DATABASE_URL")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


class BaseDBModel(DeclarativeBase):
    pass


def _connection_init(conn):
    return conn


_pool = None


async def connect():
    global _pool

    if not _pool:
        _pool = await asyncpg.create_pool(
            init=_connection_init,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            )
    return _pool
