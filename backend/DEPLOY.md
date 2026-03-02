# 换衣小程序后端 Docker 部署指南

## 前置条件

- 已安装 Docker 和 Docker Compose
- 阿里云百炼 API Key（DASHSCOPE_API_KEY）

## 方式一：Docker Compose（推荐）

1. 在 `backend` 目录创建 `.env` 文件：

```bash
cd backend
cp .env.example .env
# 编辑 .env，填入真实的 DASHSCOPE_API_KEY
```

2. 启动服务：

```bash
docker compose up -d
```

3. 验证：访问 `http://服务器IP:8000/docs` 查看 API 文档

4. 停止服务：`docker compose down`

## 方式二：原生 Docker 命令

```bash
cd backend
docker build -t xiaoyijiang-backend .
docker run -d \
  --name xiaoyijiang-backend \
  -p 8000:8000 \
  -e DASHSCOPE_API_KEY=你的API密钥 \
  --restart unless-stopped \
  xiaoyijiang-backend
```

## 生产环境建议

1. **反向代理**：使用 Nginx 或 Traefik 做 HTTPS 终止、限流、日志
2. **环境变量**：切勿将 API Key 写进镜像，通过 `-e` 或 `.env` 注入
3. **端口**：可按需修改 `docker-compose.yml` 中 `ports` 的宿主机端口
4. **日志**：`docker compose logs -f backend` 查看运行日志

## 小程序配置

部署后将 `miniprogram/api/index.js` 中 `BASE_URL` 改为：

- 开发调试：内网穿透后的地址（如 ngrok、frp）
- 正式发布：已备案域名的 HTTPS 地址（需在小程序后台配置 request 合法域名）
