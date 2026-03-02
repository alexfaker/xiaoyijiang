# 换衣小程序后端 Docker 镜像
# 构建: docker build -t xiaoyijiang-backend .
# 运行: docker run -p 8000:8000 -e DASHSCOPE_API_KEY=xxx xiaoyijiang-backend

FROM python:3.12-slim AS builder

WORKDIR /app

# 安装依赖到 /app/venv，以便最终阶段 appuser 可访问
COPY requirements.txt .
RUN pip install --no-cache-dir --target /app/venv -r requirements.txt

# 运行阶段：使用精简镜像
FROM python:3.12-slim

WORKDIR /app

# 从 builder 复制依赖到 /app/venv（非 root 目录）
COPY --from=builder /app/venv /app/venv
ENV PATH=/app/venv/bin:$PATH PYTHONPATH=/app/venv

# 复制应用代码
COPY app/ ./app/

# 非 root 用户运行
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# 生产模式运行 uvicorn（python -m 确保使用正确模块路径）
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
