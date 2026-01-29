# Novel Skit Agent 设计系统

## 1. 设计原则

### 1.1 核心理念
- **清晰性**: 信息层次清晰，用户能快速找到所需内容
- **一致性**: 统一的视觉语言和交互模式
- **响应性**: 适配各种设备尺寸，提供流畅体验
- **专业性**: 现代化的界面设计，体现系统专业性

### 1.2 设计目标
- 提升用户操作效率
- 降低认知负担
- 增强视觉吸引力
- 确保可访问性

## 2. 色彩系统

### 2.1 主色调
```
Primary (蓝色系)
├── 50:  #eff6ff  (最浅)
├── 100: #dbeafe
├── 200: #bfdbfe
├── 300: #93c5fd
├── 400: #60a5fa
├── 500: #3b82f6  (主色)
├── 600: #2563eb
├── 700: #1d4ed8
├── 800: #1e40af
└── 900: #1e3a8a  (最深)
```

### 2.2 状态色
```
Success (绿色系)
├── 500: #10b981  (成功)
└── 600: #059669

Warning (橙色系)
├── 500: #f59e0b  (警告)
└── 600: #d97706

Danger (红色系)
├── 500: #ef4444  (错误)
└── 600: #dc2626

Info (蓝色系)
├── 500: #0ea5e9  (信息)
└── 600: #0284c7
```

### 2.3 中性色
```
Gray (灰色系)
├── 50:  #f9fafb  (背景)
├── 100: #f3f4f6
├── 200: #e5e7eb  (边框)
├── 300: #d1d5db
├── 400: #9ca3af  (次要文字)
├── 500: #6b7280
├── 600: #4b5563
├── 700: #374151  (主要文字)
├── 800: #1f2937
└── 900: #111827  (最深)
```

### 2.4 色彩使用规范

| 场景 | 颜色 | 用途 |
|------|------|------|
| 主按钮 | primary-500 | 主要操作按钮 |
| 成功状态 | success-500 | 成功提示、完成状态 |
| 警告状态 | warning-500 | 警告提示、待处理状态 |
| 错误状态 | danger-500 | 错误提示、失败状态 |
| 背景色 | gray-50 | 页面背景 |
| 卡片背景 | white | 卡片、弹窗背景 |
| 边框色 | gray-200 | 分割线、边框 |
| 主要文字 | gray-700 | 标题、正文 |
| 次要文字 | gray-500 | 描述、辅助文字 |

## 3. 字体系统

### 3.1 字体族
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### 3.2 字号规范

| 层级 | 字号 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| 标题1 | 1.875rem (30px) | 2.25rem | 700 | 页面主标题 |
| 标题2 | 1.5rem (24px) | 2rem | 600 | 卡片标题 |
| 标题3 | 1.25rem (20px) | 1.75rem | 600 | 小节标题 |
| 正文大 | 1.125rem (18px) | 1.75rem | 400 | 重要正文 |
| 正文 | 1rem (16px) | 1.5rem | 400 | 普通正文 |
| 小字 | 0.875rem (14px) | 1.25rem | 400 | 辅助文字 |
| 超小 | 0.75rem (12px) | 1rem | 400 | 标签、时间 |

### 3.3 字重规范
- **font-normal (400)**: 正文、描述
- **font-medium (500)**: 次要标题、强调
- **font-semibold (600)**: 卡片标题、按钮文字
- **font-bold (700)**: 页面标题、重要数字

## 4. 间距系统

### 4.1 基础单位
基础间距单位: `0.25rem` (4px)

### 4.2 间距规范

| 名称 | 值 | 用途 |
|------|-----|------|
| xs | 0.5rem (8px) | 紧凑间距、图标间距 |
| sm | 1rem (16px) | 小组件内边距 |
| md | 1.5rem (24px) | 卡片内边距 |
| lg | 2rem (32px) | 大组件间距 |
| xl | 3rem (48px) | 区块间距 |

### 4.3 布局间距
- **页面内边距**: px-4 (16px)
- **卡片内边距**: p-6 (24px)
- **组件间距**: gap-6 (24px)
- **网格间距**: gap-6 (24px)

## 5. 阴影系统

### 5.1 阴影规范

| 名称 | 值 | 用途 |
|------|-----|------|
| shadow-sm | 0 1px 2px 0 rgba(0,0,0,0.05) | 按钮、小元素 |
| shadow-card | 0 4px 6px -1px rgba(0,0,0,0.1) | 卡片 |
| shadow-hover | 0 10px 15px -3px rgba(0,0,0,0.1) | 悬停状态 |
| shadow-soft | 0 2px 15px -3px rgba(0,0,0,0.07) | 弹窗、下拉菜单 |

## 6. 圆角系统

### 6.1 圆角规范

| 名称 | 值 | 用途 |
|------|-----|------|
| rounded | 0.25rem (4px) | 小按钮、标签 |
| rounded-lg | 0.5rem (8px) | 按钮、输入框 |
| rounded-xl | 0.75rem (12px) | 卡片 |
| rounded-2xl | 1rem (16px) | 大卡片、弹窗 |
| rounded-full | 9999px | 圆形按钮、头像 |

