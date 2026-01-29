// 应用工具函数

/**
 * 格式化时间戳为人类可读的时间格式
 * @param {number|string} timestamp - 时间戳
 * @returns {string} 格式化后的时间字符串
 */
export const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

/**
 * 格式化数字，添加千位分隔符
 * @param {number} num - 要格式化的数字
 * @returns {string} 格式化后的数字字符串
 */
export const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * 获取智能体状态对应的CSS类
 * @param {string} status - 智能体状态
 * @returns {string} CSS类名
 */
export const getAgentStatusClass = (status) => {
  switch (status) {
    case '可用':
      return 'bg-green-100 text-green-700 hover:bg-green-200'
    case '繁忙':
      return 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200'
    case '错误':
      return 'bg-red-100 text-red-700 hover:bg-red-200'
    default:
      return 'bg-gray-100 text-gray-700 hover:bg-gray-200'
  }
}

/**
 * 获取工作流状态对应的CSS类
 * @param {string} status - 工作流状态
 * @returns {string} CSS类名
 */
export const getWorkflowStatusClass = (status) => {
  switch (status) {
    case '运行中':
      return 'bg-blue-100 text-blue-700 hover:bg-blue-200'
    case '已完成':
      return 'bg-green-100 text-green-700 hover:bg-green-200'
    case '失败':
      return 'bg-red-100 text-red-700 hover:bg-red-200'
    case '已停止':
      return 'bg-orange-100 text-orange-700 hover:bg-orange-200'
    default:
      return 'bg-gray-100 text-gray-700 hover:bg-gray-200'
  }
}

/**
 * 生成唯一ID
 * @returns {string} 唯一ID
 */
export const generateUniqueId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2)
}

/**
 * 防抖函数
 * @param {Function} func - 要执行的函数
 * @param {number} delay - 延迟时间（毫秒）
 * @returns {Function} 防抖后的函数
 */
export const debounce = (func, delay) => {
  let timeoutId
  return (...args) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => func.apply(null, args), delay)
  }
}

/**
 * 节流函数
 * @param {Function} func - 要执行的函数
 * @param {number} limit - 时间限制（毫秒）
 * @returns {Function} 节流后的函数
 */
export const throttle = (func, limit) => {
  let inThrottle
  return (...args) => {
    if (!inThrottle) {
      func.apply(null, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}
