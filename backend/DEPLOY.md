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
- 正式发布：**必须使用 HTTPS**，并在小程序后台配置 request 合法域名

## 常见问题：上传接口 405 Method Not Allowed

**现象**：日志显示 `GET /api/upload/image 405`，但客户端调用的是 `uni.uploadFile`（应为 POST）。

**原因**：HTTP 301/302 重定向会将 POST 转为 GET。若经过 Nginx 等反向代理，且将 HTTP 重定向到 HTTPS，就会出现此问题。

**解决方案**：

1. **优先方案**：`BASE_URL` 直接使用 HTTPS，避免重定向。
2. **若必须重定向**：Nginx 使用 307/308（保留请求方法），例如：

```nginx
# 错误示例：301 会导致 POST 变 GET
# return 301 https://$host$request_uri;

# 正确：307 保留 POST 方法与 body
return 307 https://$host$request_uri;
```

3. **推荐 Nginx 配置**（HTTPS 反向代理到后端 8000）：

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    ssl_certificate     /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 10M;   # 上传图片需足够大
    }
}
```

小程序端 `BASE_URL` 使用 `https://your-domain.com`，无需经过 HTTP 重定向。
