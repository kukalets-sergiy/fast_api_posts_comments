from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy.pool import NullPool
from app.config import (
    DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER,
    DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_USER_TEST)


def get_database_url(testing: bool = False) -> str:
    if testing:
        return f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


SQLALCHEMY_DATABASE_URL = get_database_url()
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
metadata = MetaData()


async def get_async_session(testing: bool = False) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
