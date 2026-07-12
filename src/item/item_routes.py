from fastapi import APIRouter, Depends, Query
from src.models import User
from src.database import get_session
from src.auth.jwt import verify_access_token
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.order.schemes import NewOrderSchema
from src.models import Item
from src.item.schemes import PaginationSchema
from src.database import SessionDep
from src.utils.schemes import PaginationDep

item_router = APIRouter(prefix="/item", tags=["Items"])

@item_router.get("/all")
async def items(session: SessionDep, data: PaginationDep, only_active: bool = False, authUser: User = Depends(verify_access_token)):

  page = data.page;
  per_page = data.per_page;

  offset_value = (page - 1) * per_page;

  items = session.query(Item)
  if only_active == True:
    items = items.filter(Item.is_active == True);
  items = items.limit(per_page).offset(offset_value).all();

  return {"items": items, "pagination": { "page": page, "per_page": per_page }}
