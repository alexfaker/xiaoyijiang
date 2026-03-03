"""图片代理：将百炼返回的图片（可能为 HTTP）通过本域名 HTTPS 转发，解决小程序 HTTPS 与 downloadFile 合法域名限制"""
import re
from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

router = APIRouter(prefix="/api/image", tags=["image"])

# 仅允许代理的阿里云 OSS/百炼 域名，防止滥用
ALLOWED_HOSTS = re.compile(r"^([a-z0-9-]+\.)*oss.*\.aliyuncs\.com$", re.IGNORECASE)


def _is_allowed_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        # 允许 http 和 https（百炼可能返回 http）
        if parsed.scheme not in ("http", "https"):
            return False
        return bool(ALLOWED_HOSTS.match(parsed.netloc))
    except Exception:
        return False


@router.get("/proxy")
async def proxy_image(url: str = Query(..., description="图片 URL，仅支持阿里云 OSS")):
    """代理转发图片，供小程序 image 组件和 downloadFile 使用。支持将 HTTP 转为 HTTPS 输出。"""
    if not _is_allowed_url(url):
        raise HTTPException(400, "仅支持阿里云 OSS 图片域名")

    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(502, f"拉取图片失败: {str(e)}")

    content = resp.content if isinstance(resp.content, bytes) else resp.read()
    content_type = resp.headers.get("content-type", "image/jpeg")
    return Response(content=content, media_type=content_type)
