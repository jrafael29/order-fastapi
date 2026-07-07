from sqlalchemy import create_engine, ForeignKey, func, Enum as SQLEnum
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from sqlalchemy.types import String, Boolean, DateTime
from enum import Enum
from datetime import datetime

db = create_engine("sqlite:///database.db")

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

class Order(Base):
  __tablename__ = "orders"

  id: Mapped[int] = mapped_column(primary_key=True);
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False);
  user: Mapped["User"] = relationship(back_populates="orders");
  status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), nullable=False);
  created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now());

  def __init__(self, user_id: int, status: OrderStatus):
    self.user_id = user_id;
    self.status = status;