"""应用配置"""
import os
from functools import lru_cache


@lru_cache
def get_config():
    """获取配置（缓存）"""
    api_key = os.getenv("DASHSCOPE_API_KEY", "")
    return {
        "api_key": api_key,
        "upload_max_size_mb": 5,
        "upload_min_size_kb": 5,
        "upload_allowed_extensions": {".jpg", ".jpeg", ".png", ".bmp", ".heic"},
        "bailian_model": "aitryon",
        "bailian_upload_api": "https://dashscope.aliyuncs.com/api/v1/uploads",
        "bailian_task_api": "https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis",
        "bailian_result_api": "https://dashscope.aliyuncs.com/api/v1/tasks",
    }
