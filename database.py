from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from config import db_url


def get_db_url():
    return db_url


async_engine = create_async_engine(
    get_db_url(),
    echo=True,
)

async_session = async_sessionmaker(async_engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)


class BaseDBModel(AsyncAttrs, DeclarativeBase):
    pass


metadata = BaseDBModel.metadata


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
