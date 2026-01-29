# 组件使用指南

## 1. 通用组件

### 1.1 AppIcon - 图标组件

统一封装图标，解决图标尺寸不一致问题。

**基本用法**:
```vue
<template>
  <!-- 基础用法 -->
  <AppIcon name="ChartPieIcon" />
  
  <!-- 指定尺寸 -->
  <AppIcon name="ChartPieIcon" size="lg" />
  
  <!-- 指定颜色 -->
  <AppIcon name="ChartPieIcon" color="#3b82f6" />
  
  <!-- 添加自定义类 -->
  <AppIcon name="ChartPieIcon" className="mr-2" />
</template>

<script setup>
import AppIcon from './components/common/AppIcon.vue'
</script>
```

**Props**:

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| name | string | 必填 | 图标名称，如 'ChartPieIcon' |
| size | string | 'md' | 图标尺寸: xs/sm/md/lg/xl |
| color | string | 'currentColor' | 图标颜色 |
| className | string | '' | 自定义CSS类 |

**尺寸对照表**:

| size | 实际尺寸 | 适用场景 |
|------|----------|----------|
| xs | 12px | 内联图标、小标签 |
| sm | 16px | 按钮图标、列表图标 |
| md | 20px | 卡片标题图标 |
| lg | 24px | 导航图标、大按钮 |
| xl | 32px | 空状态图标、大图标 |

---

### 1.2 AppCard - 卡片组件

统一的卡片容器，支持标题、图标、悬停效果。

**基本用法**:
```vue
<template>
  <!-- 基础卡片 -->
  <AppCard title="卡片标题" icon="ChartPieIcon">
    <p>卡片内容</p>
  </AppCard>
  
  <!-- 可悬停卡片 -->
  <AppCard title="可点击卡片" icon="ChartPieIcon" :hoverable="true" @click="handleClick">
    <p>点击我</p>
  </AppCard>
  
  <!-- 自定义头部 -->
  <AppCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h3>自定义标题</h3>
        <button>操作</button>
      </div>
    </template>
    <p>卡片内容</p>
  </AppCard>
  
  <!-- 带底部 -->
  <AppCard title="带底部" icon="ChartPieIcon">
    <p>卡片内容</p>
    <template #footer>
      <button>查看更多</button>
    </template>
  </AppCard>
</template>

<script setup>
import AppCard from './components/common/AppCard.vue'

const handleClick = () => {
  console.log('卡片被点击')
}
</script>
```

**Props**:

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| title | string | '' | 卡片标题 |
| icon | string | '' | 标题图标名称 |
| hoverable | boolean | false | 是否启用悬停效果 |
| className | string | '' | 自定义CSS类 |
| padding | string | 'normal' | 内边距: none/small/normal/large |

**Slots**:

| 插槽 | 说明 |
|------|------|
| default | 卡片主要内容 |
| header | 自定义头部（会覆盖title和icon） |
| footer | 卡片底部内容 |

---

### 1.3 StatusBadge - 状态徽章

统一的状态指示器，支持多种状态和尺寸。

**基本用法**:
```vue
<template>
  <!-- 基础用法 -->
  <StatusBadge status="success" text="成功" />
  
  <!-- 不同状态 -->
  <StatusBadge status="success" />
  <StatusBadge status="warning" />
  <StatusBadge status="danger" />
  <StatusBadge status="info" />
  <StatusBadge status="running" />
  <StatusBadge status="completed" />
  <StatusBadge status="failed" />
  <StatusBadge status="pending" />
  
  <!-- 不同尺寸 -->
  <StatusBadge status="success" size="sm" />
  <StatusBadge status="success" size="md" />
  <StatusBadge status="success" size="lg" />
  
  <!-- 隐藏圆点 -->
  <StatusBadge status="success" :showDot="false" text="已完成" />
</template>

<script setup>
import StatusBadge from './components/common/StatusBadge.vue'
</script>
```

**Props**:

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| status | string | 必填 | 状态类型 |
| text | string | '' | 显示文本（为空时显示默认文本） |
| showDot | boolean | true | 是否显示状态圆点 |
| size | string | 'md' | 尺寸: sm/md/lg |

**状态映射**:

| status | 显示文本 | 颜色 |
|--------|----------|------|
| success | 成功 | 绿色 |
| completed | 已完成 | 绿色 |
| warning | 警告 | 橙色 |
| pending | 待处理 | 橙色 |
| danger | 错误 | 红色 |
| failed | 失败 | 红色 |
| info | 信息 | 蓝色 |
| running | 运行中 | 蓝色 |
| default | 未知 | 灰色 |

---

### 1.4 AppLoading - 加载组件

统一的加载动画组件。

**基本用法**:
```vue
<template>
  <!-- 基础用法 -->
  <AppLoading />
  
  <!-- 不同尺寸 -->
  <AppLoading size="sm" />
  <AppLoading size="md" />
  <AppLoading size="lg" />
  <AppLoading size="xl" />
  
  <!-- 带文字 -->
  <AppLoading size="lg" text="加载中..." />
</template>

<script setup>
import AppLoading from './components/common/AppLoading.vue'
</script>
```

**Props**:

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| size | string | 'md' | 尺寸: sm/md/lg/xl |
| text | string | '' | 加载提示文字 |

---

### 1.5 AppEmpty - 空状态组件

统一的空状态展示。

**基本用法**:
```vue
<template>
  <!-- 基础用法 -->
  <AppEmpty />
  
  <!-- 自定义标题和描述 -->
  <AppEmpty title="暂无数据" description="请稍后重试" />
  
  <!-- 带操作按钮 -->
  <AppEmpty title="暂无数据" description="点击按钮刷新">
    <button @click="refresh">刷新</button>
  </AppEmpty>
</template>

<script setup>
import AppEmpty from './components/common/AppEmpty.vue'

const refresh = () => {
  console.log('刷新数据')
}
</script>
```

**Props**:

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| title | string | '暂无数据' | 空状态标题 |
| description | string | '当前没有可显示的数据' | 空状态描述 |

**Slots**:

| 插槽 | 说明 |
|------|------|
| default | 自定义操作区域 |

---

### 1.6 AppChart - 图表组件

基于 Chart.js 的图表组件。

**基本用法**:
```vue
<template>
  <!-- 环形图 -->
  <AppChart 
    type="doughnut" 
    :data="chartData"
    :options="chartOptions"
    height="200"
  />
  
  <!-- 柱状图 -->
  <AppChart 
    type="bar" 
    :data="