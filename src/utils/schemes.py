from pydantic import BaseModel, ConfigDict, Field
from fastapi.security import OAuth2PasswordBearer
from fastapi import Query, Depends
from typing import Annotated

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/signin-form")

class PaginationParams(BaseModel):
  page: int = Field(Query(1, ge=1, description="Page number (starts at 1)"))
  per_page: int = Field(Query(10, ge=1, le=100, description="Items per page (max 100)"))

  model_config = ConfigDict(
    from_attributes=True
  )

  @property
  def offset(self) -> int:
      """Calculate SQL OFFSET value."""
      return (self.page - 1) * self.per_page


PaginationDep = Annotated[PaginationParams, Depends()]