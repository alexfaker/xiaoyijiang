"""FastAPI 应用入口"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.routers import tryon, upload, image_proxy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequestLogMiddleware(BaseHTTPMiddleware):
    """对上传接口的 GET 请求打日志，便于排查 HTTP 重定向导致 POST 变 GET 的问题"""

    async def dispatch(self, request, call_next):
        if request.method == "GET" and "/api/upload" in request.url.path:
            logger.warning(
                "收到 GET 请求访问上传接口，正确应为 POST。"
                "可能原因：HTTP→HTTPS 重定向(301/302)导致方法被改为 GET，请使用 HTTPS 直连或配置 307/308 重定向。"
            )
        return await call_next(request)


app = FastAPI(
    title="换衣小程序后端",
    description="AI 虚拟试衣 API，支持模特图+服饰图合成",
    root_path=os.getenv("ROOT_PATH", ""),  # 在 Nginx /xiaoyijiang 下部署时设置 ROOT_PATH=/xiaoyijiang
)

app.add_middleware(RequestLogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 小程序需配置为实际域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(tryon.router)
app.include_router(image_proxy.router)


@app.get("/")
async def root():
    return {"service": "换衣小程序后端", "docs": "/docs"}
