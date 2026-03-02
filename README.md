# 换衣小程序

AI 虚拟试衣小程序，支持微信、抖音双端发布。面向电商推广场景，降低营销成本。

## 项目结构

```
├── backend/        # FastAPI 后端（图片上传、百炼试衣 API）
├── miniprogram/    # uni-app 小程序
└── docs/           # 技术方案与实施计划
```

## 快速启动

### 后端

```bash
cd backend
cp .env.example .env   # 编辑并设置 DASHSCOPE_API_KEY
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 文档：http://localhost:8000/docs

### 小程序

1. 使用 **HBuilderX**：导入 `miniprogram` 目录，或先通过 `npx degit dcloudio/uni-preset-vue#vite tryon-tmp` 创建项目后，将本文 `miniprogram/` 内页面、组件、api 等覆盖进去
2. 在 `manifest.json` 中填写微信、抖音的 appid
3. 将 `miniprogram/api/index.js` 中 `BASE_URL` 改为实际后端地址（开发时可用内网穿透暴露 8000 端口）

## 依赖

- 阿里云百炼 API Key（中国内地北京地域）
- 微信/抖音小程序开发者账号
