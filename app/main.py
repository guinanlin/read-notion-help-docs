from fastapi import FastAPI
from app.api.v1.endpoints import router
from app.api.v1.notion import router as notion_router
app = FastAPI()

app.include_router(router) 
app.include_router(notion_router)