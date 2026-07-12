from fastapi import FastAPI
from src.auth.auth_routes import auth_router
from src.order.order_routes import order_router
from src.item.item_routes import item_router
from dotenv import load_dotenv
load_dotenv()
from src.config import settings

app = FastAPI();

@app.get("/")
async def root():
  return {"message": "OK"}

app.include_router(auth_router);
app.include_router(order_router);
app.include_router(item_router);

