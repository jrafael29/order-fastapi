from pydantic import BaseModel, ConfigDict
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/signin-form")

class SignupSchema(BaseModel):
  name: str
  email: str
  password: str

  model_config = ConfigDict(
    from_attributes=True
  )


class SigninSchema(BaseModel):
  email: str
  password: str

  model_config = ConfigDict(
    from_attributes=True
  )

class RefreshTokenSchema(BaseModel):
  refresh_token: str