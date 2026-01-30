// API端点配置
export const endpoints = {
  // 监控相关
  monitoring: {
    data: '/monitoring/data',
  },
  
  // 聊天相关
  chat: {
    send: '/chat/send',
    history: '/chat/history',
  },
  
  // 创作相关
  creative: {
    generate: '/creative/generate',
    list: '/creative/list',
    detail: '/creative/detail',
    update: '/creative/update',
    delete: '/creative/delete',
  },
  
  // 智能体相关
  agent: {
    list: '/agent/list',
    detail: '/agent/detail',
    update: '/agent/update',
  },
  
  // 知识相关
  knowledge: {
    upload: '/knowledge/upload',
    list: '/knowledge/list',
    delete: '/knowledge/delete',
  },
  
  // 协作相关
  collaboration: {
    create: '/collaboration/create',
    list: '/collaboration/list',
    detail: '/collaboration/detail',
    update: '/collaboration/update',
    delete: '/collaboration/delete',
  },
  
  // 调度相关
  scheduler: {
    tasks: '/scheduler/tasks',
    execute: '/scheduler/execute',
    cancel: '/scheduler/cancel',
    schedule: '/scheduler/schedule',
  },
};

export default endpoints;