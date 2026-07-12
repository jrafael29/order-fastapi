from fastapi import APIRouter, Depends
from src.models import User
from src.database import get_session
from src.auth.jwt import verify_access_token
from sqlalchemy.orm import Session
from src.order.schemes import NewOrderSchema

order_router = APIRouter(prefix="/order", tags=["Orders"])

@order_router.get("/")
async def orders(authUser: User = Depends(verify_access_token)):
  return {"orders": authUser.as_tuple()}


@order_router.post("/new-order")
async def new_order(data: NewOrderSchema, authUser: User = Depends(verify_access_token), session: Session = Depends(get_session)):
  return