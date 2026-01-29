<template>
  <AppCard title="执行历史" icon="ClockIcon" class="h-full">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center py-12">
      <AppLoading size="lg" />
    </div>
    
    <!-- 空状态 -->
    <div v-else-if="!history.length" class="text-center py-12">
      <AppEmpty description="暂无执行历史" />
    </div>
    
    <!-- 历史列表 -->
    <div v-else class="space-y-3 max-h-[600px] overflow-y-auto pr-2">
      <div 
        v-for="task in history" 
        :key="task.id"
        :class="[
          'p-4 rounded-lg border-l-4 cursor-pointer transition-all duration-300',
          'hover:shadow-hover hover:-translate-y-0.5',
          getStatusBorderClass(task.status)
        ]"
        @click="$emit('select', task.id)"
      >
        <!-- 标题和状态 -->
        <div class="flex items-start justify-between mb-2">
          <h4 class="font-medium text-gray-900 line-clamp-1 flex-1 mr-3">{{ task.taskGoal }}</h4>
          <StatusBadge :status="task.status" size="sm" />
        </div>
        
        <!-- 时间和时长 -->
        <div class="flex items-center gap-4 text-sm text-gray-500 mb-2">
          <span class="flex items-center gap-1">
            <AppIcon name="CalendarIcon" size="xs" />
            {{ formatDate(task.startTime) }}
          </span>
          <span class="flex items-center gap-1">
            <AppIcon name="ClockIcon" size="xs" />
            {{ task.duration }}
          </span>
        </div>
        
        <!-- 参与智能体 -->
        <div class="flex flex-wrap gap-1.5">
          <span 
            v-for="agent in task.agents" 
            :key="agent"
            class="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded-full"
          >
            {{ agent }}
          </span>
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
  history: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['select'])

// 状态边框样式
const getStatusBorderClass = (status) => {
  const map = {
    completed: 'border-success-500 bg-success-50/50',
    success: 'border-success-500 bg-success-50/50',
    failed: 'border-danger-500 bg-danger-50/50',
    running: 'border-primary-500 bg-primary-50/50',
    pending: 'border-warning-500 bg-warning-50/50',
  }
  return map[status] || 'border-gray-300 bg-gray-50'
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
/* 自定义滚动条 */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
