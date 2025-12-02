from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base


engine = create_engine("sqlite:///logs.db", echo=True)
Base = declarative_base()


class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime(timezone=True))
    humidty = Column(Integer)
    temperature = Column(Integer)
    moisture = Column(Integer)
    watered_seconds = Column(Integer)
