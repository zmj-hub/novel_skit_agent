<template>
  <AppCard title="智能体状态" icon="CpuChipIcon">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center py-8">
      <AppLoading size="lg" />
    </div>
    
    <!-- 数据展示 -->
    <div v-else class="space-y-3">
      <div 
        v-for="agent in agentsList" 
        :key="agent.id"
        class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
      >
        <div class="flex items-center gap-3">
          <div :class="['w-10 h-10 rounded-lg flex items-center justify-center', agent.bgColor]">
            <AppIcon :name="agent.icon" size="md" :class="agent.iconColor" />
          </div>
          <div>
            <div class="font-medium text-gray-900 text-sm">{{ agent.name }}</div>
            <div class="text-xs text-gray-500">{{ agent.description }}</div>
          </div>
        </div>
        <StatusBadge :status="agent.status" size="sm" />
      </div>
    </div>
  </AppCard>
</template>

<script setup>
import { computed } from 'vue'
import AppCard from './common/AppCard.vue'
import AppIcon from './common/AppIcon.vue'
import AppLoading from './common/AppLoading.vue'
import StatusBadge from './common/StatusBadge.vue'

const props = defineProps({
  agents: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// 智能体配置
const agentsConfig = [
  {
    id: 'creative',
    name: '创意策划智能体',
    description: '专注于创意生成与方案设计',
    icon: 'LightBulbIcon',
    bgColor: 'bg-warning-100',
    iconColor: 'text-warning-600',
  },
  {
    id: 'novel',
    name: '小说创作智能体',
    description: '负责故事内容的创作与优化',
    icon: 'BookOpenIcon',
    bgColor: 'bg-success-100',
    iconColor: 'text-success-600',
  },
  {
    id: 'scheduler',
    name: '协同调度智能体',
    description: '负责任务分发与流程控制',
    icon: 'CalendarIcon',
    bgColor: 'bg-primary-100',
    iconColor: 'text-primary-600',
  },
]

// 状态映射
const statusMap = {
  'available': 'success',
  '可用': 'success',
  'busy': 'warning',
  '繁忙': 'warning',
  'error': 'danger',
  '错误': 'danger',
  'offline': 'default',
  '离线': 'default',
}

// 智能体列表
const agentsList = computed(() => {
  return agentsConfig.map(config => {
    const status = props.agents[config.id] || '未知'
    return {
      ...config,
      status: statusMap[status] || 'default',
    }
  })
})
</script>
