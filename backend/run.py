import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from 长沙餐馆信息管理系统.backend.app import router
app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],# 指定前端地址
        "methods": ["GET", "POST", "PUT", "DELETE"],# 允许的HTTP方法
        "allow_headers": ["Content-Type"] # 允许的请求头
    }
})
# 加载 .env 文件
load_dotenv()

# 然后就可以使用 os.getenv() 读取配置了
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

app.register_blueprint(router.restaurants)
app.register_blueprint(router.ai)
if __name__ == '__main__':
    print("running")
    app.run(debug=True)
