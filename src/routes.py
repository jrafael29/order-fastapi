from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models import get_session, User
from src.schemes import SignupSchema, SigninSchema
from src.crypto import bcrypt_context
from src.validator import email_validator, string_length_validator
from datetime import datetime, timedelta
from jose import jwt, JWTError
from enum import Enum

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

order_router = APIRouter(prefix="/order", tags=["Orders"])


JWT_EXPIRE_MINUTES=1
JWT_SECRET_KEY="ifewifmsokmiodqwndi"
JWT_ALGORITHM="HS256"


class JWTType(Enum):
  ACCESS = "access"
  REFRESH = "refresh"

## TODO: mudar de lugar
def generate_jwt(
    user: User, 
    expiration: timedelta = timedelta(minutes=JWT_EXPIRE_MINUTES), 
    type: JWTType = JWTType.ACCESS
) -> str:
  expiration = datetime.now() + expiration;
  jwt_info = {"sub": user.id, "type": type.value, "exp": expiration};
  generated_jwt = jwt.encode(jwt_info, JWT_SECRET_KEY, JWT_ALGORITHM);
  return generated_jwt;

def verify_jwt(token):
  pass;
  


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


def dependente(tokeneas):
  pass;

@order_router.get("/")
async def orders(param = Depends(dependente)):
  return {"orders": []}
