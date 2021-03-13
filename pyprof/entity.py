from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DB_URL = "postgres+psycopg2://postgres:postgres@localhost/pyprof"

Base = declarative_base()

engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)


class Frame(Base):
    __tablename__ = "frames"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    blocks = relationship("Block", cascade="all, delete, delete-orphan")

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Frame(name={self.name})>"


class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    frame_id = Column(Integer, ForeignKey("frames.id"))
    name = Column(String(32))

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Block(name={self.name})>"
