<template>
  <span :class="badgeClasses">
    <span v-if="showDot" :class="dotClasses" />
    <slot>{{ displayText }}</slot>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: { 
    type: String, 
    required: true,
    validator: (value) => ['success', 'warning', 'danger', 'info', 'default', 'running', 'completed', 'failed', 'pending'].includes(value)
  },
  text: { 
    type: String, 
    default: '' 
  },
  showDot: { 
    type: Boolean, 
    default: true 
  },
  size: { 
    type: String, 
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
})

// 状态映射表
const statusMap = {
  success: { 
    bg: 'bg-success-50', 
    text: 'text-success-700', 
    dot: 'bg-success-500',
    label: '成功'
  },
  completed: { 
    bg: 'bg-success-50', 
    text: 'text-success-700', 
    dot: 'bg-success-500',
    label: '已完成'
  },
  warning: { 
    bg: 'bg-warning-50', 
    text: 'text-warning-700', 
    dot: 'bg-warning-500',
    label: '警告'
  },
  pending: { 
    bg: 'bg-warning-50', 
    text: 'text-warning-700', 
    dot: 'bg-warning-500',
    label: '待处理'
  },
  danger: { 
    bg: 'bg-danger-50', 
    text: 'text-danger-700', 
    dot: 'bg-danger-500',
    label: '错误'
  },
  failed: { 
    bg: 'bg-danger-50', 
    text: 'text-danger-700', 
    dot: 'bg-danger-500',
    label: '失败'
  },
  info: { 
    bg: 'bg-primary-50', 
    text: 'text-primary-700', 
    dot: 'bg-primary-500',
    label: '信息'
  },
  running: { 
    bg: 'bg-primary-50', 
    text: 'text-primary-700', 
    dot: 'bg-primary-500',
    label: '运行中'
  },
  default: { 
    bg: 'bg-gray-50', 
    text: 'text-gray-700', 
    dot: 'bg-gray-400',
    label: '未知'
  },
}

const sizeMap = {
  sm: 'px-2 py-0.5 text-xs gap-1.5',
  md: 'px-2.5 py-1 text-sm gap-2',
  lg: 'px-3 py-1.5 text-base gap-2',
}

const dotSizeMap = {
  sm: 'w-1.5 h-1.5',
  md: 'w-2 h-2',
  lg: 'w-2.5 h-2.5',
}

const currentStatus = computed(() => statusMap[props.status] || statusMap.default)

const displayText = computed(() => {
  return props.text || currentStatus.value.label
})

const badgeClasses = computed(() => {
  return [
    'inline-flex items-center rounded-full font-medium',
    sizeMap[props.size],
    currentStatus.value.bg,
    currentStatus.value.text,
  ].join(' ')
})

const dotClasses = computed(() => {
  return [
    'rounded-full',
    dotSizeMap[props.size],
    currentStatus.value.dot,
  ].join(' ')
})
</script>