#!/bin/bash
set -e  # 脚本中任何命令失败则立即退出

echo "==> 执行数据库迁移..."
python manage.py makemigrations
python manage.py migrate

# # 动态修改前端 baseurl.txt
# HOST_PORT=${HOST_PORT:-8008}  # 默认8008
# sed -i "s|http://127.0.0.1:8008|http://127.0.0.1:${HOST_PORT}|g" /GreaterWMS/static/baseurl.txt




echo "==> 启动 Daphne 服务..."
exec daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application