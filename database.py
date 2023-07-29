
from contextlib import asynccontextmanager
from typing import Optional

import asyncpg
from sqlalchemy.orm import DeclarativeBase
from .config import DB_HOST, DB_NAME, DB_USER, DB_PORT, DB_PASSWORD


class BaseDBModel(DeclarativeBase):
    pass


async def _connection_init(conn):
    return conn


_pool: Optional[asyncpg.pool.Pool] = None


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
            min_size=1,
            max_size=4,
            )

    return _pool


async def close_conn():
    global _pool

    if not _pool:
        return
    await _pool.close()


@asynccontextmanager
async def get_connection():
    conn_pool = await connect()
    conn = await conn_pool.acquire()
    yield conn
    await conn_pool.release(conn)
