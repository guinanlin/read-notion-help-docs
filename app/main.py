from fastapi import FastAPI
from app.api.v1.endpoints import router
from app.api.v1.notion import router as notion_router
from app.api.v1.tweets import router as tweets_router
app = FastAPI()

app.include_router(router) 
app.include_router(notion_router)
app.include_router(tweets_router)