from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.models import User
from src.database import get_session
from src.auth.schemes import SignupSchema, SigninSchema, RefreshTokenSchema
from src.auth.crypto import bcrypt_context
from src.utils.validator import email_validator, string_length_validator
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from enum import Enum
from src.auth.schemes import oauth2_schema
from os import getenv

class JWTType(Enum):
  ACCESS = "access"
  REFRESH = "refresh"

## TODO: mudar de lugar
def generate_jwt(
    user: User, 
    expiration: timedelta = timedelta(minutes=int(getenv("JWT_EXPIRE_MINUTES", "15"))), 
    type: JWTType = JWTType.ACCESS
) -> str:
  expiration = datetime.now(timezone.utc) + expiration;
  print(f"expiration {expiration}")
  jwt_info = {"sub": str(user.id), "type": type.value, "exp": expiration};
  generated_jwt = jwt.encode(jwt_info, getenv("JWT_SECRET_KEY"), getenv("JWT_ALGORITHM"));
  return generated_jwt;

def refresh_access_token(data: RefreshTokenSchema, session = Depends(get_session)):
# def refresh_access_token(data = Depends(oauth2_schema), session = Depends(get_session)) -> str:
  refresh_token = data.refresh_token
  print("Refresh Token", refresh_token);

  try:
    token_result = jwt.decode(token=refresh_token, key=getenv("JWT_SECRET_KEY"));
    print("token result: ", token_result);
    if not token_result.get("type") == JWTType.REFRESH.value:
      raise HTTPException(status_code=401,detail="Only refresh tokens are accepted")

    user_id = token_result.get("sub");
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
      raise HTTPException(status_code=401,detail="User not found")

    new_access_token = generate_jwt(user=user)
    
    return new_access_token
  except ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token signature has expired")
  except JWTError as err:
    raise HTTPException(status_code=401, detail="Invalid token");

def verify_access_token(token = Depends(oauth2_schema), session = Depends(get_session)) -> User:
  print(f"token {token}")
  try:
    token_result = jwt.decode(token=token, key=getenv("JWT_SECRET_KEY"));
    print("token result: ", token_result);
    if not token_result.get("type") == JWTType.ACCESS.value:
      raise HTTPException(status_code=401,detail="Only refresh tokens are accepted")

    user_id = token_result.get("sub");
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
      raise HTTPException(status_code=401,detail="User not found")
    
    return user
  except ExpiredSignatureError as err:
    print(f"error: {err}")
    raise HTTPException(status_code=401, detail="Token signature has expired")
  except JWTError as err:
    raise HTTPException(status_code=401, detail="Invalid token");
