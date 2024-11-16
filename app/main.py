from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import router
from app.api.v1.notion import router as notion_router
from app.api.v1.tweets import router as tweets_router
app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.8.135:3000","https://read-notion-help-docs.onrender.com"],  # 允许的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

app.include_router(router) 
app.include_router(notion_router)
app.include_router(tweets_router)