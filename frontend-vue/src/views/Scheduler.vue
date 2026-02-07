<template>
  <Layout>
    <div class="scheduler">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1 class="page-title">
          <el-icon class="title-icon"><Timer /></el-icon>
          故事创作调度
        </h1>
        <p class="page-subtitle">智能协调系统，为您的故事创作任务提供高效的智能体协作方案</p>
      </div>

      <!-- 调度表单 -->
      <el-card class="form-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Promotion /></el-icon>
            <span>故事创作计划</span>
          </div>
        </template>

        <el-form
          ref="formRef"
          :model="formData"
          :rules="formRules"
          label-position="top"
          class="scheduler-form"
        >
          <!-- 故事描述 -->
          <el-form-item label="故事详细描述" prop="story_description">
            <template #label>
              <div class="form-label">
                <el-icon><Document /></el-icon>
                <span>故事详细描述</span>
              </div>
            </template>
            <el-input
              v-model="formData.story_description"
              type="textarea"
              :rows="6"
              placeholder="请详细描述您想要创作的故事内容"
              class="story-textarea"
            />
            <div class="form-tip">详细的描述将帮助智能体更好地理解您的创作意图</div>
          </el-form-item>

          <!-- 故事类型 -->
          <el-form-item label="故事类型" prop="story_type">
            <template #label>
              <div class="form-label">
                <el-icon><Document /></el-icon>
                <span>故事类型</span>
              </div>
            </template>
            <el-select
              v-model="formData.story_type"
              placeholder="请选择故事类型"
              class="w-full"
            >
              <el-option
                v-for="type in storyTypes"
                :key="type.value"
                :label="type.label"
                :value="type.value"
              />
            </el-select>
          </el-form-item>

          <!-- 调度参数 -->
          <div class="param-section">
            <h3 class="param-title">调度参数</h3>
            
            <el-row :gutter="20">
              <el-col :xs="24" :sm="12">
                <el-form-item label="模型选择" prop="model">
                  <template #label>
                    <div class="form-label">
                      <el-icon><Setting /></el-icon>
                      <span>模型选择</span>
                    </div>
                  </template>
                  <el-select v-model="formData.model" class="w-full">
                    <el-option label="Qwen3-30B" value="qwen3-30b" />
                    <el-option label="DeepSeek Chat" value="deepseek-chat" />
                    <el-option label="GPT-4" value="gpt-4" />
                  </el-select>
                </el-form-item>
              </el-col>
              
              <el-col :xs="24" :sm="12">
                <el-form-item label="优先级" prop="request_priority">
                  <el-select v-model="formData.request_priority" class="w-full">
                    <el-option label="低" :value="1" />
                    <el-option label="中低" :value="2" />
                    <el-option label="中" :value="3" />
                    <el-option label="中高" :value="4" />
                    <el-option label="高" :value="5" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="会话ID" prop="session_id">
              <el-input v-model="formData.session_id" readonly class="session-input" />
            </el-form-item>
          </div>

          <!-- 提交按钮 -->
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="submit-btn"
              @click="handleSubmit"
            >
              <el-icon><Promotion /></el-icon>
              <span>开始调度</span>
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 实时进度显示（加载中） -->
      <el-card v-if="loading" class="progress-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <el-icon class="rotating"><Refresh /></el-icon>
              <span>实时调度进度</span>
              <el-tag :type="wsConnected ? 'success' : 'danger'" size="small">
                {{ wsConnected ? '实时连接' : '无实时连接' }}
              </el-tag>
            </div>
          </div>
        </template>

        <div class="progress-content">
          <!-- 整体进度条 -->
          <div class="overall-progress">
            <div class="progress-label">
              <span>整体进度</span>
              <span class="progress-value">{{ progress }}%</span>
            </div>
            <el-progress
              :percentage="progress"
              :status="progress >= 100 ? 'success' : ''"
              :stroke-width="20"
              class="main-progress"
            />
          </div>

          <!-- 智能体状态卡片 -->
          <div class="agent-cards">
            <h4 class="section-title">智能体状态</h4>
            <el-row :gutter="16">
              <el-col :xs="24" :sm="8">
                <el-card class="agent-card" shadow="never">
                  <div class="agent-header">
                    <div class="agent-icon purple">
                      <el-icon><User /></el-icon>
                    </div>
                    <div class="agent-info">
                      <div class="agent-name">创意智能体</div>
                      <div class="agent-desc">负责创意构思与大纲设计</div>
                    </div>
                  </div>
                  <el-progress
                    :percentage="progress > 50 ? 100 : progress * 2"
                    :status="progress > 50 ? 'success' : ''"
                    size="small"
                  />
                  <div class="agent-status-text">
                    {{ progress < 25 ? '待开始' : progress < 50 ? '进行中' : '已完成' }}
                  </div>
                </el-card>
              </el-col>
              
              <el-col :xs="24" :sm="8">
                <el-card class="agent-card" shadow="never">
                  <div class="agent-header">
                    <div class="agent-icon blue">
                      <el-icon><Document /></el-icon>
                    </div>
                    <div class="agent-info">
                      <div class="agent-name">剧本智能体</div>
                      <div class="agent-desc">负责细节描写与场景渲染</div>
                    </div>
                  </div>
                  <el-progress
                    :percentage="progress > 75 ? 100 : progress > 50 ? (progress - 50) * 4 : 0"
                    :status="progress > 75 ? 'success' : ''"
                    size="small"
                  />
                  <div class="agent-status-text">
                    {{ progress < 50 ? '待开始' : progress < 75 ? '进行中' : '已完成' }}
                  </div>
                </el-card>
              </el-col>
              
              <el-col :xs="24" :sm="8">
                <el-card class="agent-card" shadow="never">
                  <div class="agent-header">
                    <div class="agent-icon indigo">
                      <el-icon><Timer /></el-icon>
                    </div>
                    <div class="agent-info">
                      <div class="agent-name">调度智能体</div>
                      <div class="agent-desc">负责任务协调与资源分配</div>
                    </div>
                  </div>
                  <el-progress
                    :percentage="progress"
                    :status="progress === 100 ? 'success' : ''"
                    size="small"
                  />
                  <div class="agent-status-text">
                    {{ progress < 100 ? '进行中' : '已完成' }}
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>

          <!-- 任务时间线 -->
          <div class="task-timeline">
            <h4 class="section-title">任务执行时间线</h4>
            <el-timeline>
              <el-timeline-item
                v-for="(item, index) in timelineItems"
                :key="index"
                :type="item.type"
                :icon="item.icon"
              >
                {{ item.content }}
              </el-timeline-item>
            </el-timeline>
          </div>

          <!-- 状态信息 -->
          <div class="status-info">
            <el-alert
              :title="statusText"
              :type="progress === 100 ? 'success' : 'info'"
              :closable="false"
              center
            />
          </div>
        </div>
      </el-card>

      <!-- 调度结果 -->
      <template v-if="showResult && schedulerResult">
        <!-- 实时任务进度 -->
        <el-card class="result-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Cloudy /></el-icon>
              <span>实时任务进度</span>
            </div>
          </template>
          <WebSocketProgress
            :is-connected="wsConnected"
            :has-error="!!wsError"
            :error-message="wsError"
            :progress-updates="progressUpdates"
          />
        </el-card>

        <!-- 调度结果 -->
        <el-card class="result-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><DataLine /></el-icon>
              <span>调度结果</span>
            </div>
          </template>

          <div class="result-content">
            <!-- 状态提示 -->
            <el-alert
              :title="`调度状态: ${schedulerResult.result_summary.status === 'completed' ? '已完成' : '进行中'}`"
              :type="schedulerResult.result_summary.status === 'completed' ? 'success' : 'info'"
              show-icon
              class="status-alert"
            />

            <el-divider />

            <!-- 任务概览 -->
            <div class="overview-section">
              <h4 class="section-title">任务概览</h4>
              <el-descriptions :column="2" border>
                <el-descriptions-item label="故事类型">
                  {{ schedulerResult.task_plan.story_type }}
                </el-descriptions-item>
                <el-descriptions-item label="总体进度">
                  {{ schedulerResult.progress_tracking.overall_progress }}%
                </el-descriptions-item>
                <el-descriptions-item label="已完成任务">
                  {{ schedulerResult.result_summary.completed_tasks }}/{{ schedulerResult.result_summary.total_tasks }}
                </el-descriptions-item>
                <el-descriptions-item label="预计工作量">
                  {{ schedulerResult.task_plan.estimated_duration }}分钟
                </el-descriptions-item>
              </el-descriptions>
            </div>

            <el-divider />

            <!-- 智能体分配 -->
            <div class="allocation-section">
              <h4 class="section-title">智能体分配</h4>
              <el-table :data="allocations" style="width: 100%" border>
                <el-table-column prop="subtask_id" label="任务ID" width="120" />
                <el-table-column prop="subtask_name" label="任务名称" />
                <el-table-column prop="agent_name" label="智能体" width="120">
                  <template #default="{ row }">
                    <el-tag :type="row.agent_name.includes('创意') ? 'purple' : 'primary'">
                      {{ row.agent_name }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="estimated_duration" label="预计时长" width="100">
                  <template #default="{ row }">
                    {{ row.estimated_duration }}分钟
                  </template>
                </el-table-column>
                <el-table-column prop="priority" label="优先级" width="80">
                  <template #default="{ row }">
                    <el-tag :type="getPriorityType(row.priority)">
                      {{ row.priority }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </div>

            <el-divider />

            <!-- 进度跟踪 -->
            <div class="tracking-section">
              <h4 class="section-title">进度跟踪</h4>
              <el-table :data="progressUpdates" style="width: 100%" border>
                <el-table-column prop="subtask_name" label="任务名称" />
                <el-table-column prop="agent_name" label="智能体" width="120" />
                <el-table-column prop="progress" label="进度" width="150">
                  <template #default="{ row }">
                    <el-progress :percentage="row.progress" size="small" />
                  </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" width="100">
                  <template #default="{ row }">
                    <el-tag :type="getStatusType(row.status)">
                      {{ getStatusText(row.status) }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </div>

            <el-divider />

            <!-- 关键成果 -->
            <div class="achievements-section">
              <h4 class="section-title">关键成果</h4>
              <div class="achievements-list">
                <div
                  v-for="(achievement, index) in schedulerResult.result_summary.key_achievements"
                  :key="index"
                  class="achievement-item"
                >
                  <el-icon class="achievement-icon" color="#67c23a"><CircleCheck /></el-icon>
                  <span>{{ achievement }}</span>
                </div>
              </div>
            </div>

            <!-- 下一步 -->
            <div class="next-steps-section">
              <h4 class="section-title">下一步</h4>
              <div class="next-steps-list">
                <div
                  v-for="(step, index) in schedulerResult.result_summary.next_steps"
                  :key="index"
                  class="next-step-item"
                >
                  <el-icon class="step-icon" color="#409eff"><ArrowRight /></el-icon>
                  <span>{{ step }}</span>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </template>
    </div>
  </Layout>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElNotification } from 'element-plus'
import {
  Timer,
  Promotion,
  Document,
  Setting,
  Refresh,
  User,
  DataLine,
  Cloudy,
  CircleCheck,
  ArrowRight,
} from '@element-plus/icons-vue'
import Layout from '@/components/layout/Layout.vue'
import WebSocketProgress from '@/components/progress/WebSocketProgress.vue'
import api from '@/services/api'
import endpoints from '@/services/endpoints'

// 表单引用
const formRef = ref(null)

// 加载状态
const loading = ref(false)
const showResult = ref(false)

// 进度相关
const progress = ref(0)
const progressUpdates = ref([])
const allocations = ref([])

// WebSocket相关
const websocket = ref(null)
const wsConnected = ref(false)
const wsError = ref(null)
const sessionIdRef = ref('')

// 调度结果
const schedulerResult = ref(null)

// 故事类型选项
const storyTypes = [
  { value: '科幻', label: '科幻' },
  { value: '悬疑', label: '悬疑' },
  { value: '爱情', label: '爱情' },
  { value: '奇幻', label: '奇幻' },
  { value: '历史', label: '历史' },
  { value: '都市', label: '都市' },
  { value: '武侠', label: '武侠' },
  { value: '恐怖', label: '恐怖' },
]

// 表单数据
const formData = reactive({
  story_description: '',
  story_type: '历史',
  request_priority: 3,
  model: 'qwen3-30b',
  session_id: '',
})

// 表单验证规则
const formRules = {
  story_description: [
    { required: true, message: '请输入故事详细描述', trigger: 'blur' },
    { whitespace: true, message: '内容不能为空', trigger: 'blur' },
  ],
  story_type: [
    { required: true, message: '请选择故事类型', trigger: 'change' },
  ],
}

// 时间线项目
const timelineItems = computed(() => [
  { content: '开始处理调度请求', type: progress.value > 0 ? 'success' : '', icon: progress.value > 0 ? CircleCheck : '' },
  { content: '执行任务规划', type: progress.value > 20 ? 'success' : progress.value > 0 ? 'primary' : '', icon: progress.value > 20 ? CircleCheck : '' },
  { content: '执行任务分解', type: progress.value > 40 ? 'success' : progress.value > 20 ? 'primary' : '', icon: progress.value > 40 ? CircleCheck : '' },
  { content: '执行智能体分配', type: progress.value > 60 ? 'success' : progress.value > 40 ? 'primary' : '', icon: progress.value > 60 ? CircleCheck : '' },
  { content: '执行工作流', type: progress.value > 80 ? 'success' : progress.value > 60 ? 'primary' : '', icon: progress.value > 80 ? CircleCheck : '' },
  { content: '生成执行报告', type: progress.value > 90 ? 'success' : progress.value > 80 ? 'primary' : '', icon: progress.value > 90 ? CircleCheck : '' },
  { content: '任务完成', type: progress.value === 100 ? 'success' : progress.value > 90 ? 'primary' : '', icon: progress.value === 100 ? CircleCheck : '' },
])

// 状态文本
const statusText = computed(() => {
  if (progress.value < 20) return '正在初始化调度系统...'
  if (progress.value < 40) return '正在规划故事创作任务...'
  if (progress.value < 60) return '正在分解任务并分配智能体...'
  if (progress.value < 80) return '正在执行工作流...'
  if (progress.value < 100) return '正在生成执行报告...'
  return '任务调度已完成！'
})

// 生成会话ID
const generateSessionId = () => {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

// WebSocket连接
const connectWebSocket = (sessionId) => {
  try {
    // 关闭现有连接
    if (websocket.value) {
      websocket.value.close()
    }

    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${wsProtocol}//${window.location.host}/api/scheduler/ws/${sessionId}`

    const ws = new WebSocket(wsUrl)
    websocket.value = ws

    ws.onopen = () => {
      console.log('WebSocket连接已建立')
      wsConnected.value = true
      wsError.value = null
      ElNotification.success({
        title: '实时连接已建立',
        message: '您将实时收到任务执行进度更新',
        duration: 3000,
      })
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('收到WebSocket消息:', data)
        handleProgressUpdate(data)
      } catch (error) {
        console.error('解析WebSocket消息失败:', error)
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket错误:', error)
      wsError.value = 'WebSocket连接错误'
      ElNotification.error({
        title: '实时连接错误',
        message: '无法建立实时连接，将使用轮询获取进度',
        duration: 3000,
      })
    }

    ws.onclose = () => {
      console.log('WebSocket连接已关闭')
      wsConnected.value = false
      websocket.value = null
    }
  } catch (error) {
    console.error('建立WebSocket连接失败:', error)
    wsError.value = '无法建立WebSocket连接'
  }
}

// 关闭WebSocket连接
const disconnectWebSocket = () => {
  if (websocket.value) {
    websocket.value.close()
    websocket.value = null
    wsConnected.value = false
  }
}

// 处理进度更新
const handleProgressUpdate = (data) => {
  if (data.overall_progress !== undefined) {
    progress.value = data.overall_progress
  }

  if (data.updates && Array.isArray(data.updates)) {
    progressUpdates.value = data.updates
  }

  if (data.status) {
    switch (data.status) {
      case 'completed':
        ElNotification.success({
          title: '任务完成',
          message: '所有任务已成功完成',
          duration: 3000,
        })
        break
      case 'failed':
        ElNotification.error({
          title: '任务失败',
          message: data.message || '任务执行失败',
          duration: 3000,
        })
        break
      case 'running':
        if (data.message) {
          ElNotification.info({
            title: '任务执行中',
            message: data.message,
            duration: 2000,
          })
        }
        break
    }
  }
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    completed: 'success',
    in_progress: 'primary',
    pending: 'info',
    failed: 'danger',
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    completed: '已完成',
    in_progress: '进行中',
    pending: '待开始',
    failed: '失败',
  }
  return texts[status] || status
}

// 获取优先级类型
const getPriorityType = (priority) => {
  if (priority >= 4) return 'danger'
  if (priority >= 3) return 'warning'
  return 'primary'
}

// 模拟进度增长
const simulateProgress = () => {
  const interval = setInterval(() => {
    if (progress.value < 100 && loading.value) {
      progress.value += Math.random() * 15
      if (progress.value > 100) progress.value = 100
    } else {
      clearInterval(interval)
    }
  }, 1000)
}

// 处理表单提交
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  showResult.value = false
  progress.value = 0

  // 保存会话ID
  sessionIdRef.value = formData.session_id

  // 建立WebSocket连接
  connectWebSocket(formData.session_id)

  // 开始模拟进度
  simulateProgress()

  try {
    // 真实API调用
    const response = await api.post(endpoints.scheduler.schedule, {
      story_description: formData.story_description,
      story_type: formData.story_type,
      request_priority: formData.request_priority,
      session_id: formData.session_id,
      model: formData.model,
    })

    const result = {
      response: response.response || '故事创作任务调度成功',
      session_id: response.session_id || formData.session_id,
      task_plan: response.task_plan || {
        story_type: formData.story_type,
        plan: `为${formData.story_type}故事创建完整的创作计划，包括创意构思、情节设计、人物塑造和结局安排`,
        estimated_duration: 120,
      },
      task_breakdown: response.task_breakdown || { subtasks: [] },
      agent_allocation: response.agent_allocation || { allocations: [] },
      progress_tracking: response.progress_tracking || {
        progress_updates: [],
        overall_progress: 0,
      },
      result_summary: response.result_summary || {
        overall_progress: 0,
        status: 'in_progress',
        completed_tasks: 0,
        total_tasks: 0,
        summary: '任务调度中',
        key_achievements: [],
        next_steps: [],
      },
    }

    schedulerResult.value = result
    progressUpdates.value = result.progress_tracking.progress_updates
    allocations.value = result.agent_allocation.allocations
    showResult.value = true
    ElMessage.success('故事创作任务调度成功！')
  } catch (error) {
    console.error('调度任务失败:', error)
    ElMessage.error('调度任务失败，请重试')

    // 使用模拟数据
    const mockResult = {
      response: '故事创作任务调度成功',
      session_id: formData.session_id,
      task_plan: {
        story_type: formData.story_type,
        plan: `为${formData.story_type}故事创建完整的创作计划`,
        estimated_duration: 120,
      },
      task_breakdown: {
        subtasks: [
          { subtask_id: 'subtask_1', name: '创意构思与大纲设计', description: '设计故事大纲', estimated_duration: 30, agent_type: 'creative', priority: 1 },
          { subtask_id: 'subtask_2', name: '人物设定与关系构建', description: '设计人物关系', estimated_duration: 25, agent_type: 'creative', priority: 2 },
          { subtask_id: 'subtask_3', name: '情节发展与冲突设计', description: '设计情节冲突', estimated_duration: 40, agent_type: 'creative', priority: 3 },
          { subtask_id: 'subtask_4', name: '细节描写与场景渲染', description: '场景渲染', estimated_duration: 35, agent_type: 'script', priority: 4 },
          { subtask_id: 'subtask_5', name: '结局设计与主题升华', description: '设计结局', estimated_duration: 30, agent_type: 'script', priority: 5 },
        ],
      },
      agent_allocation: {
        allocations: [
          { subtask_id: 'subtask_1', subtask_name: '创意构思与大纲设计', agent_type: 'creative', agent_name: '创意智能体', estimated_duration: 30, priority: 1 },
          { subtask_id: 'subtask_2', subtask_name: '人物设定与关系构建', agent_type: 'creative', agent_name: '创意智能体', estimated_duration: 25, priority: 2 },
          { subtask_id: 'subtask_3', subtask_name: '情节发展与冲突设计', agent_type: 'creative', agent_name: '创意智能体', estimated_duration: 40, priority: 3 },
          { subtask_id: 'subtask_4', subtask_name: '细节描写与场景渲染', agent_type: 'script', agent_name: '剧本智能体', estimated_duration: 35, priority: 4 },
          { subtask_id: 'subtask_5', subtask_name: '结局设计与主题升华', agent_type: 'script', agent_name: '剧本智能体', estimated_duration: 30, priority: 5 },
        ],
      },
      progress_tracking: {
        progress_updates: [
          { subtask_id: 'subtask_1', subtask_name: '创意构思与大纲设计', agent_name: '创意智能体', progress: 100, status: 'completed' },
          { subtask_id: 'subtask_2', subtask_name: '人物设定与关系构建', agent_name: '创意智能体', progress: 100, status: 'completed' },
          { subtask_id: 'subtask_3', subtask_name: '情节发展与冲突设计', agent_name: '创意智能体', progress: 80, status: 'in_progress' },
          { subtask_id: 'subtask_4', subtask_name: '细节描写与场景渲染', agent_name: '剧本智能体', progress: 30, status: 'in_progress' },
          { subtask_id: 'subtask_5', subtask_name: '结局设计与主题升华', agent_name: '剧本智能体', progress: 0, status: 'pending' },
        ],
        overall_progress: 62,
      },
      result_summary: {
        overall_progress: 62,
        status: 'in_progress',
        completed_tasks: 2,
        total_tasks: 5,
        summary: '任务已完成62%，共完成2个任务，总计5个任务',
        key_achievements: ['完成故事大纲设计', '构建主要人物关系', '设计核心情节冲突', '渲染关键场景细节'],
        next_steps: ['完成剩余任务', '整合所有内容', '进行质量评估', '提交最终结果'],
      },
    }

    schedulerResult.value = mockResult
    progressUpdates.value = mockResult.progress_tracking.progress_updates
    allocations.value = mockResult.agent_allocation.allocations
    showResult.value = true
    progress.value = 62
    ElMessage.success('故事创作任务调度成功（模拟数据）！')
  } finally {
    loading.value = false
  }
}

// 组件挂载时生成会话ID
onMounted(() => {
  formData.session_id = generateSessionId()
})

// 组件卸载时关闭WebSocket
onUnmounted(() => {
  disconnectWebSocket()
})
</script>

<style scoped>
.scheduler {
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

.title-icon {
  color: #6366f1;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.page-subtitle {
  font-size: 14px;
  color: #8c8c8c;
}

.form-card,
.progress-card,
.result-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.scheduler-form {
  max-width: 800px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-tip {
  font-size: 12px;
  color: #8c8c8c;
  margin-top: 8px;
}

.w-full {
  width: 100%;
}

.param-section {
  margin: 24px 0;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.param-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 16px;
  color: #262626;
}

.session-input {
  background-color: #f5f7fa;
}

.submit-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  border: none;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

/* 进度卡片样式 */
.progress-content {
  padding: 20px 0;
}

.overall-progress {
  margin-bottom: 24px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-weight: 500;
}

.progress-value {
  font-size: 20px;
  color: #6366f1;
}

.main-progress :deep(.el-progress-bar__outer) {
  border-radius: 10px;
}

.main-progress :deep(.el-progress-bar__inner) {
  border-radius: 10px;
  background: linear-gradient(90deg, #6366f1 0%, #4f46e5 100%);
}

.agent-cards {
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 16px;
  color: #262626;
}

.agent-card {
  margin-bottom: 16px;
}

.agent-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.agent-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.agent-icon.purple {
  background-color: #f3e8ff;
  color: #9333ea;
}

.agent-icon.blue {
  background-color: #dbeafe;
  color: #2563eb;
}

.agent-icon.indigo {
  background-color: #e0e7ff;
  color: #4f46e5;
}

.agent-name {
  font-weight: 500;
  color: #262626;
}

.agent-desc {
  font-size: 12px;
  color: #8c8c8c;
}

.agent-status-text {
  margin-top: 8px;
  font-size: 12px;
  color: #8c8c8c;
}

.task-timeline {
  margin-bottom: 24px;
}

.status-info {
  margin-top: 24px;
}

/* 结果卡片样式 */
.result-content {
  padding: 20px 0;
}

.status-alert {
  margin-bottom: 16px;
}

.overview-section,
.allocation-section,
.tracking-section,
.achievements-section,
.next-steps-section {
  margin-bottom: 24px;
}

.achievements-list,
.next-steps-list {
  background-color: #f0f9ff;
  border-radius: 8px;
  padding: 16px;
}

.achievement-item,
.next-step-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
}

.achievement-icon,
.step-icon {
  font-size: 18px;
}

/* 旋转动画 */
.rotating {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 响应式 */
@media (max-width: 768px) {
  .scheduler {
    padding: 12px;
  }
  
  .page-title {
    font-size: 20px;
  }
}
</style>
