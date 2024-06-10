from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Item(Base):
    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(50), unique=True, nullable=False)
    price: Mapped[int] = Column(Float(), nullable=False)


class ItemOptionGroup(Base):
    __tablename__ = 'item_option_groups'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    item_id = mapped_column(ForeignKey(Item.id), nullable=False)
    multiple_choice = Column(Boolean(), nullable=False, default=False)


class ItemOption(Base):
    __tablename__ = 'item_options'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    item_option_group_id = mapped_column(
        ForeignKey(ItemOptionGroup.id), nullable=False)
    price = Column(Float(), nullable=False)
