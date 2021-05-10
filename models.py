from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Date,
    Float,
    BigInteger,
)

Base = declarative_base()


class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist_name = Column(String)
    year = Column(Integer)
    release = Column(String)
    ingestion_time = Column(DateTime)


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    original_title = Column(String)
    original_language = Column(String)
    budget = Column(Integer)
    is_adult = Column(Boolean)
    release_date = Column(Date)
    original_title_normalized = Column(String)


class App(Base):
    __tablename__ = "apps"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    genre = Column(String)
    rating = Column(Float)
    version = Column(String)
    size_bytes = Column(BigInteger)
    is_awesome = Column(Boolean)


class DataFile(Base):
    __tablename__ = "data_files"
    id = Column(Integer, primary_key=True)
    name = Column(String)
