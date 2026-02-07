<template>
  <el-card class="stat-card" :body-style="{ padding: '20px' }">
    <div class="stat-content">
      <div class="stat-icon" :style="{ backgroundColor: iconBgColor }">
        <el-icon :size="24" :color="iconColor">
          <component :is="icon" />
        </el-icon>
      </div>
      <div class="stat-info">
        <div class="stat-value" :style="{ color: valueColor }">
          {{ prefix }}{{ value }}{{ suffix }}
        </div>
        <div class="stat-title">{{ title }}</div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [Number, String],
    required: true,
  },
  icon: {
    type: String,
    required: true,
  },
  iconBgColor: {
    type: String,
    default: '#e6f7ff',
  },
  iconColor: {
    type: String,
    default: '#1890ff',
  },
  valueColor: {
    type: String,
    default: '#262626',
  },
  prefix: {
    type: String,
    default: '',
  },
  suffix: {
    type: String,
    default: '',
  },
})
</script>

<style scoped>
.stat-card {
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  line-height: 1.2;
}

.stat-title {
  font-size: 14px;
  color: #8c8c8c;
  margin-top: 4px;
}
</style>
