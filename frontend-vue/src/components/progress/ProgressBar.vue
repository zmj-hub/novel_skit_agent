<template>
  <div class="progress-bar-container">
    <div class="progress-info">
      <span class="progress-label">{{ label }}</span>
      <span class="progress-value">{{ progress }}%</span>
    </div>
    <div class="progress-bar-wrapper">
      <div
        class="progress-bar"
        :style="{
          width: `${progress}%`,
          backgroundColor: statusColor,
        }"
      ></div>
    </div>
    <div v-if="showStatus" class="progress-status">
      <el-tag :type="statusType" size="small">{{ statusText }}</el-tag>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  progress: {
    type: Number,
    default: 0,
  },
  label: {
    type: String,
    default: '',
  },
  status: {
    type: String,
    default: 'pending',
  },
  showStatus: {
    type: Boolean,
    default: true,
  },
})

const statusColor = computed(() => {
  const colors = {
    pending: '#909399',
    running: '#409eff',
    completed: '#67c23a',
    failed: '#f56c6c',
  }
  return colors[props.status] || colors.pending
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
</script>

<style scoped>
.progress-bar-container {
  width: 100%;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-label {
  font-size: 14px;
  color: #606266;
}

.progress-value {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
}

.progress-bar-wrapper {
  width: 100%;
  height: 8px;
  background-color: #e4e7ed;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-status {
  margin-top: 8px;
}
</style>
