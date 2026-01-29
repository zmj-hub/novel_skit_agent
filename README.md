# Novel Skit Agent - 前后端分离架构

## 项目概述

Novel Skit Agent 是一个基于多智能体协作的小说创作系统，采用前后端分离架构设计，实现了前端展示逻辑与后端业务逻辑的完全分离。

## 架构特点

- **前后端物理分离**：前端代码和后端代码完全独立存放
- **标准化API通信**：前后端通过RESTful API进行数据交互
- **独立构建部署**：前后端拥有各自的构建流程和部署配置
- **现代化技术栈**：前端使用Vue 3 + Tailwind CSS，后端使用FastAPI + LangChain

## 目录结构

```
novel_skit_agent/
├── backend/            # 后端代码目录
│   ├── agent/          # 智能体实现
│   ├── api/            # API接口定义
│   ├── core/           # 核心功能模块
│   ├── models/         # 数据模型
│   ├── rag/            # 检索增强生成
│   ├── utils/          # 工具函数
│   ├── config/         # 配置文件
│   ├── logs/           # 日志目录
│   ├── main.py         # 后端入口文件
│   ├── requirements.txt # 后端依赖
│   ├── start.sh        # Linux启动脚本
│   ├── start.bat       # Windows启动脚本
│   └── .env            # 环境配置文件
├── frontend/           # 前端代码目录
│   ├── src/            # 前端源码
│   │   ├── assets/     # 静态资源
│   │   ├── components/ # 组件
│   │   ├── services/   # API服务
│   │   ├── stores/     # 状态管理
│   │   ├── utils/      # 工具函数
│   │   ├── App.vue     # 根组件
│   │   └── main.js     # 前端入口
│   ├── public/         # 公共资源
│   ├── package.json    # 前端依赖
│   ├── vite.config.js  # Vite配置
│   └── tailwind.config.js # Tailwind配置
└── README.md           # 项目说明文档
```

## 技术栈

### 前端技术栈
- **框架**：Vue 3
- **状态管理**：Pinia
- **HTTP客户端**：Axios
- **样式**：Tailwind CSS
- **UI组件**：Ant Design Vue
- **构建工具**：Vite

### 后端技术栈
- **框架**：FastAPI
- **语言模型**：LangChain, LangGraph
- **缓存**：Redis
- **向量数据库**：ChromaDB
- **部署**：Uvicorn

## 快速开始

### 后端启动

1. **进入后端目录**
   ```bash
   cd backend
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动服务**
   - Linux/Mac
     ```bash
     ./start.sh
     ```
   - Windows
     ```bash
     start.bat
     ```

4. **验证后端服务**
   后端服务默认运行在 `http://localhost:8000`
   ```bash
   curl http://localhost:8000/api/monitoring/data
   ```

### 前端启动

1. **进入前端目录**
   ```bash
   cd frontend
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **启动开发服务器**
   ```bash
   npm run dev
   ```

4. **访问前端页面**
   前端服务默认运行在 `http://localhost:3000`

## API文档

后端API文档可通过以下地址访问：
- **Swagger UI**：`http://localhost:8000/docs`
- **ReDoc**：`http://localhost:8000/redoc`

## 环境配置

### 后端环境变量

在 `backend/.env` 文件中配置以下环境变量：

```env
# API配置
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# 数据库配置
REDIS_HOST=localhost
REDIS_PORT=6379

# 模型配置
DEFAULT_MODEL=Qwen/Qwen3-30B-A3B-Instruct-2507
EMBEDDING_MODEL=text-embedding-3-small

# 安全配置
CORS_ORIGINS=*

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=./logs
```

### 前端环境配置

在 `frontend/.env` 文件中配置以下环境变量：

```env
# API配置
VITE_API_BASE_URL=http://localhost:8000/api

# 应用配置
VITE_APP_NAME=Novel Skit Agent
VITE_APP_VERSION=1.0.0
```

## 构建与部署

### 前端构建

```bash
cd frontend
npm run build
```
构建产物将生成在 `frontend/dist` 目录中。

### 后端部署

1. **安装依赖**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **启动生产服务**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

## 开发指南

### 前端开发

1. **代码风格**：使用ESLint和Prettier保持代码风格一致
2. **组件设计**：遵循Vue 3 Composition API最佳实践
3. **API调用**：通过services目录下的API服务统一管理

### 后端开发

1. **代码风格**：遵循PEP 8编码规范
2. **API设计**：使用FastAPI的路径操作装饰器定义API
3. **错误处理**：使用统一的错误处理机制

## 测试

### 前端测试

```bash
cd frontend
npm run test       # 运行单元测试
npm run e2e        # 运行端到端测试
```

### 后端测试

```bash
cd backend
pytest
```

## 监控与维护

- **API监控**：通过 `/api/monitoring/data` 接口获取系统状态
- **日志管理**：日志文件存储在 `backend/logs` 目录
- **性能监控**：可通过FastAPI自带的性能指标进行监控

## 常见问题

1. **API连接失败**：检查后端服务是否启动，以及前端API配置是否正确
2. **前端页面空白**：检查浏览器控制台是否有错误信息，确保前端依赖安装正确
3. **智能体功能不可用**：检查相关API密钥是否配置，如OPENAI_API_KEY

## 版本历史

- v1.0.0：初始版本，实现前后端分离架构

## 贡献指南

欢迎提交Issue和Pull Request，参与项目开发。

## 许可证

本项目采用MIT许可证。
