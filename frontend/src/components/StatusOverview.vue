<template>
  <AppCard title="工作流状态概览" icon="ChartPieIcon">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center py-8">
      <AppLoading size="lg" />
    </div>
    
    <!-- 空状态 -->
    <div v-else-if="!hasData" class="text-center py-8">
      <AppEmpty description="暂无监控数据" />
    </div>
    
    <!-- 数据展示 -->
    <div v-else class="space-y-6">
      <!-- 统计数字 -->
      <div class="grid grid-cols-2 gap-3">
        <div class="bg-gray-50 rounded-lg p-3">
          <div class="text-xs text-gray-500 mb-1">总任务数</div>
          <div class="text-xl font-bold text-gray-900">{{ data.totalTasks || 0 }}</div>
        </div>
        <div class="bg-success-50 rounded-lg p-3">
          <div class="text-xs text-success-600 mb-1">成功任务</div>
          <div class="text-xl font-bold text-success-600">{{ data.successTasks || 0 }}</div>
        </div>
        <div class="bg-danger-50 rounded-lg p-3">
          <div class="text-xs text-danger-600 mb-1">失败任务</div>
          <div class="text-xl font-bold text-danger-600">{{ data.failedTasks || 0 }}</div>
        </div>
        <div class="bg-primary-50 rounded-lg p-3">
          <div class="text-xs text-primary-600 mb-1">运行中</div>
          <div class="text-xl font-bold text-primary-600">{{ data.runningTasks || 0 }}</div>
        </div>
      </div>
      
      <!-- 平均执行时间 -->
      <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
        <div class="flex items-center gap-2">
          <AppIcon name="ClockIcon" size="sm" class="text-gray-400" />
          <span class="text-sm text-gray-600">平均执行时间</span>
        </div>
        <span class="font-semibold text-gray-900">{{ data.avgExecutionTime || '0s' }}</span>
      </div>
      
      <!-- 图表 -->
      <div class="h-48">
        <div v-if="hasData" class="flex items-center justify-center h-full">
          <div class="text-center">
            <div class="text-4xl font-bold text-primary-500 mb-2">{{ totalTasks }}</div>
            <div class="text-sm text-gray-500">总任务</div>
          </div>
        </div>
      </div>
      
      <!-- 状态分布 -->
      <div class="grid grid-cols-3 gap-2 text-center">
        <div class="p-2 bg-success-50 rounded-lg">
          <AppIcon name="CheckCircleIcon" size="md" class="text-success-500 mx-auto mb-1" />
          <div class="text-xs text-gray-600">成功</div>
          <div class="text-lg font-bold text-success-600">{{ successPercentage }}%</div>
        </div>
        <div class="p-2 bg-danger-50 rounded-lg">
          <AppIcon name="XCircleIcon" size="md" class="text-danger-500 mx-auto mb-1" />
          <div class="text-xs text-gray-600">失败</div>
          <div class="text-lg font-bold text-danger-600">{{ failedPercentage }}%</div>
        </div>
        <div class="p-2 bg-primary-50 rounded-lg">
          <AppIcon name="PlayCircleIcon" size="md" class="text-primary-500 mx-auto mb-1" />
          <div class="text-xs text-gray-600">运行中</div>
          <div class="text-lg font-bold text-primary-600">{{ runningPercentage }}%</div>
        </div>
      </div>
    </div>
  </AppCard>
</template>

<script setup>
import { computed } from 'vue'
import AppCard from './common/AppCard.vue'
import AppIcon from './common/AppIcon.vue'
import AppLoading from './common/AppLoading.vue'
import AppEmpty from './common/AppEmpty.vue'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// 是否有有效数据
const hasData = computed(() => {
  return props.data && 
         typeof props.data === 'object' &&
         (props.data.totalTasks !== undefined ||
          props.data.successTasks !== undefined ||
          props.data.failedTasks !== undefined ||
          props.data.runningTasks !== undefined)
})

// 计算百分比
const total = computed(() => {
  return (props.data.successTasks || 0) + 
         (props.data.failedTasks || 0) + 
         (props.data.runningTasks || 0)
})

const successPercentage = computed(() => {
  if (total.value === 0) return 0
  return Math.round((props.data.successTasks || 0) / total.value * 100)
})

const failedPercentage = computed(() => {
  if (total.value === 0) return 0
  return Math.round((props.data.failedTasks || 0) / total.value * 100)
})

const runningPercentage = computed(() => {
  if (total.value === 0) return 0
  return Math.round((props.data.runningTasks || 0) / total.value * 100)
})

// 总任务数
const totalTasks = computed(() => {
  return props.data.totalTasks || 0
})
</script>
