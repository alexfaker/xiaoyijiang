# 换衣小程序后端

基于 FastAPI 的 AI 虚拟试衣后端，对接阿里云百炼 OutfitAnyone API。

## 后端服务启动流程

### 1. 创建虚拟环境（首次使用）

```bash
cd backend
python3 -m venv .venv
```

### 2. 激活虚拟环境并安装依赖

```bash
# 激活（macOS / Linux）
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

Windows 用户使用：`.venv\Scripts\activate`

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 DASHSCOPE_API_KEY（阿里云百炼，中国内地北京地域）
```

### 4. 启动服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 验证

- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/

---

## 一键启动（已创建虚拟环境时）

```bash
cd backend
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/upload/image` | POST | 上传图片，返回 oss:// URL |
| `/api/tryon/create` | POST | 创建试衣任务 |
| `/api/tryon/result` | GET | 查询任务结果 |
