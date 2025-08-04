# models.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Date, Time, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, time

# Database setup
DATABASE_URL = "sqlite:///events.db"
engine = create_engine(DATABASE_URL, echo=False)  # Set echo=True for debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Event Model
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String(1500))
    start_date = Column(Date)
    end_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    venue = Column(String(150))
    location = Column(String(200))
    booking_url = Column(String(500))
    ticket_price = Column(Float)
    category = Column(String(100))
    description = Column(Text)

    def __repr__(self):
        return f"<Event(name={self.name}, id={self.id})>"