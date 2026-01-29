// 应用常量定义

// 颜色常量
export const COLORS = {
  PRIMARY: '#3b82f6',
  SECONDARY: '#8b5cf6',
  SUCCESS: '#10b981',
  WARNING: '#f59e0b',
  DANGER: '#ef4444',
  INFO: '#3b82f6',
  LIGHT: '#f3f4f6',
  DARK: '#1f2937'
}

// 状态常量
export const AGENT_STATUS = {
  AVAILABLE: '可用',
  BUSY: '繁忙',
  ERROR: '错误',
  UNKNOWN: '未知'
}

// 工作流状态常量
export const WORKFLOW_STATUS = {
  IDLE: '空闲',
  RUNNING: '运行中',
  COMPLETED: '已完成',
  FAILED: '失败',
  STOPPED: '已停止'
}

// API 端点常量
export const API_ENDPOINTS = {
  MONITORING: '/api/monitoring',
  WORKFLOW: '/api/workflow',
  EXECUTION: '/api/execution'
}

// 响应式断点常量
export const BREAKPOINTS = {
  SM: '640px',
  MD: '768px',
  LG: '1024px',
  XL: '1280px',
  '2XL': '1536px'
}

// 动画持续时间常量（毫秒）
export const ANIMATION_DURATION = {
  FAST: 150,
  NORMAL: 300,
  SLOW: 500
}
