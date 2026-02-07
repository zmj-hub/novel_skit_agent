import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import endpoints from '@/services/endpoints'

export const useChatStore = defineStore('chat', () => {
  // State
  const messages = ref([])
  const sessions = ref([])
  const currentSession = ref(null)
  const loading = ref(false)
  const useKnowledge = ref(false)
  const selectedModel = ref('qwen3-30b')
  
  // Actions
  async function fetchSessions() {
    try {
      const data = await api.get(endpoints.chat.sessions)
      sessions.value = data
      return data
    } catch (error) {
      console.error('获取会话列表失败:', error)
      throw error
    }
  }
  
  async function fetchHistory(sessionId) {
    try {
      const data = await api.get(`${endpoints.chat.history}/${sessionId}`)
      messages.value = data.messages || []
      return data
    } catch (error) {
      console.error('获取聊天历史失败:', error)
      throw error
    }
  }
  
  async function sendMessage(message) {
    loading.value = true
    try {
      // 添加用户消息
      messages.value.push({
        role: 'user',
        content: message,
        timestamp: new Date().toISOString(),
      })
      
      const data = await api.post(endpoints.chat.send, {
        message,
        session_id: currentSession.value?.id,
        use_knowledge: useKnowledge.value,
        model: selectedModel.value,
      })
      
      // 添加助手回复
      messages.value.push({
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString(),
      })
      
      return data
    } catch (error) {
      console.error('发送消息失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }
  
  function setCurrentSession(session) {
    currentSession.value = session
  }
  
  function toggleKnowledge() {
    useKnowledge.value = !useKnowledge.value
  }
  
  function setModel(model) {
    selectedModel.value = model
  }
  
  function clearMessages() {
    messages.value = []
  }
  
  return {
    messages,
    sessions,
    currentSession,
    loading,
    useKnowledge,
    selectedModel,
    fetchSessions,
    fetchHistory,
    sendMessage,
    setCurrentSession,
    toggleKnowledge,
    setModel,
    clearMessages,
  }
})
