# 前端架构说明

## 1. 架构概述

### 1.1 技术栈
- **前端框架**：Vue 3 Composition API
- **状态管理**：Pinia
- **CSS 框架**：Tailwind CSS v3
- **图表库**：Chart.js + vue-chartjs
- **HTTP 客户端**：Axios
- **构建工具**：Vite
- **代码规范**：ESLint + Prettier
- **测试框架**：Vitest + Vue Test Utils + Playwright
- **图标库**：@heroicons/vue

### 1.2 架构模式
- **组件化架构**：将应用拆分为多个可复用的组件
- **状态管理**：使用 Pinia 进行集中式状态管理
- **服务层**：封装 API 调用和业务逻辑
- **响应式设计**：适配不同屏幕尺寸
- **模块化组织**：按功能和职责划分模块

## 2. 目录结构

### 2.1 核心目录结构
```
frontend/
├── src/
│   ├── assets/            # 静态资源
│   │   └── tailwind.css   # Tailwind CSS 样式
│   ├── components/         # 组件
│   │   ├── AppIcon.vue     # 图标组件
│   │   ├── Header.vue      # 头部组件
│   │   ├── StatusOverview.vue  # 状态概览组件
│   │   ├── AgentStatus.vue     # 智能体状态组件
│   │   ├── ExecutionControl.vue  # 执行控制组件
│   │   ├── ExecutionHistory.vue  # 执行历史组件
│   │   ├── WorkflowDetails.vue   # 工作流详情组件
│   │   └── Notification.vue      # 通知组件
│   ├── services/           # 服务层
│   │   ├── api.js           # Axios 实例
│   │   ├── endpoints.js     # API 端点配置
│   │   ├── monitoringService.js  # 监控服务
│   │   └── workflowService.js    # 工作流服务
│   ├── stores/             # 状态管理
│   │   ├── monitoring.js    # 监控状态
│   │   ├── workflow.js      # 工作流状态
│   │   └── ui.js            # UI 状态
│   ├── utils/              # 工具函数
│   │   └── appUtils.js      # 应用工具函数
│   ├── constants/           # 常量
│   │   └── appConstants.js  # 应用常量
│   ├── types/               # 类型定义
│   │   └── appTypes.js      # 应用类型定义
│   ├── App.vue              # 根组件
│   └── main.js              # 入口文件
├── docs/                   # 文档
├── tests/                  # 测试
├── index.html              # HTML 模板
├── package.json            # 项目配置
├── tailwind.config.js      # Tailwind 配置
├── vite.config.js          # Vite 配置
└── vite.config.test.js     # 测试配置
```

