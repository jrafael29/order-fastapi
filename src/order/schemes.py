from pydantic import BaseModel, ConfigDict
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/signin-form")

class NewOrderSchema(BaseModel):
  user_id: int
  item_list: list[int]

  model_config = ConfigDict(
    from_attributes=True
  )
