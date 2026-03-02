"""FastAPI 应用入口"""
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import tryon, upload

app = FastAPI(
    title="换衣小程序后端",
    description="AI 虚拟试衣 API，支持模特图+服饰图合成",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 小程序需配置为实际域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(tryon.router)


@app.get("/")
async def root():
    return {"service": "换衣小程序后端", "docs": "/docs"}
