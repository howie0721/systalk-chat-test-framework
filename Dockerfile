# Dockerfile for CI/CD and local development
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Playwright 依賴
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 安裝 Playwright 瀏覽器
RUN playwright install chromium

# 複製專案檔案
COPY . .

# 設定環境變數
ENV PYTHONPATH=/app
ENV ENVIRONMENT=ci

# 預設命令
CMD ["pytest", "-v", "--cov=.", "--cov-report=html", "--cov-report=term"]
