from fastapi import FastAPI
from src.routes import order_router, auth_router

app = FastAPI();

@app.get("/")
async def root():
  return {"message": "OK"}

app.include_router(auth_router);
app.include_router(order_router);