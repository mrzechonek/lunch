from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

DATABASE = "sqlite:///lunch.sqlite"

Base = declarative_base()


class Feed(Base):
    __tablename__ = "feed"

    url = Column(String, primary_key=True)
