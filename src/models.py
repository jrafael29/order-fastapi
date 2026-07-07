from sqlalchemy import create_engine
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.types import String, Boolean

db = create_engine("sqlite:///database.db")

class Base(DeclarativeBase):
  pass;


class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(255), nullable=False)
  email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
  password: Mapped[str] = mapped_column(String(), nullable=False)
  is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
  is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)

  def __init__(self, name, email, password, is_active=True, is_admin=False):
    self.name = name;
    self.email = email;
    self.password = password;
    self.is_active = is_active;
    self.is_admin = is_admin;

  def as_tuple(self):
    return (self.id, self.name, self.email, self.password, self.is_active, self.is_admin);