## 7. 图标系统

### 7.1 图标库
- **Heroicons**: 主要图标库
- **Ant Design Icons**: 备用图标库

### 7.2 图标尺寸

| 名称 | 尺寸 | 用途 |
|------|------|------|
| xs | 12px (w-3 h-3) | 内联图标、小标签 |
| sm | 16px (w-4 h-4) | 按钮图标、列表图标 |
| md | 20px (w-5 h-5) | 卡片标题图标 |
| lg | 24px (w-6 h-6) | 导航图标、大按钮 |
| xl | 32px (w-8 h-8) | 空状态图标、大图标 |

### 7.3 图标使用规范
- 使用 `AppIcon` 组件统一调用
- 指定合适的尺寸，避免图标过大或过小
- 保持图标颜色与上下文一致

## 8. 组件规范

### 8.1 卡片 (AppCard)
```vue
<AppCard 
  title="卡片标题" 
  icon="IconName"
  :hoverable="true"
>
  <!-- 内容 -->
</AppCard>
```

**样式规范**:
- 背景: 白色
- 圆角: rounded-xl (12px)
- 阴影: shadow-card
- 内边距: p-6 (24px)
- 悬停效果: shadow-hover + translateY(-2px)

### 8.2 按钮
**主按钮**:
```
背景: bg-primary-500
悬停: bg-primary-600
文字: text-white
圆角: rounded-lg
内边距: px-4 py-2
```

**危险按钮**:
```
背景: bg-danger-500
悬停: bg-danger-600
文字: text-white
```

**次要按钮**:
```
背景: bg-gray-100
悬停: bg-gray-200
文字: text-gray-700
```

### 8.3 状态徽章 (StatusBadge)
```vue
<StatusBadge status="success" text="成功" size="md" />
```

**状态映射**:
- success → 绿色徽章
- warning → 橙色徽章
- danger → 红色徽章
- info → 蓝色徽章
- default → 灰色徽章

### 8.4 图标组件 (AppIcon)
```vue
<AppIcon name="IconName" size="md" color="#3b82f6" />
```

**尺寸映射**:
- xs → 12px
- sm → 16px
- md → 20px
- lg → 24px
- xl → 32px

## 9. 响应式设计

### 9.1 断点系统
```
sm: 640px   (手机横屏)
md: 768px   (平板)
lg: 1024px  (小桌面)
xl: 1280px  (大桌面)
```

### 9.2 布局适配

**桌面端 (lg+)**:
- 三列布局: 3-5-4
- 侧边栏固定
- 完整导航显示

**平板端 (md)**:
- 两列布局
- 部分导航折叠
- 保持核心功能

**移动端 (< md)**:
- 单列布局
- 汉堡菜单导航
- 简化信息显示

### 9.3 响应式类名
```css
/* 网格布局 */
grid-cols-1 lg:grid-cols-12

/* 显示/隐藏 */
hidden md:block
md:hidden

/* 间距调整 */
p-4 md:p-6
space-y-4 md:space-y-6
```

## 10. 动画规范

### 10.1 过渡动画
```css
/* 默认过渡 */
transition-all duration-300 ease-out

/* 快速过渡 */
transition-all duration-150 ease-out

/* 慢速过渡 */
transition-all duration-500 ease-out
```

### 10.2 悬停效果
```css
/* 卡片悬停 */
hover:shadow-hover hover:-translate-y-0.5

/* 按钮悬停 */
hover:bg-primary-600

/* 链接悬停 */
hover:text-primary-600
```

### 10.3 自定义动画
```css
/* 淡入 */
@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

/* 上滑 */
@keyframes slideUp {
  0% { transform: translateY(10px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}
```

## 11. 可访问性

### 11.1 颜色对比度
- 正文文字与背景对比度 ≥ 4.5:1
- 大文字与背景对比度 ≥ 3:1
- 交互元素与背景对比度 ≥ 3:1

### 11.2 焦点状态
- 所有可交互元素都有可见的焦点状态
- 焦点环颜色: ring-primary-500
- 焦点环宽度: ring-2

### 11.3 语义化
- 使用正确的HTML标签
- 提供ARIA标签
- 支持键盘导航

## 12. 最佳实践

### 12.1 代码规范
- 使用 Tailwind 工具类
- 避免内联样式
- 保持组件单一职责
- 使用 TypeScript 类型

### 12.2 性能优化
- 图片懒加载
- 组件按需加载
- 避免不必要的重渲染
- 使用 CSS 动画代替 JS 动画

### 12.3 文件组织
```
src/
├── components/
│   ├── common/      # 通用组件
│   └── business/    # 业务组件
├── views/           # 页面视图
├── stores/          # 状态管理
├── utils/           # 工具函数
└── styles/          # 全局样式
```

---

*设计系统版本: 1.0*
*最后更新: 2026-01-29*
