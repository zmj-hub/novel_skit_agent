# 小说创作智能体 - Vue.js 版本

基于 Vue 3 + Element Plus + Pinia + Tailwind CSS 构建的小说创作智能体前端应用。

## 技术栈

- **框架**: Vue 3.4+ (Composition API)
- **构建工具**: Vite 5
- **UI组件库**: Element Plus 2.x
- **CSS框架**: Tailwind CSS 3.x
- **状态管理**: Pinia 2.x
- **路由**: Vue Router 4.x
- **HTTP客户端**: Axios

## 功能模块

1. **仪表盘 (Dashboard)**: 系统概览、统计卡片、智能体状态监控、执行历史
2. **智能对话 (Chat)**: 与AI助手进行对话
3. **创意策划 (Creative)**: 生成创意故事框架
4. **小说创作 (Novel)**: 创作和管理小说
5. **智能体协作 (Collaboration)**: 多智能体协作完成任务
6. **任务调度 (Scheduler)**: 调度智能体执行任务，支持WebSocket实时进度
7. **知识库 (Knowledge)**: 管理知识库内容
8. **系统设置 (Settings)**: 配置系统参数

## 项目结构

```
frontend-vue/
├── public/                 # 静态资源
├── src/
│   ├── assets/            # 资源文件
│   │   └── styles/        # 全局样式
│   ├── components/        # 组件
│   │   ├── layout/        # 布局组件
│   │   ├── common/        # 通用组件
│   │   └── progress/      # 进度组件
│   ├── views/             # 页面视图
│   ├── router/            # 路由配置
│   ├── stores/            # Pinia状态管理
│   ├── services/          # API服务
│   ├── utils/             # 工具函数
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
├── index.html             # HTML模板
├── package.json           # 项目配置
├── vite.config.js         # Vite配置
├── tailwind.config.js     # Tailwind配置
└── README.md              # 项目说明
```

## 安装和运行

### 安装依赖

```bash
npm install
```

### 开发环境

```bash
npm run dev
```

访问 http://localhost:3000

### 生产构建

```bash
npm run build
```

构建后的文件位于 `dist` 目录。

### 代码检查

```bash
npm run lint
```

### 代码格式化

```bash
npm run format
```

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| VITE_APP_TITLE | 应用标题 | 小说创作智能体 |
| VITE_APP_VERSION | 应用版本 | 1.0.0 |
| VITE_API_BASE_URL | API基础URL | http://localhost:8000/api |
| VITE_ENV | 环境 | development |

## 浏览器支持

- Chrome >= 80
- Firefox >= 75
- Safari >= 13
- Edge >= 80

## 迁移说明

本项目是从 React + TypeScript + Ant Design 迁移而来，主要变更：

1. **框架**: React → Vue 3
2. **语言**: TypeScript → JavaScript
3. **UI库**: Ant Design → Element Plus
4. **状态管理**: Redux Toolkit → Pinia
5. **路由**: React Router → Vue Router

## 许可证

MIT
