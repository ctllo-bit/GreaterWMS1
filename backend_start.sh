#!/bin/bash
set -e  # 脚本中任何命令失败则立即退出

echo "==> 执行数据库迁移..."
python manage.py makemigrations
python manage.py migrate

echo "==> 启动 Daphne 服务..."
exec daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application