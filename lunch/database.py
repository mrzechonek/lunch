from contextlib import asynccontextmanager
from contextvars import ContextVar

from fastapi import Depends
from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE = "sqlite:///lunch.sqlite"

Base = declarative_base()


class Feed(Base):
    __tablename__ = "feed"

    url = Column(String, primary_key=True)


class Topic(Base):
    __tablename__ = "topic"

    title = Column(String, primary_key=True)


engine = create_async_engine(DATABASE.replace("sqlite://", "sqlite+aiosqlite://"))

factory = sessionmaker(engine, class_=AsyncSession)

DB_SESSION = ContextVar("DB_SESSION", default=None)


class DBMeta(type):
    @property
    def session(self):
        return DB_SESSION.get()


class DB(metaclass=DBMeta):
    pass


@asynccontextmanager
async def db_session_context():
    async with factory() as session, session.begin():
        token = DB_SESSION.set(session)
        yield
        DB_SESSION.reset(token)
