from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Address(Base):
    ''' db schema '''
    __tablename__ = 'addresses'
    id:  Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    postcode: Mapped[int] = Column(Integer(), nullable=False)
    street: Mapped[str] = Column(String(255), nullable=False)
    street_number: Mapped[int] = Column(Integer(), nullable=False)
    city: Mapped[str] = Column(String(30), nullable=False)
