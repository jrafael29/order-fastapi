from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.models import User
from src.database import get_session
from src.auth.schemes import SignupSchema, SigninSchema
from src.auth.crypto import bcrypt_context
from src.utils.validator import email_validator, string_length_validator
from datetime import timedelta
from src.auth.schemes import oauth2_schema
from src.auth.jwt import refresh_access_token, generate_jwt, JWTType

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/signup")
async def register(data: SignupSchema, session: Session = Depends(get_session)):

  is_valid_email = email_validator(data.email);

  if not is_valid_email:
    raise HTTPException(status_code=400, detail="invalid email");

  if not string_length_validator(data.name, 255):
    raise HTTPException(status_code=400, detail="name must be lower than 255 characters");

  if not string_length_validator(data.email, 255):
    raise HTTPException(status_code=400, detail="email must be lower than 255 characters");
  
  if session.query(User).filter(User.email == data.email).first() is not None:
    raise HTTPException(status_code=400, detail="email already registered");
  
  password_crypt = bcrypt_context.hash(data.password);

  new_user = User(name=data.name, email=data.email, password=password_crypt);
  session.add(new_user);
  session.commit();
  return {"message": "user sucessfully created"};

@auth_router.post("/signin")
async def login(data: SigninSchema, session: Session = Depends(get_session)):

  user = session.query(User).filter(User.email == data.email).first();

  if user is None or not user:
    raise HTTPException(status_code=400, detail="invalid credentials or user no registered");

  password_match = bcrypt_context.verify(data.password, user.password);

  if not password_match:
    raise HTTPException(status_code=400, detail="invalid credentials or user no registered");

  print(f"usuario autenticado: {user.email}")
  jwt_access_token = generate_jwt(user);
  jwt_refresh_token = generate_jwt(user, expiration=timedelta(days=3), type=JWTType.REFRESH);
  return {
    "access_token": jwt_access_token,
    "refresh_token": jwt_refresh_token,
    "token_type": "Bearer"
  };

@auth_router.post("/signin-form")
async def login_form(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):

  print(data);

  user = session.query(User).filter(User.email == data.username).first();

  if user is None or not user:
    raise HTTPException(status_code=400, detail="invalid credentials or user no registered");
  password_match = bcrypt_context.verify(data.password, user.password);
  if not password_match:
    raise HTTPException(status_code=400, detail="invalid credentials or user no registered");

  print(f"usuario autenticado: {user.email}")
  jwt_access_token = generate_jwt(user);
  print(f"jwt_access_token: {jwt_access_token}")
  return {
    "access_token": jwt_access_token,
    "token_type": "Bearer"
  };

@auth_router.post("/refresh-token")
async def refresh_token(new_access_token = Depends(refresh_access_token)):
  return {
    "access_token": new_access_token,
    "token_type": "Bearer"
  }

