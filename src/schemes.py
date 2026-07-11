from pydantic import BaseModel, ConfigDict

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