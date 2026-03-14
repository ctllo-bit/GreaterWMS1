FROM --platform=linux/amd64 python:3.10.18-slim-bullseye
WORKDIR /GreaterWMS

# 系统依赖 只用 SQLite，可以去掉 libpq-dev
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# 复制依赖文件，安装 Python 依赖
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .


EXPOSE 8008

RUN chmod +x /GreaterWMS/backend_start.sh
CMD ["/GreaterWMS/backend_start.sh"]

