
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum, Column, Integer, Float
from typing import List
from enum import Enum as PyEnum
from .item_model import Item
from .database import Base

from .user_model import User
from .restaurant_model import Restaurant
from .address_model import Address
from .item_model import Item

class OrderStatusEnum(PyEnum):
    PENDING = 1
    ACCEPTED = 2
    IN_PROGRESS = 3
    READY = 4
    DELIVERY = 5
    COMPLETED = 6
    CANCELED = 7


class OrderStatus(Base):
    __tablename__ = 'order_status'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Enum(OrderStatusEnum))


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_status = mapped_column(ForeignKey(OrderStatus.id))
    items: Mapped[List['OrderItem']] = relationship()
    branch_id = mapped_column(ForeignKey(Restaurant.id), nullable=False)
    address_id = mapped_column(ForeignKey(Address.id), nullable=False)
    customer_id = mapped_column(ForeignKey(User.id), nullable=False)
    total_price = Column(Float())


class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_id = mapped_column(ForeignKey(Item.id), nullable=False)
    item_details: Mapped[Item] = relationship()
    order_id = mapped_column(ForeignKey(Order.id), nullable=False)
    quantity = Column(Integer(), nullable=False)
