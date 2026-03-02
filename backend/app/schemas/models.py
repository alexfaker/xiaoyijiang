"""请求与响应模型"""
from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """图片上传成功响应"""
    url: str = Field(..., description="图片公网 URL（oss:// 或 https://）")


class CreateTryonRequest(BaseModel):
    """创建试衣任务请求"""
    person_image_url: str = Field(..., description="模特图 URL")
    garment_image_url: str = Field(..., description="服饰图 URL")


class CreateTryonResponse(BaseModel):
    """创建试衣任务响应"""
    task_id: str = Field(..., description="任务 ID")


class TryonResultResponse(BaseModel):
    """试衣结果查询响应"""
    status: str = Field(..., description="任务状态：PENDING/RUNNING/SUCCEEDED/FAILED")
    result_image_url: str | None = Field(None, description="结果图 URL（仅 SUCCEEDED 时有值）")
    message: str | None = Field(None, description="失败时错误信息")
