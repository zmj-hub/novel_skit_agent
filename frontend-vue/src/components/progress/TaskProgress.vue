<template>
  <div class="task-progress">
    <div class="task-header">
      <div class="task-title">{{ taskName }}</div>
      <el-tag :type="statusType" size="small">{{ statusText }}</el-tag>
    </div>
    
    <div class="task-info">
      <span class="agent-name">{{ agentName }}</span>
      <span class="progress-text">{{ progress }}%</span>
    </div>
    
    <el-progress
      :percentage="progress"
      :status="progressStatus"
      :stroke-width="8"
    />
    
    <div v-if="updatedAt" class="task-time">
      更新时间: {{ formatTime(updatedAt) }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  taskName: {
    type: String,
    default: '',
  },
  agentName: {
    type: String,
    default: '',
  },
  progress: {
    type: Number,
    default: 0,
  },
  status: {
    type: String,
    default: 'pending',
  },
  updatedAt: {
    type: String,
    default: '',
  },
})

const statusType = computed(() => {
  const types = {
    pending: 'info',
    running: 'primary',
    completed: 'success',
    failed: 'danger',
  }
  return types[props.status] || 'info'
})

const statusText = computed(() => {
  const texts = {
    pending: '待开始',
    running: '进行中',
    completed: '已完成',
    failed: '失败',
  }
  return texts[props.status] || '未知'
})

const progressStatus = computed(() => {
  if (props.status === 'completed') return 'success'
  if (props.status === 'failed') return 'exception'
  return ''
})

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}
</script>

<style scoped>
.task-progress {
  padding: 16px;
  background-color: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 12px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.task-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.task-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.agent-name {
  font-size: 14px;
  color: #606266;
}

.progress-text {
  font-size: 14px;
  font-weight: bold;
  color: #409eff;
}

.task-time {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}
</style>
