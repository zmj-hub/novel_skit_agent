const endpoints = {
  // 监控相关
  monitoring: {
    data: '/monitoring/data',
    agents: '/monitoring/agents',
    history: '/monitoring/history',
  },
  
  // 聊天相关
  chat: {
    send: '/chat/send',
    history: '/chat/history',
    sessions: '/chat/sessions',
  },
  
  // 创意相关
  creative: {
    generate: '/creative/generate',
    list: '/creative/list',
    detail: (id) => `/creative/${id}`,
    update: (id) => `/creative/${id}`,
    delete: (id) => `/creative/${id}`,
  },
  
  // 智能体相关
  agent: {
    list: '/agent/list',
    detail: (id) => `/agent/${id}`,
    update: (id) => `/agent/${id}`,
  },
  
  // 知识库相关
  knowledge: {
    upload: '/knowledge/upload',
    list: '/knowledge/list',
    delete: (id) => `/knowledge/${id}`,
  },
  
  // 协作相关
  collaboration: {
    create: '/collaboration/create',
    list: '/collaboration/list',
    detail: (id) => `/collaboration/${id}`,
    update: (id) => `/collaboration/${id}`,
    delete: (id) => `/collaboration/${id}`,
  },
  
  // 调度相关
  scheduler: {
    schedule: '/scheduler/schedule',
    tasks: '/scheduler/tasks',
    task: (id) => `/scheduler/tasks/${id}`,
    execute: (id) => `/scheduler/tasks/${id}/execute`,
    cancel: (id) => `/scheduler/tasks/${id}/cancel`,
    ws: (sessionId) => `/scheduler/ws/${sessionId}`,
  },
}

export default endpoints
