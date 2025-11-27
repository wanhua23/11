# 餐馆管理系统

## 项目简介
基于Vue.js + Flask的餐馆信息管理平台，支持餐馆的增删改查和AI智能客服。

## 技术栈
- 前端：Vue 3, Element Plus, Vue Router
- 后端：Flask, PyMySQL
- 数据库：MySQL

## 本地开发环境搭建

1. **克隆项目**
git clone [项目地址]
cd [项目文件夹]

2. **后端环境**
cd backend
python -m venv venv  # 创建虚拟环境
source venv/bin/activate  # Linux/Mac 激活
venv\Scripts\activate  # Windows 激活
pip install -r requirements.txt

3. **数据库设置**
- 创建名为 `cguan` 的数据库
- 导入 `cguan.sql` (如果需要)

4. **环境变量配置**
- 复制 `.env.example` 为 `.env`
- 在 `.env` 中填入你的数据库密码和API密钥

5. **启动后端服务**
python run.py

6. **启动前端服务**
cd frontend
npm install
npm run dev

访问 http://localhost:5173