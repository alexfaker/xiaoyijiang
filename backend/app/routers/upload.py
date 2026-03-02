"""图片上传路由"""
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.models import UploadResponse
from app.services.oss_upload import upload_file_from_upload

router = APIRouter(prefix="/api/upload", tags=["upload"])


@router.get("/image")
def upload_image_get():
    """
    诊断用：上传接口仅支持 POST。若客户端收到此 JSON，说明请求被发成了 GET。
    可能原因：平台/运营商代理、或请求来自爬虫探针（非您的小程序）。
    """
    return {
        "diagnostic": "GET_not_allowed",
        "message": "上传需使用 POST + multipart/form-data，当前为 GET。uni.uploadFile 应发 POST，请检查客户端或网络路径。",
    }


@router.post("/image", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """上传图片至百炼临时存储，返回 oss:// URL"""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "请上传图片文件")

    try:
        url = await upload_file_from_upload(file)
        return UploadResponse(url=url)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"上传失败：{str(e)}")
