# --- Stage 1: Go Builder ---
# 使用官方的 Go 镜像作为构建环境
FROM golang:1.22-alpine AS builder-go

# 设置工作目录
WORKDIR /src

# 复制 Go 项目的模块文件并下载依赖
COPY golang/go.mod ./
RUN go mod download

# 复制 Go 项目的源代码
COPY golang/ .

# 编译 Go 应用。CGO_ENABLED=0 创建一个静态链接的二进制文件，更适合容器环境
# -o 指定输出文件名和路径
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /go_app_binary .


# --- Stage 2: Final Image ---
# 使用你原来的 Python 基础镜像
FROM python:3.11-slim

# 设置主工作目录
WORKDIR /app

# 安装 Supervisor 和你的 Python 依赖
# 将 supervisor 添加到 apt-get install 列表中
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 \
    libnspr4 libnss3 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxdamage1 \
    libxext6 libxfixes3 libxrandr2 libxrender1 libxtst6 ca-certificates \
    fonts-liberation libasound2 libpangocairo-1.0-0 libpango-1.0-0 libu2f-udev xvfb \
    && rm -rf /var/lib/apt/lists/*

# 从 Go 构建阶段复制编译好的二进制文件到最终镜像中
COPY --from=builder-go /go_app_binary .

# 复制 Python 项目的 requirements.txt 并安装依赖
COPY camoufox-py/requirements.txt ./camoufox-py/requirements.txt
RUN pip install --no-cache-dir -r ./camoufox-py/requirements.txt

# 运行 camoufox fetch
# 注意：如果 camoufox 需要在项目根目录运行，需要调整 WORKDIR 或命令路径
RUN camoufox fetch

# 复制 Python 项目的所有文件
COPY camoufox-py/ .
# 为了保持目录结构清晰，我们把它放到 camoufox-py 子目录中
# WORKDIR /app/camoufox-py
# COPY camoufox-py/ .
# WORKDIR /app
# 上面的注释是一种替代方案，但当前方案更简单

# 复制 Supervisor 的配置文件
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 容器启动时，运行 Supervisor
# 它会根据 supervisord.conf 的配置来启动你的 Python 和 Go 应用
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]