// API端点配置
export const API_ENDPOINTS = {
  // 监控相关
  MONITORING: {
    GET_DATA: '/monitoring/data',
    GET_WORKFLOW: (taskId) => `/monitoring/workflow/${taskId}`
  },
  
  // 工作流相关
  WORKFLOW: {
    COLLABORATE: '/collaborate',
    CANCEL: (sessionId) => `/collaboration/cancel/${sessionId}`
  }
}

export default API_ENDPOINTS