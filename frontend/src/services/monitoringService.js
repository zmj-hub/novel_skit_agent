import { apiService } from './api'
import { API_ENDPOINTS } from './endpoints'
import { debounce } from '../utils/appUtils'

// 监控服务
export const monitoringService = {
  /**
   * 获取监控数据
   * @returns {Promise<Object>} 监控数据
   */
  async getMonitoringData() {
    // 设置请求超时
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => {
        reject(new Error('请求超时，请检查网络连接'))
      }, 10000) // 10秒超时
    })

    try {
      // 使用 Promise.race 实现超时控制
      const data = await Promise.race([
        apiService.get(API_ENDPOINTS.MONITORING.GET_DATA),
        timeoutPromise
      ])
      return data
    } catch (error) {
      console.error('获取监控数据失败:', error)
      // 在实际环境中，这里可以返回缓存数据或默认数据
      // 但在当前环境中，我们让调用者处理错误，以便使用模拟数据
      throw error
    }
  },

  /**
   * 更新步骤参数
   * @param {string} stepId 步骤ID
   * @param {Object} parameters 参数对象
   * @returns {Promise<boolean>} 是否更新成功
   */
  async updateStepParameters(stepId, parameters) {
    try {
      // 验证参数
      if (!stepId || !parameters || typeof parameters !== 'object') {
        throw new Error('无效的参数')
      }
      
      // 这里可以调用后端API来更新参数
      console.log('更新参数:', stepId, parameters)
      
      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 500))
      
      // 模拟成功响应
      return true
    } catch (error) {
      console.error('更新参数失败:', error)
      // 即使失败也返回false，而不是抛出错误，让调用者可以优雅处理
      return false
    }
  }
}

// 添加防抖版本的方法
monitoringService.debouncedGetMonitoringData = debounce(monitoringService.getMonitoringData, 1000)

export default monitoringService