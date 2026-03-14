# 安装 Python 3.10
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev build-essential libpq-dev -y

# 安装 Node
1、安装nvm， 可以随时切换 Node 版本
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc

2、安装 Node 16
nvm install 16
nvm alias default 16

# 数据库（开发一般 sqlite，生产 PostgreSQL）
sudo apt install postgresql -y


# 确认版本：
python3 --version
node -v
npm -v

后端开发（Django）

0、删除虚拟环境
deactivate   # 如果还在旧 venv 里
rm -rf venv

1、创建虚拟环境
python3.10 -m venv venv
source venv/bin/activate

2、更新pip并安装依赖
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

3、初始化数据库
python manage.py makemigrations
python manage.py migrate

4、（可选）创建管理员账号，拥有最高权限，能登录 Django 自带的 admin 后台（http://127.0.0.1:8000/admin/）
python manage.py createsuperuser

5、启动开发服务器
//用途：性能低，有热重载，开发环境，调试用
python manage.py runserver 0.0.0.0:8008

//用途：更高性能，不会热重载，生产环境，异步后台任务
daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application

# 后端启动
daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application
daphne -b 0.0.0.0 -p 8008 greaterwms.asgi:application
# Nginx 反向代理静态前端 + 后端 API
前端会向 "http://{局域网ip}:8008"发请求, 在这里我们只是看下项目是不是可以运行

前端开发
npm install
npm run dev




"scripts": {
  "dev": "NODE_OPTIONS=--openssl-legacy-provider quasar dev"
}
npx quasar dev
