from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class User(Base):
    '''represents the db schema for this entity'''
    __tablename__ = 'users'
    id:  Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email = Column(String(40),nullable=False, unique=True)
    first_name: Mapped[str] = Column(String(20), nullable=False) 
    last_name: Mapped[str] = Column(String(20), nullable=False)
    phone_number: Mapped[str] = Column(String(15), nullable=False, unique=True)
    password:  Mapped[str] = Column(String(255), nullable=False)
    created_at: Mapped[str] = Column(DateTime(), default=func.now())
