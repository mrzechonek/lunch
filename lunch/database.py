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


async def connect():
    async with factory() as session, session.begin():
        yield session


DB = Depends(connect)
