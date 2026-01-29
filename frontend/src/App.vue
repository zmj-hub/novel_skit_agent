<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <Header 
      @start-execution="startExecution"
      @stop-execution="stopExecution"
    />
    
    <!-- 主内容区 -->
    <main class="container mx-auto px-4 py-6">
      <!-- 三列布局 -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <!-- 左侧边栏 (3列) - 状态概览和智能体状态 -->
        <div class="lg:col-span-3 space-y-6">
          <StatusOverview 
            :data="monitoringData"
            :loading="loading"
          />
          <AgentStatus 
            :agents="agentStatuses"
            :loading="loading"
          />
        </div>
        
        <!-- 中间内容区 (5列) - 执行历史 -->
        <div class="lg:col-span-5">
          <ExecutionHistory 
            :history="executionHistory"
            :loading="loading"
            @select="selectWorkflow"
          />
        </div>
        
        <!-- 右侧详情区 (4列) - 工作流详情 -->
        <div class="lg:col-span-4">
          <WorkflowDetails 
            :workflow-id="selectedWorkflowId"
            :steps="workflowSteps"
            :loading="loadingDetails"
          />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Header from './components/Header.vue'
import StatusOverview from './components/StatusOverview.vue'
import AgentStatus from './components/AgentStatus.vue'
import ExecutionHistory from './components/ExecutionHistory.vue'
import WorkflowDetails from './components/WorkflowDetails.vue'

// 状态数据
const monitoringData = ref({})
const agentStatuses = ref({})
const executionHistory = ref([])
const workflowSteps = ref([])
const selectedWorkflowId = ref('')
const loading = ref(false)
const loadingDetails = ref(false)

// 获取监控数据
const fetchMonitoringData = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/monitoring/data')
    if (response.ok) {
      const data = await response.json()
      monitoringData.value = data
      agentStatuses.value = data.agentStatuses || {}
      executionHistory.value = data.executionHistory || []
    }
  } catch (error) {
    console.error('获取监控数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取工作流详情
const fetchWorkflowDetails = async (taskId) => {
  if (!taskId) return
  
  loadingDetails.value = true
  try {
    const response = await fetch(`/api/monitoring/workflow/${taskId}`)
    if (response.ok) {
      const data = await response.json()
      workflowSteps.value = data.steps || []
    }
  } catch (error) {
    console.error('获取工作流详情失败:', error)
  } finally {
    loadingDetails.value = false
  }
}

// 选择工作流
const selectWorkflow = (taskId) => {
  selectedWorkflowId.value = taskId
  fetchWorkflowDetails(taskId)
}

// 启动执行
const startExecution = () => {
  console.log('启动执行')
  // TODO: 实现启动执行逻辑
}

// 停止执行
const stopExecution = () => {
  console.log('停止执行')
  // TODO: 实现停止执行逻辑
}

// 组件挂载时获取数据
onMounted(() => {
  fetchMonitoringData()
  // 定时刷新数据
  setInterval(fetchMonitoringData, 30000) // 每30秒刷新一次
})
</script>

<style>
/* 全局样式 */
/* 使用系统字体栈，避免Google Fonts依赖 */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* 选中文字样式 */
::selection {
  background: #3b82f6;
  color: white;
}
</style>