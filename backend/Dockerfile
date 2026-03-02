# 换衣小程序后端 Docker 镜像
# 构建: docker build -t xiaoyijiang-backend .
# 运行: docker run -p 8000:8000 -e DASHSCOPE_API_KEY=xxx xiaoyijiang-backend

FROM python:3.12-slim AS builder

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 运行阶段：使用精简镜像
FROM python:3.12-slim

WORKDIR /app

# 从 builder 复制已安装的依赖
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY app/ ./app/

# 非 root 用户运行
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# 生产模式运行 uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
