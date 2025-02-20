from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    is_subscribed = Column(Boolean, default=True)
    zodiac_sign = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"{self.full_name}"
