<template>
  <div v-if="fullscreen" class="loading-fullscreen">
    <el-icon class="loading-icon" :size="48"><Loading /></el-icon>
    <p v-if="message" class="loading-message">{{ message }}</p>
  </div>
  <div v-else class="loading-inline">
    <el-icon class="loading-icon" :size="size"><Loading /></el-icon>
    <p v-if="message" class="loading-message">{{ message }}</p>
  </div>
</template>

<script setup>
import { Loading } from '@element-plus/icons-vue'

defineProps({
  fullscreen: {
    type: Boolean,
    default: false,
  },
  message: {
    type: String,
    default: '',
  },
  size: {
    type: Number,
    default: 32,
  },
})
</script>

<style scoped>
.loading-fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-inline {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.loading-icon {
  color: #409eff;
  animation: rotate 1s linear infinite;
}

.loading-message {
  margin-top: 12px;
  color: #606266;
  font-size: 14px;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
