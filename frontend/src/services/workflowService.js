import { apiService } from './api'
import { API_ENDPOINTS } from './endpoints'

// 工作流服务
export const workflowService = {
  /**
   * 启动工作流执行
   * @param {Object} params 执行参数
   * @param {string} params.task_goal 任务目标
   * @param {string} params.session_id 会话ID
   * @param {string} params.model 模型名称
   * @param {number} params.timeout 超时时间
   * @param {number} params.priority 优先级
   * @returns {Promise<Object>} 执行结果
   */
  async startExecution(params) {
    try {
      const data = await apiService.post(API_ENDPOINTS.WORKFLOW.COLLABORATE, params)
      return data
    } catch (error) {
      console.error('启动执行失败:', error)
      throw error
    }
  },

  /**
   * 停止工作流执行
   * @param {string} sessionId 会话ID
   * @returns {Promise<Object>} 执行结果
   */
  async stopExecution(sessionId) {
    try {
      const data = await apiService.post(API_ENDPOINTS.WORKFLOW.CANCEL(sessionId))
      return data
    } catch (error) {
      console.error('停止执行失败:', error)
      throw error
    }
  }
}

export default workflowService