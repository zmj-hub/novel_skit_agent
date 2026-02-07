<template>
  <Layout>
    <div class="dashboard">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1 class="page-title">
          <el-icon><DataLine /></el-icon>
          系统仪表盘
        </h1>
        <p class="page-subtitle">实时监控小说创作智能体的运行状态</p>
      </div>

      <!-- 统计卡片 -->
      <el-row :gutter="20" class="stat-cards">
        <el-col :xs="24" :sm="12" :md="6">
          <StatCard
            title="总任务数"
            :value="stats.totalTasks"
            icon="Document"
            icon-bg-color="#e6f7ff"
            icon-color="#1890ff"
          />
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <StatCard
            title="成功任务"
            :value="stats.successTasks"
            icon="CircleCheck"
            icon-bg-color="#f6ffed"
            icon-color="#52c41a"
            value-color="#52c41a"
          />
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <StatCard
            title="失败任务"
            :value="stats.failedTasks"
            icon="CircleClose"
            icon-bg-color="#fff1f0"
            icon-color="#f5222d"
            value-color="#f5222d"
          />
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <StatCard
            title="运行中"
            :value="stats.runningTasks"
            icon="Loading"
            icon-bg-color="#fff7e6"
            icon-color="#fa8c16"
            value-color="#fa8c16"
          />
        </el-col>
      </el-row>

      <!-- 智能体状态 -->
      <el-card class="agent-status-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span><el-icon><User /></el-icon> 智能体状态</span>
          </div>
        </template>
        <el-table :data="agentList" style="width: 100%">
          <el-table-column prop="name" label="智能体名称" />
          <el-table-column prop="type" label="类型">
            <template #default="{ row }">
              <el-tag :type="getAgentTypeType(row.type)">
                {{ getAgentTypeText(row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="lastActive" label="最后活跃" />
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button type="primary" link @click="viewAgentDetail(row)">
                查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 执行历史 -->
      <el-card class="history-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span><el-icon><Timer /></el-icon> 执行历史</span>
            <el-button type="primary" link @click="refreshHistory">
              <el-icon><Refresh /></el-icon>刷新
            </el-button>
          </div>
        </template>
        <el-timeline>
          <el-timeline-item
            v-for="item in executionHistory"
            :key="item.id"
            :type="getTimelineType(item.status)"
            :timestamp="item.time"
          >
            <div class="timeline-content">
              <div class="timeline-title">{{ item.title }}</div>
              <div class="timeline-desc">{{ item.description }}</div>
              <el-tag :type="getStatusType(item.status)" size="small">
                {{ getStatusText(item.status) }}
              </el-tag>
            </div>
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  DataLine,
  User,
  Timer,
  Refresh,
  Document,
  CircleCheck,
  CircleClose,
  Loading,
} from '@element-plus/icons-vue'
import Layout from '@/components/layout/Layout.vue'
import StatCard from '@/components/common/StatCard.vue'
import api from '@/services/api'
import endpoints from '@/services/endpoints'

// 统计数据
const stats = ref({
  totalTasks: 0,
  successTasks: 0,
  failedTasks: 0,
  runningTasks: 0,
})

// 智能体列表
const agentList = ref([])

// 执行历史
const executionHistory = ref([])

// 获取统计数据
const fetchStats = async () => {
  try {
    const data = await api.get(endpoints.monitoring.data)
    stats.value = {
      totalTasks: data.total_tasks || 0,
      successTasks: data.success_tasks || 0,
      failedTasks: data.failed_tasks || 0,
      runningTasks: data.running_tasks || 0,
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
    // 使用模拟数据
    stats.value = {
      totalTasks: 128,
      successTasks: 98,
      failedTasks: 5,
      runningTasks: 25,
    }
  }
}

// 获取智能体列表
const fetchAgents = async () => {
  try {
    const data = await api.get(endpoints.monitoring.agents)
    agentList.value = data || []
  } catch (error) {
    console.error('获取智能体列表失败:', error)
    // 使用模拟数据
    agentList.value = [
      { name: '创意智能体', type: 'creative', status: 'online', lastActive: '2024-01-15 10:30:00' },
      { name: '剧本智能体', type: 'script', status: 'online', lastActive: '2024-01-15 10:25:00' },
      { name: '编辑智能体', type: 'editor', status: 'busy', lastActive: '2024-01-15 10:20:00' },
      { name: '审核智能体', type: 'reviewer', status: 'offline', lastActive: '2024-01-15 09:00:00' },
    ]
  }
}

// 获取执行历史
const fetchHistory = async () => {
  try {
    const data = await api.get(endpoints.monitoring.history)
    executionHistory.value = data || []
  } catch (error) {
    console.error('获取执行历史失败:', error)
    // 使用模拟数据
    executionHistory.value = [
      { id: 1, title: '小说创作任务', description: '完成科幻小说第三章创作', status: 'completed', time: '2024-01-15 10:30:00' },
      { id: 2, title: '创意生成任务', description: '生成5个奇幻故事创意', status: 'completed', time: '2024-01-15 10:15:00' },
      { id: 3, title: '智能体协作任务', description: '多智能体协作编辑', status: 'running', time: '2024-01-15 10:00:00' },
      { id: 4, title: '知识库更新', description: '更新历史知识库', status: 'failed', time: '2024-01-15 09:45:00' },
    ]
  }
}

// 刷新历史
const refreshHistory = () => {
  fetchHistory()
}

// 查看智能体详情
const viewAgentDetail = (agent) => {
  console.log('查看智能体详情:', agent)
}

// 获取智能体类型样式
const getAgentTypeType = (type) => {
  const types = {
    creative: 'success',
    script: 'primary',
    editor: 'warning',
    reviewer: 'info',
  }
  return types[type] || 'info'
}

// 获取智能体类型文本
const getAgentTypeText = (type) => {
  const texts = {
    creative: '创意',
    script: '剧本',
    editor: '编辑',
    reviewer: '审核',
  }
  return texts[type] || type
}

// 获取状态样式
const getStatusType = (status) => {
  const types = {
    online: 'success',
    offline: 'info',
    busy: 'warning',
    error: 'danger',
    completed: 'success',
    running: 'primary',
    failed: 'danger',
    pending: 'info',
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    online: '在线',
    offline: '离线',
    busy: '忙碌',
    error: '错误',
    completed: '已完成',
    running: '进行中',
    failed: '失败',
    pending: '待处理',
  }
  return texts[status] || status
}

// 获取时间线类型
const getTimelineType = (status) => {
  const types = {
    completed: 'success',
    running: 'primary',
    failed: 'danger',
    pending: 'info',
  }
  return types[status] || 'info'
}

onMounted(() => {
  fetchStats()
  fetchAgents()
  fetchHistory()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #262626;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.page-subtitle {
  font-size: 14px;
  color: #8c8c8c;
}

.stat-cards {
  margin-bottom: 24px;
}

.agent-status-card,
.history-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 500;
}

.timeline-content {
  padding: 8px 0;
}

.timeline-title {
  font-weight: 500;
  margin-bottom: 4px;
}

.timeline-desc {
  font-size: 14px;
  color: #8c8c8c;
  margin-bottom: 8px;
}
</style>
