from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Annotated
from fastapi import Depends

db = create_engine("sqlite:///database.db")

SessionLocal = sessionmaker(bind=db);

def get_session():
  db = SessionLocal();
  try:
    yield db;
  finally:
    # print("sessão fechada")
    db.close();

SessionDep = Annotated[Session, Depends(get_session)]