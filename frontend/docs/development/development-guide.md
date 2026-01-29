# 前端开发指南

## 1. 开发环境搭建

### 1.1 系统要求
- **操作系统**：Windows、macOS、Linux
- **Node.js**：v18.0.0 或更高版本
- **npm**：v9.0.0 或更高版本
- **Git**：最新版本

### 1.2 环境搭建步骤

#### 1.2.1 克隆代码库
```bash
# 克隆代码库
git clone <repository-url>
cd novel-skit-agent
```

#### 1.2.2 安装依赖
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

#### 1.2.3 启动开发服务器
```bash
# 启动开发服务器
npm run dev

# 访问应用
# 打开浏览器，访问 http://localhost:5173
```

## 2. 项目配置

### 2.1 核心配置文件
- **package.json**：项目依赖和脚本配置
- **vite.config.js**：Vite 构建工具配置
- **tailwind.config.js**：Tailwind CSS 配置
- **.eslintrc.js**：ESLint 代码规范配置
- **.prettierrc.js**：Prettier 代码格式化配置
- **vite.config.test.js**：测试环境配置

### 2.2 环境变量
- **.env**：本地环境变量配置
- **.env.example**：环境变量示例配置

## 3. 开发流程

### 3.1 分支管理
- **main**：主分支，用于生产环境
- **develop**：开发分支，用于集成开发
- **feature/xxx**：特性分支，用于开发新功能
- **bugfix/xxx**：修复分支，用于修复 bug

### 3.2 开发步骤
1. **创建分支**：从 develop 分支创建特性分支
2. **开发功能**：实现新功能或修复 bug
3. **代码审查**：提交代码前进行代码审查
4. **测试**：运行测试，确保代码质量
5. **提交代码**：提交代码到特性分支
6. **创建 PR**：创建 Pull Request 到 develop 分支
7. **合并代码**：经过审查后合并到 develop 分支

### 3.3 代码提交规范
- **提交信息格式**：`[类型]: [描述]`
  - **类型**：feat（新功能）、fix（修复）、docs（文档）、style（样式）、refactor（重构）、test（测试）、chore（构建）
  - **描述**：简洁明了的描述
- **示例**：`feat: 添加智能体状态监控功能`

## 4. 代码规范

### 4.1 ESLint 规范
- **配置文件**：`.eslintrc.js`
- **运行检查**：`npm run lint`
- **常见规则**：
  - 使用双引号
  - 使用分号
  - 禁止未使用的变量
  - 禁止控制台日志（生产环境）
  - 遵循 Vue 最佳实践

### 4.2 Prettier 规范
- **配置文件**：`.prettierrc.js`
- **运行格式化**：`npm run format`
- **常见规则**：
  - 单引号
  - 分号
  - 尾随逗号
  - 箭头函数括号
  - 打印宽度 80

### 4.3 代码风格指南
- **缩进**：使用 2 个空格
- **命名规范**：
  - 组件名：PascalCase（如 Header.vue）
  - 变量名：camelCase（如 userInfo）
  - 常量名：SNAKE_CASE（如 MAX_LENGTH）
  - 函数名：camelCase（如 fetchData）
- **注释**：使用 JSDoc 格式，为组件、函数添加注释
- **文件组织**：按功能模块组织文件，保持目录结构清晰

## 5. 组件开发

### 5.1 组件创建流程
1. **创建组件文件**：在 `src/components/` 目录下创建组件文件
2. **定义组件**：使用 Vue 3 Composition API
3. **编写模板**：使用 Tailwind CSS 工具类
4. **添加样式**：使用组件内样式或 Tailwind CSS
5. **定义 props**：使用 `defineProps`
6. **定义事件**：使用 `defineEmits`
7. **添加逻辑**：在 `setup` 函数中添加逻辑
8. **导出组件**：默认导出组件

### 5.2 组件示例
```vue
<template>
  <div class="card">
    <h2 class="text-xl font-bold mb-4">{{ title }}</h2>
    <p>{{ content }}</p>
    <button @click="handleClick" class="btn btn-primary">点击按钮</button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  content: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['click'])

const handleClick = () => {
  emit('click')
}
</script>

<style scoped>
/* 组件内样式（如果需要） */
</style>
```

### 5.3 组件最佳实践
- **单一职责**：每个组件只负责一个功能
- **可复用性**：设计可复用的组件
- **props 验证**：为 props 添加类型验证和默认值
- **事件命名**：使用 kebab-case 命名事件
- **样式隔离**：使用 `scoped` 样式或 Tailwind CSS
- **性能优化**：使用 `computed`、`watch` 等优化性能

## 6. 状态管理

### 6.1 Pinia 使用指南
1. **创建 store**：在 `src/stores/` 目录下创建 store 文件
2. **定义状态**：在 `state` 函数中定义状态
3. **定义 getters**：添加计算属性
4. **定义 actions**：添加异步操作和状态更新
5. **使用 store**：在组件中导入并使用 store

### 6.2 Store 示例
```javascript
import { defineStore } from 'pinia'
import { apiService } from '../services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    isLoading: false,
    error: null
  }),

  getters: {
    isLoggedIn: (state) => !!state.user
  },

  actions: {
    async fetchUser() {
      try {
        this.isLoading = true
        this.error = null
        const data = await apiService.get('/user')
        this.user = data
      } catch (error) {
        this.error = error.message
      } finally {
        this.isLoading = false
      }
    }
  }
})
```

