import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import endpoints from '@/services/endpoints'

export const useSchedulerStore = defineStore('scheduler', () => {
  // State
  const schedulerResult = ref(null)
  const progressUpdates = ref([])
  const allocations = ref([])
  const loading = ref(false)
  const progress = ref(0)
  const websocket = ref(null)
  const wsConnected = ref(false)
  const wsError = ref(null)

  // Actions
  async function scheduleTask(taskData) {
    loading.value = true
    try {
      const data = await api.post(endpoints.scheduler.schedule, taskData)
      schedulerResult.value = data
      progressUpdates.value = data.progress_tracking?.progress_updates || []
      allocations.value = data.agent_allocation?.allocations || []
      return data
    } catch (error) {
      console.error('调度任务失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  function connectWebSocket(sessionId) {
    try {
      // 关闭现有连接
      if (websocket.value) {
        websocket.value.close()
      }

      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const wsUrl = `${wsProtocol}//${window.location.host}${endpoints.scheduler.ws(sessionId)}`

      const ws = new WebSocket(wsUrl)
      websocket.value = ws

      ws.onopen = () => {
        console.log('WebSocket连接已建立')
        wsConnected.value = true
        wsError.value = null
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          handleProgressUpdate(data)
        } catch (error) {
          console.error('解析WebSocket消息失败:', error)
        }
      }

      ws.onerror = (error) => {
        console.error('WebSocket错误:', error)
        wsError.value = 'WebSocket连接错误'
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

  function disconnectWebSocket() {
    if (websocket.value) {
      websocket.value.close()
      websocket.value = null
      wsConnected.value = false
    }
  }

  function handleProgressUpdate(data) {
    if (data.type === 'progress_update') {
      const index = progressUpdates.value.findIndex(
        (item) => item.subtask_id === data.subtask_id
      )
      if (index !== -1) {
        progressUpdates.value[index] = { ...progressUpdates.value[index], ...data }
      } else {
        progressUpdates.value.push(data)
      }

      // 更新总体进度
      if (data.overall_progress !== undefined) {
        progress.value = data.overall_progress
      }
    }
  }

  function resetState() {
    schedulerResult.value = null
    progressUpdates.value = []
    allocations.value = []
    progress.value = 0
    disconnectWebSocket()
  }

  return {
    schedulerResult,
    progressUpdates,
    allocations,
    loading,
    progress,
    websocket,
    wsConnected,
    wsError,
    scheduleTask,
    connectWebSocket,
    disconnectWebSocket,
    handleProgressUpdate,
    resetState,
  }
})