### 2.2 目录职责说明
- **assets/**：存放静态资源，如样式文件、图片等
- **components/**：存放可复用的组件
- **services/**：封装 API 调用和业务逻辑
- **stores/**：使用 Pinia 进行状态管理
- **utils/**：存放通用工具函数
- **constants/**：存放常量定义
- **types/**：存放类型定义
- **docs/**：存放项目文档
- **tests/**：存放测试文件

## 3. 组件结构

### 3.1 根组件 (App.vue)
- **职责**：组织和管理整个应用的布局和主要组件
- **结构**：
  - Header：顶部导航栏
  - main：主要内容区
    - 左侧：状态概览、智能体状态、执行控制
    - 右侧：执行历史
    - 底部：工作流详情
  - Notification：通知组件

### 3.2 头部组件 (Header.vue)
- **职责**：显示应用标题、图标和操作按钮
- **属性**：无
- **事件**：
  - start-execution：启动执行
  - stop-execution：停止执行

### 3.3 状态概览组件 (StatusOverview.vue)
- **职责**：显示工作流状态概览和统计数据
- **属性**：
  - monitoringData：监控数据
- **功能**：
  - 显示总任务数、成功任务数、失败任务数、运行中任务数
  - 显示任务状态分布图表

### 3.4 智能体状态组件 (AgentStatus.vue)
- **职责**：显示各个智能体的状态
- **属性**：
  - monitoringData：监控数据
- **功能**：
  - 显示创意策划智能体状态
  - 显示小说创作智能体状态
  - 显示协同调度智能体状态

### 3.5 执行控制组件 (ExecutionControl.vue)
- **职责**：提供执行参数配置和控制
- **属性**：
  - defaultValues：默认执行参数
- **事件**：
  - update:taskGoal：更新任务目标
  - update:sessionId：更新会话 ID
  - update:model：更新模型
  - update:timeout：更新超时时间
  - update:priority：更新优先级

### 3.6 执行历史组件 (ExecutionHistory.vue)
- **职责**：显示工作流执行历史
- **属性**：
  - monitoringData：监控数据
- **事件**：
  - show-workflow-details：显示工作流详情

### 3.7 工作流详情组件 (WorkflowDetails.vue)
- **职责**：显示工作流的详细步骤和状态
- **属性**：
  - monitoringData：监控数据
  - selectedWorkflowId：选中的工作流 ID
- **事件**：
  - update-step-parameters：更新步骤参数

### 3.8 通知组件 (Notification.vue)
- **职责**：显示错误和成功消息
- **属性**：
  - message：通知消息
  - type：通知类型（error/success）
- **事件**：
  - close：关闭通知

### 3.9 图标组件 (AppIcon.vue)
- **职责**：统一管理和使用图标
- **属性**：
  - name：图标名称
  - size：图标大小
  - color：图标颜色
  - class：自定义类名
  - strokeWidth：描边宽度

## 4. 状态管理

### 4.1 状态管理架构
- **使用 Pinia**：替代 Vuex，提供更简洁的 API 和更好的 TypeScript 支持
- **模块化状态**：按功能划分状态模块
- **持久化**：可选，使用 localStorage 或 sessionStorage 持久化状态

### 4.2 监控状态 (monitoring.js)
- **状态**：
  - monitoringData：监控数据
  - selectedWorkflowId：选中的工作流 ID
  - isLoading：加载状态
  - error：错误信息
- **getters**：
  - getSelectedWorkflowDetails：获取选中的工作流详情
  - getExecutionHistory：获取执行历史
  - getAgentStatuses：获取智能体状态
- **actions**：
  - fetchMonitoringData：获取监控数据
  - setSelectedWorkflowId：设置选中的工作流 ID
  - updateStepParameters：更新步骤参数

### 4.3 工作流状态 (workflow.js)
- **状态**：
  - executionParams：执行参数
  - isExecuting：是否正在执行
  - executionError：执行错误
  - executionSuccess：执行成功信息
- **getters**：
  - getExecutionParams：获取执行参数
  - isExecutionInProgress：获取执行状态
- **actions**：
  - updateExecutionParams：更新执行参数
  - startExecution：启动执行
  - stopExecution：停止执行
  - resetExecutionMessages：重置执行消息

### 4.4 UI 状态 (ui.js)
- **状态**：
  - notifications：通知信息
  - isLoading：加载状态
  - loadingMessage：加载消息
- **getters**：
  - hasError：是否有错误
  - hasSuccess：是否有成功消息
  - isLoading：获取加载状态
- **actions**：
  - showError：显示错误消息
  - showSuccess：显示成功消息
  - clearError：清除错误消息
  - clearSuccess：清除成功消息
  - clearAllNotifications：清除所有通知
  - setLoading：设置加载状态

## 5. 服务层

### 5.1 API 配置 (api.js)
- **职责**：配置 Axios 实例，添加拦截器
- **功能**：
  - 创建 Axios 实例
  - 请求拦截器：添加认证信息
  - 响应拦截器：统一处理响应和错误

### 5.2 API 端点 (endpoints.js)
- **职责**：集中管理 API 端点
- **配置**：
  - MONITORING：监控相关端点
  - WORKFLOW：工作流相关端点

### 5.3 监控服务 (monitoringService.js)
- **职责**：封装监控相关的 API 调用
- **方法**：
  - getMonitoringData：获取监控数据
  - updateStepParameters：更新步骤参数

### 5.4 工作流服务 (workflowService.js)
- **职责**：封装工作流相关的 API 调用
- **方法**：
  - startExecution：启动工作流执行
  - stopExecution：停止工作流执行

## 6. 数据流

### 6.1 组件数据流
1. **父组件向子组件传递数据**：通过 props
2. **子组件向父组件传递事件**：通过 emit
3. **兄弟组件通信**：通过 Pinia 状态管理

### 6.2 API 调用流程
1. **组件触发 action**：调用 store 中的 action
2. **action 调用服务**：调用服务层方法
3. **服务调用 API**：使用 Axios 发送请求
4. **响应处理**：服务处理响应，返回数据
5. **更新状态**：store 更新状态
6. **组件响应**：组件根据状态变化更新 UI

### 6.3 状态更新流程
1. **用户交互**：用户操作触发事件
2. **事件处理**：组件处理事件，调用 store action
3. **状态更新**：store action 更新状态
4. **组件更新**：组件响应状态变化，更新 UI

## 7. 响应式设计

### 7.1 断点设计
- **移动端**：< 640px (sm:)
- **平板端**：640px - 1024px (md:)
- **桌面端**：1024px - 1280px (lg:)
- **大屏幕**：> 1280px (xl:)

### 7.2 响应式工具类
- **容器**：.responsive-container
- **网格**：.responsive-grid, .responsive-grid-2, .responsive-grid-4
- **字体**：.text-responsive
- **间距**：.spacing-responsive
- **卡片**：.card-responsive
- **按钮**：.btn-responsive
- **图标**：.icon-responsive

### 7.3 适配策略
- **移动优先**：从移动端开始设计
- **渐进增强**：为更大屏幕添加功能
- **灵活布局**：使用 flexbox 和 grid
- **图片适配**：使用响应式图片

## 8. 性能优化

### 8.1 代码优化
- **组件拆分**：合理拆分组件，提高复用率
- **懒加载**：使用动态导入
- **计算属性**：缓存计算结果
- **响应式数据**：合理使用 ref 和 reactive

### 8.2 网络优化
- **防抖**：避免频繁 API 请求
- **缓存**：缓存 API 响应
- **压缩**：使用 Vite 压缩资源
- **CDN**：使用 CDN 加速静态资源

### 8.3 渲染优化
- **虚拟滚动**：处理长列表
- **条件渲染**：避免不必要的渲染
- **key 属性**：合理使用 key，提高渲染性能

## 9. 测试策略

### 9.1 单元测试
- **测试文件**：tests/unit/
- **测试工具**：Vitest + Vue Test Utils
- **测试内容**：组件功能、计算属性、方法

### 9.2 集成测试
- **测试文件**：tests/integration/
- **测试工具**：Vitest + Vue Test Utils + Pinia
- **测试内容**：组件交互、状态管理、服务调用

### 9.3 E2E 测试
- **测试文件**：tests/e2e/
- **测试工具**：Playwright
- **测试内容**：完整用户流程、页面导航、表单提交

### 9.4 测试命令
- **运行单元测试**：`npm test`
- **监视测试**：`npm run test:watch`
- **测试覆盖率**：`npm run test:coverage`
- **运行 E2E 测试**：`npm run e2e`

## 10. 开发流程

### 10.1 开发环境
- **启动开发服务器**：`npm run dev`
- **代码规范检查**：`npm run lint`
- **代码格式化**：`npm run format`

### 10.2 构建部署
- **构建生产版本**：`npm run build`
- **预览生产版本**：`npm run preview`

### 10.3 代码规范
- **ESLint**：检查代码质量和风格
- **Prettier**：自动格式化代码
- **Git Hooks**：可选，使用 husky 进行提交前检查

## 11. 安全性

### 11.1 前端安全
- **XSS 防护**：使用 Vue 的插值和指令
- **CSRF 防护**：使用 CSRF token
- **输入验证**：验证用户输入
- **敏感信息**：不存储敏感信息在前端

### 11.2 API 安全
- **认证**：使用 token 认证
- **授权**：验证用户权限
- **HTTPS**：使用 HTTPS 传输

## 12. 文档和维护

### 12.1 文档结构
- **设计规范**：docs/design/
- **架构说明**：docs/architecture/
- **开发指南**：docs/development/

### 12.2 维护指南
- **版本控制**：使用 Git 进行版本管理
- **分支策略**：main 分支用于生产，feature 分支用于开发
- **代码审查**：提交前进行代码审查
- **问题跟踪**：使用 issue 跟踪问题

---

本架构说明旨在为开发人员提供应用的整体架构和各个部分的职责，帮助开发人员理解和维护应用。如有任何疑问或建议，请随时提出。
