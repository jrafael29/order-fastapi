from sqlalchemy import create_engine, ForeignKey, func, Enum as SQLEnum
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase, relationship
from sqlalchemy.types import String, Boolean, DateTime, Integer
from enum import Enum
from datetime import datetime


class Base(DeclarativeBase):
  pass;


class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True);
  name: Mapped[str] = mapped_column(String(255), nullable=False);
  email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True);
  password: Mapped[str] = mapped_column(String(), nullable=False);
  is_active: Mapped[bool] = mapped_column(Boolean(), default=True);
  is_admin: Mapped[bool] = mapped_column(Boolean(), default=False);
  created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now());
  orders: Mapped[list["Order"]] = relationship(back_populates="user");

  def __init__(self, name, email, password, is_active=True, is_admin=False):
    self.name = name;
    self.email = email;
    self.password = password;
    self.is_active = is_active;
    self.is_admin = is_admin;

  def as_tuple(self):
    return (self.id, self.name, self.email, self.password, self.is_active, self.is_admin);

class OrderStatus(Enum):
  PENDING = "PENDING";
  COMPLETED = "COMPLETED";
  CANCELED = "CANCELED";

class Item(Base):
  __tablename__ = "items"

  id: Mapped[int] = mapped_column(primary_key=True);
  name: Mapped[str] = mapped_column(String(), nullable=False);
  description: Mapped[str] = mapped_column(String(), nullable=False);
  sku: Mapped[str] = mapped_column(String(), nullable=False);
  price: Mapped[int] = mapped_column(Integer(), nullable=False);
  is_active: Mapped[bool] = mapped_column(Boolean(), default=True);
  created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now());
  order_items: Mapped[list["OrderItem"]] = relationship(back_populates="item");
  
  def __init__(self, name: int, description: str, sku: str, price: int, is_active: bool = True):
    self.name = name;
    self.description = description;
    self.sku = sku;
    self.price = price;
    self.is_active = is_active;


class Order(Base):
  __tablename__ = "orders"

  id: Mapped[int] = mapped_column(primary_key=True);
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False);
  user: Mapped["User"] = relationship(back_populates="orders");
  status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), nullable=False);
  created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now());
  order_items: Mapped[list["OrderItem"]] = relationship(back_populates="order");

  def __init__(self, user_id: int, status: OrderStatus):
    self.user_id = user_id;
    self.status = status;

class OrderItem(Base):
  __tablename__ = "order_items"

  id: Mapped[int] = mapped_column(primary_key=True);
  order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False);
  order: Mapped["Order"] = relationship(back_populates="order_items");
  item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False);
  item: Mapped["Item"] = relationship(back_populates="order_items");
  quantity: Mapped[int] = mapped_column(Integer(), nullable=False);
  created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now());

  def __init__(self, order_id: int, item_id: int, quantity: int):
    self.order_id = order_id;
    self.item_id = item_id;
    self.quantity = quantity;