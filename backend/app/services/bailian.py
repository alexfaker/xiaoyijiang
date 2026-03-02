"""阿里云百炼 OutfitAnyone 试衣 API 封装"""
import httpx

from app.config import get_config


def _get_headers() -> dict:
    cfg = get_config()
    api_key = cfg["api_key"]
    if not api_key:
        raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
        "X-DashScope-OssResourceResolve": "enable",  # 支持 oss:// URL
    }


def create_tryon_task(person_image_url: str, garment_image_url: str) -> str:
    """
    创建试衣任务，返回 task_id。
    单件服饰统一传入 top_garment_url（上装/连衣裙）。
    """
    cfg = get_config()
    url = cfg["bailian_task_api"]

    body = {
        "model": cfg["bailian_model"],
        "input": {
            "person_image_url": person_image_url,
            "top_garment_url": garment_image_url,
        },
        "parameters": {
            "resolution": -1,
            "restore_face": True,
        },
    }

    with httpx.Client() as client:
        resp = client.post(url, headers=_get_headers(), json=body)
        resp.raise_for_status()
    data = resp.json()
    if "output" not in data or "task_id" not in data["output"]:
        raise RuntimeError(f"创建任务失败：{data}")
    return data["output"]["task_id"]


def get_task_result(task_id: str) -> tuple[str, str | None, str | None]:
    """
    查询任务结果。返回 (status, result_image_url, message)。
    status: PENDING | RUNNING | SUCCEEDED | FAILED
    """
    cfg = get_config()
    api_key = cfg["api_key"]
    if not api_key:
        raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")

    url = f"{cfg['bailian_result_api']}/{task_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    with httpx.Client() as client:
        resp = client.get(url, headers=headers)
        resp.raise_for_status()
    data = resp.json()

    output = data.get("output", {})
    status = output.get("task_status", "PENDING")
    result_url = None
    message = None

    if status == "SUCCEEDED":
        result_url = output.get("image_url")
    elif status == "FAILED":
        message = output.get("message", "任务失败")

    return (status, result_url, message)
