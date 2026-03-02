"""试衣任务路由"""
from fastapi import APIRouter, HTTPException

from app.schemas.models import (
    CreateTryonRequest,
    CreateTryonResponse,
    TryonResultResponse,
)
from app.services.bailian import create_tryon_task, get_task_result

router = APIRouter(prefix="/api/tryon", tags=["tryon"])


@router.post("/create", response_model=CreateTryonResponse)
async def create_tryon(req: CreateTryonRequest):
    """创建试衣任务，返回 task_id"""
    try:
        task_id = create_tryon_task(
            person_image_url=req.person_image_url,
            garment_image_url=req.garment_image_url,
        )
        return CreateTryonResponse(task_id=task_id)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"创建任务失败：{str(e)}")


@router.get("/result", response_model=TryonResultResponse)
async def get_tryon_result(task_id: str):
    """查询试衣任务结果"""
    try:
        status, result_url, message = get_task_result(task_id)
        return TryonResultResponse(
            status=status,
            result_image_url=result_url,
            message=message,
        )
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"查询失败：{str(e)}")
