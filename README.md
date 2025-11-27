# 长沙餐馆信息管理系统

## 项目简介

一个基于 Vue.js + Flask 的长沙餐馆信息管理平台，提供完整的餐馆信息管理功能和 AI 智能客服系统。系统支持餐馆信息的增删改查、智能搜索、多条件筛选，以及基于 AI 的餐馆推荐服务。

## 技术栈

### 前端技术
- **Vue 3** - 渐进式 JavaScript 框架
- **Element Plus** - UI 组件库
- **Vue Router** - 路由管理
- **Axios** - HTTP 请求库

### 后端技术
- **Flask** - Python Web 框架
- **Flask-CORS** - 跨域支持
- **PyMySQL** - MySQL 数据库连接
- **DBUtils** - 数据库连接池
- **OpenAI** - AI 对话接口（基于阿里云 DashScope）

### 数据库
- **MySQL** - 关系型数据库

## 功能特性

### 🏪 餐馆管理
- **餐馆列表** - 查看所有餐馆信息，支持分页显示
- **添加餐馆** - 新增餐馆信息，包含名称、地址、菜系、价格等
- **编辑餐馆** - 修改现有餐馆信息
- **删除餐馆** - 移除餐馆记录
- **智能搜索** - 支持按名称、菜系类型、价格区间搜索

### 🤖 AI 智能客服
- **智能对话** - 基于餐馆数据的智能推荐
- **快捷提问** - 预设常见问题快速提问
- **对话历史** - 查看历史对话记录
- **实时响应** - 流式输出响应内容

### 📊 数据管理
- **分页显示** - 大数据量分页处理
- **数据验证** - 前后端双重数据验证
- **错误处理** - 完善的错误提示机制

## 项目结构

```
changsha-restaurant-system/
├── backend/                    # 后端代码
│   ├── run.py                 # Flask 应用入口
│   ├── router.py              # 路由定义
│   ├── utils.py               # 数据库工具类
│   ├── requirements.txt       # Python 依赖
│   └── .env                   # 环境变量配置
├── frontend/                   # 前端代码
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   │   ├── List.vue       # 餐馆列表
│   │   │   ├── add.vue        # 添加餐馆
│   │   │   ├── put.vue        # 编辑餐馆
│   │   │   ├── ai.vue         # AI 客服
│   │   │   └── aiList.vue     # 对话历史
│   │   ├── router/            # 路由配置
│   │   ├── App.vue            # 根组件
│   │   └── main.js            # 应用入口
│   └── package.json           # 前端依赖
└── README.md                  # 项目说明
```

## 本地开发环境搭建

### 1. 克隆项目
```bash
git clone [项目地址]
cd changsha-restaurant-system
```

### 2. 后端环境配置

#### 创建虚拟环境
```bash
cd 11
cd backend
python -m venv venv

# Windows 激活
venv\Scripts\activate

# Linux/Mac 激活
source venv/bin/activate
```

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 数据库配置
1. 确保已安装 MySQL 数据库
2. 创建名为 `cguan` 的数据库
3. 创建必要的表结构（根据项目需求）

#### 环境变量配置
创建 `.env` 文件：
```env
# 阿里云 DashScope API 密钥
DASHSCOPE_API_KEY=your_aliyun_dashscope_api_key_here


#### 启动后端服务
```bash
python run.py
```
后端服务将在 http://127.0.0.1:5000 启动

### 3. 前端环境配置

#### 安装依赖
```bash
cd frontend
npm install
```

#### 启动开发服务器
```bash
npm run dev
```
前端服务将在 http://localhost:5173 启动

## API 接口文档

### 餐馆管理接口
- `GET /api/restaurants` - 获取餐馆列表
- `GET /api/restaurants/:id` - 获取单个餐馆详情
- `POST /api/restaurants` - 添加新餐馆
- `PUT /api/restaurants/:id` - 更新餐馆信息
- `DELETE /api/restaurants/:id` - 删除餐馆
- `POST /api/search` - 搜索餐馆

### AI 客服接口
- `POST /api/ai/chat` - AI 对话
- `GET /api/ai/List` - 获取对话历史

## 数据库设计

### 主要数据表
- `restaurants` - 餐馆信息表
- `question_table` - AI 对话历史表

## 部署说明

### 生产环境部署
1. 设置 `debug=False`
2. 配置生产环境数据库
3. 设置正确的 CORS 域名

### 环境变量
确保在生产环境中正确设置：
- `DASHSCOPE_API_KEY`

## 注意事项

1. **API 密钥安全**：不要将 API 密钥提交到版本控制系统
2. **数据库备份**：定期备份数据库数据
3. **CORS 配置**：在生产环境中正确配置允许的域名
4. **错误处理**：系统包含完整的错误处理机制

## 开发团队

- 前端开发：Vue 3 + Element Plus
- 后端开发：Flask + MySQL
- AI 集成：阿里云 DashScope

## 许可证

MIT License

## 更新日志

### v1.0.0
- 初始版本发布
- 完成基础餐馆管理功能
- 集成 AI 智能客服系统
- 实现前后端分离架构

---

**开始使用**：按照上述步骤配置环境，即可开始使用长沙餐馆信息管理系统！
