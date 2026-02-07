<template>
  <div class="websocket-progress">
    <div class="connection-status">
      <el-tag :type="connectionStatusType" effect="dark" size="small">
        <el-icon class="status-icon">
          <CircleCheck v-if="isConnected" />
          <CircleClose v-else-if="hasError" />
          <Loading v-else />
        </el-icon>
        {{ connectionStatusText }}
      </el-tag>
    </div>
    
    <div v-if="progressUpdates.length > 0" class="progress-list">
      <TaskProgress
        v-for="update in progressUpdates"
        :key="update.subtask_id"
        :task-name="update.subtask_name"
        :agent-name="update.agent_name"
        :progress="update.progress"
        :status="update.status"
        :updated-at="update.updated_at"
      />
    </div>
    
    <div v-else class="empty-progress">
      <el-empty description="暂无进度更新" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  CircleCheck,
  CircleClose,
  Loading,
} from '@element-plus/icons-vue'
import TaskProgress from './TaskProgress.vue'

const props = defineProps({
  isConnected: {
    type: Boolean,
    default: false,
  },
  hasError: {
    type: Boolean,
    default: false,
  },
  errorMessage: {
    type: String,
    default: '',
  },
  progressUpdates: {
    type: Array,
    default: () => [],
  },
})

const connectionStatusType = computed(() => {
  if (props.isConnected) return 'success'
  if (props.hasError) return 'danger'
  return 'info'
})

const connectionStatusText = computed(() => {
  if (props.isConnected) return '实时连接中'
  if (props.hasError) return '连接失败'
  return '连接中...'
})
</script>

<style scoped>
.websocket-progress {
  padding: 16px;
}

.connection-status {
  margin-bottom: 16px;
  display: flex;
  justify-content: flex-end;
}

.status-icon {
  margin-right: 4px;
  animation: none;
}

.status-icon svg {
  animation: none;
}

.status-icon:has(svg[name='loading']) {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.progress-list {
  max-height: 400px;
  overflow-y: auto;
}

.empty-progress {
  padding: 40px 0;
}
</style>
