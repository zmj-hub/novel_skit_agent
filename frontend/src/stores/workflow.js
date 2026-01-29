import { defineStore } from 'pinia'
import { workflowService } from '../services/workflowService'

export const useWorkflowStore = defineStore('workflow', {
  state: () => ({
    executionParams: {
      taskGoal: '生成一个关于人工智能的故事创意，并创作故事剧本',
      sessionId: 'user_' + Math.random().toString(36).substr(2, 9),
      model: 'qwen3-30b-a3b',
      timeout: 300,
      priority: 3,
      writingStyle: 'urban',
      mediumType: 'novel',
      chapterCount: 5,
      models: {
        creative: 'qwen3-30b-a3b',
        story_script: 'qwen3-30b-a3b',
        coordination: 'qwen3-30b-a3b'
      }
    },
    isExecuting: false,
    executionError: null,
    executionSuccess: null
  }),

  getters: {
    getExecutionParams: (state) => {
      return state.executionParams
    },
    isExecutionInProgress: (state) => {
      return state.isExecuting
    }
  },

  actions: {
    updateExecutionParams(params) {
      this.executionParams = { ...this.executionParams, ...params }
    },

    resetExecutionMessages() {
      this.executionError = null
      this.executionSuccess = null
    },

    async startExecution() {
      try {
        this.isExecuting = true
        this.executionError = null
        this.executionSuccess = null
        
        const response = await workflowService.startExecution({
          task_goal: this.executionParams.taskGoal,
          session_id: this.executionParams.sessionId,
          model: this.executionParams.model,
          timeout: this.executionParams.timeout,
          priority: this.executionParams.priority,
          writing_style: this.executionParams.writingStyle,
          medium_type: this.executionParams.mediumType,
          chapter_count: this.executionParams.chapterCount,
          models: this.executionParams.models
        })
        
        this.executionSuccess = '执行已启动'
        return true
      } catch (error) {
        console.error('启动执行失败:', error)
        this.executionError = error.message || '启动执行失败'
        return false
      } finally {
        this.isExecuting = false
      }
    },

    async stopExecution() {
      try {
        this.isExecuting = true
        this.executionError = null
        this.executionSuccess = null
        
        const response = await workflowService.stopExecution(this.executionParams.sessionId)
        
        this.executionSuccess = '执行已停止'
        return true
      } catch (error) {
        console.error('停止执行失败:', error)
        this.executionError = error.message || '停止执行失败'
        return false
      } finally {
        this.isExecuting = false
      }
    }
  }
})