### 6.3 状态管理最佳实践
- **模块化**：按功能划分 store
- **单一数据源**：使用集中式状态管理
- **异步操作**：在 actions 中处理异步操作
- **错误处理**：在 actions 中处理错误
- **状态持久化**：使用 localStorage 或 sessionStorage 持久化状态

## 7. API 服务

### 7.1 服务创建流程
1. **创建服务文件**：在 `src/services/` 目录下创建服务文件
2. **定义方法**：封装 API 调用方法
3. **处理响应**：统一处理 API 响应
4. **错误处理**：统一处理 API 错误

### 7.2 服务示例
```javascript
import { apiService } from './api'
import { API_ENDPOINTS } from './endpoints'

export const userService = {
  async getUser() {
    try {
      const data = await apiService.get(API_ENDPOINTS.USER.GET)
      return data
    } catch (error) {
      console.error('获取用户信息失败:', error)
      throw error
    }
  }
}
```

### 7.3 API 服务最佳实践
- **封装 API 调用**：集中管理 API 调用
- **统一错误处理**：处理 API 错误
- **缓存**：缓存频繁使用的数据
- **防抖**：避免频繁 API 请求
- **超时处理**：设置合理的超时时间

## 8. 测试

### 8.1 测试类型
- **单元测试**：测试单个组件或函数
- **集成测试**：测试组件交互和服务调用
- **E2E 测试**：测试完整用户流程

### 8.2 测试工具
- **Vitest**：单元测试和集成测试
- **Vue Test Utils**：组件测试
- **Playwright**：E2E 测试

### 8.3 测试命令
```bash
# 运行单元测试
npm test

# 监视测试
npm run test:watch

# 测试覆盖率
npm run test:coverage

# 运行 E2E 测试
npm run e2e
```

### 8.4 测试最佳实践
- **测试覆盖率**：确保关键代码有测试覆盖
- **测试隔离**：每个测试独立运行
- **模拟依赖**：使用 mock 模拟外部依赖
- **测试命名**：使用清晰的测试命名
- **测试数据**：使用真实的测试数据

## 9. 构建与部署

### 9.1 构建流程
```bash
# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

### 9.2 构建产物
- **dist/**：构建输出目录
  - **assets/**：静态资源
  - **index.html**：HTML 入口文件

### 9.3 部署策略
- **静态部署**：部署到静态文件服务器
- **容器化部署**：使用 Docker 容器化部署
- **CI/CD**：使用 CI/CD 自动化部署

## 10. 代码审查

### 10.1 审查流程
1. **创建 PR**：提交代码到远程仓库，创建 Pull Request
2. **代码审查**：团队成员审查代码
3. **反馈**：提供代码改进建议
4. **修改**：根据反馈修改代码
5. **合并**：审查通过后合并代码

### 10.2 审查重点
- **代码质量**：代码是否符合规范
- **功能实现**：功能是否正确实现
- **性能**：代码是否高效
- **安全性**：代码是否安全
- **测试覆盖**：测试是否充分

## 11. 常见问题与解决方案

### 11.1 依赖问题
- **依赖冲突**：删除 node_modules 和 package-lock.json，重新安装
- **依赖缺失**：运行 `npm install` 安装依赖

### 11.2 构建问题
- **构建失败**：检查代码是否有语法错误
- **资源路径**：检查资源路径是否正确

### 11.3 运行问题
- **白屏**：检查控制台错误，修复代码问题
- **API 调用失败**：检查 API 地址和网络连接

### 11.4 测试问题
- **测试失败**：检查测试代码和实现代码
- **测试超时**：增加测试超时时间

## 12. 开发工具推荐

### 12.1 IDE/编辑器
- **VS Code**：推荐，支持 Vue、Tailwind CSS 等插件
  - **插件**：Vetur、Tailwind CSS IntelliSense、ESLint、Prettier

### 12.2 浏览器工具
- **Chrome DevTools**：调试和性能分析
- **Vue DevTools**：Vue 组件调试

### 12.3 其他工具
- **Git GUI**：Git 客户端工具
- **Postman**：API 测试工具
- **Docker**：容器化工具

## 13. 最佳实践

### 13.1 代码质量
- **遵循规范**：使用 ESLint 和 Prettier
- **代码审查**：定期进行代码审查
- **测试覆盖**：确保测试覆盖关键代码

### 13.2 性能优化
- **懒加载**：使用动态导入
- **缓存**：缓存 API 响应
- **虚拟滚动**：处理长列表
- **图片优化**：使用适当的图片格式和大小

### 13.3 安全性
- **输入验证**：验证用户输入
- **XSS 防护**：使用 Vue 的插值和指令
- **CSRF 防护**：使用 CSRF token
- **敏感信息**：不存储敏感信息在前端

### 13.4 可维护性
- **文档**：保持代码和文档同步
- **注释**：添加必要的注释
- **模块化**：按功能划分模块
- **组件复用**：设计可复用的组件

---

本开发指南旨在为开发人员提供前端开发的最佳实践和流程，帮助开发人员快速上手并遵循规范。如有任何疑问或建议，请随时提出。
