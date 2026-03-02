"""百炼临时存储上传服务"""
import tempfile
import uuid
from pathlib import Path

import httpx

from app.config import get_config


def _validate_file(size: int, ext: str) -> None:
    """校验文件大小和格式"""
    cfg = get_config()
    min_b = cfg["upload_min_size_kb"] * 1024
    max_b = cfg["upload_max_size_mb"] * 1024 * 1024
    if size < min_b or size > max_b:
        raise ValueError(f"图片大小需在 {cfg['upload_min_size_kb']}KB～{cfg['upload_max_size_mb']}MB 之间")
    if ext.lower() not in cfg["upload_allowed_extensions"]:
        raise ValueError(f"支持的格式：{', '.join(cfg['upload_allowed_extensions'])}")


def get_upload_policy(api_key: str, model_name: str) -> dict:
    """获取百炼文件上传凭证"""
    url = "https://dashscope.aliyuncs.com/api/v1/uploads"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    params = {"action": "getPolicy", "model": model_name}
    with httpx.Client() as client:
        resp = client.get(url, headers=headers, params=params)
        resp.raise_for_status()
    data = resp.json()
    if "data" not in data:
        raise RuntimeError(f"获取上传凭证失败：{data}")
    return data["data"]


def upload_to_oss(policy_data: dict, file_path: str) -> str:
    """将文件上传到百炼临时 OSS，返回 oss:// URL"""
    path = Path(file_path)
    file_name = path.name
    upload_dir = policy_data.get("upload_dir", "")
    unique_name = f"{uuid.uuid4().hex}_{file_name}"
    key = f"{upload_dir}/{unique_name}"

    data = {
        "OSSAccessKeyId": policy_data["oss_access_key_id"],
        "Signature": policy_data["signature"],
        "policy": policy_data["policy"],
        "x-oss-object-acl": policy_data.get("x_oss_object_acl", ""),
        "x-oss-forbid-overwrite": policy_data.get("x_oss_forbid_overwrite", ""),
        "key": key,
        "success_action_status": "200",
    }

    with open(file_path, "rb") as f:
        files = {"file": (file_name, f)}
        with httpx.Client() as client:
            resp = client.post(
                policy_data["upload_host"],
                data=data,
                files=files,
            )
            resp.raise_for_status()

    return f"oss://{key}"


async def upload_file_from_upload(upload_file) -> str:
    """
    从小程序上传的 UploadFile 上传到百炼临时存储，返回 oss:// URL。
    """
    cfg = get_config()
    api_key = cfg["api_key"]
    if not api_key:
        raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")

    ext = Path(upload_file.filename or "image.jpg").suffix
    content = await upload_file.read()
    size = len(content)
    _validate_file(size, ext)

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        policy_data = get_upload_policy(api_key, cfg["bailian_model"])
        oss_url = upload_to_oss(policy_data, tmp_path)
        return oss_url
    finally:
        Path(tmp_path).unlink(missing_ok=True)
