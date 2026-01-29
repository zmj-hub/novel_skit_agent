<template>
  <AppCard title="工作流详情" icon="ListBulletIcon">
    <!-- 未选择工作流 -->
    <div v-if="!workflowId" class="text-center py-12">
      <AppEmpty 
        title="请选择工作流" 
        description="点击左侧执行历史中的任务查看详情" 
      />
    </div>
    
    <!-- 加载状态 -->
    <div v-else-if="loading" class="flex justify-center py-12">
      <AppLoading size="lg" />
    </div>
    
    <!-- 工作流步骤 -->
    <div v-else class="relative">
      <!-- 时间线 -->
      <div class="absolute left-4 top-8 bottom-4 w-0.5 bg-gray-200" />
      
      <div class="space-y-6">
        <div 
          v-for="(step, index) in steps" 
          :key="step.stepId"
          class="relative pl-12"
        >
          <!-- 节点 -->
          <div 
            :class="[
              'absolute left-0 w-8 h-8 rounded-full flex items-center justify-center',
              'text-white text-sm font-bold shadow-md',
              getStepColorClass(step.status)
            ]"
          >
            {{ index + 1 }}
          </div>
          
          <!-- 内容卡片 -->
          <div class="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors">
            <div class="flex items-start justify-between mb-2">
              <div>
                <h4 class="font-medium text-gray-900">{{ step.task }}</h4>
                <p class="text-sm text-gray-500 flex items-center gap-1 mt-1">
                  <AppIcon name="CpuChipIcon" size="xs" class="text-gray-400" />
                  {{ step.agentType }}
                </p>
              </div>
              <StatusBadge :status="step.status" size="sm" />
            </div>
            
            <div class="text-sm text-gray-500 space-y-1 mt-3">
              <p class="flex items-center gap-1">
                <AppIcon name="PlayIcon" size="xs" class="text-gray-400" />
                开始: {{ formatDateTime(step.startTime) }}
              </p>
              <p v-if="step.endTime" class="flex items-center gap-1">
                <AppIcon name="StopIcon" size="xs" class="text-gray-400" />
                结束: {{ formatDateTime(step.endTime) }}
              </p>
              <p class="flex items-center gap-1">
                <AppIcon name="ClockIcon" size="xs" class="text-gray-400" />
                耗时: {{ step.duration }}
              </p>
              <p v-if="step.error" class="flex items-center gap-1 text-danger-600 mt-2 p-2 bg-danger-50 rounded">
                <AppIcon name="ExclamationTriangleIcon" size="xs" />
                {{ step.error }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppCard>
</template>

<script setup>
import AppCard from './common/AppCard.vue'
import AppIcon from './common/AppIcon.vue'
import AppLoading from './common/AppLoading.vue'
import AppEmpty from './common/AppEmpty.vue'
import StatusBadge from './common/StatusBadge.vue'

const props = defineProps({
  workflowId: {
    type: String,
    default: ''
  },
  steps: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// 步骤颜色样式
const getStepColorClass = (status) => {
  const map = {
    success: 'bg-success-500',
    completed: 'bg-success-500',
    failed: 'bg-danger-500',
    running: 'bg-primary-500 animate-pulse',
    pending: 'bg-warning-500',
  }
  return map[status] || 'bg-gray-400'
}

// 格式化日期时间
const formatDateTime = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
</script>
