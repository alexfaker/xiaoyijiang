"""图片上传路由"""
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.models import UploadResponse
from app.services.oss_upload import upload_file_from_upload

router = APIRouter(prefix="/api/upload", tags=["upload"])


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
