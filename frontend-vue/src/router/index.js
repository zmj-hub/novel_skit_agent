import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      title: '仪表盘',
    },
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('@/views/Chat.vue'),
    meta: {
      title: '智能对话',
    },
  },
  {
    path: '/creative',
    name: 'Creative',
    component: () => import('@/views/Creative.vue'),
    meta: {
      title: '创意策划',
    },
  },
  {
    path: '/novel',
    name: 'Novel',
    component: () => import('@/views/Novel.vue'),
    meta: {
      title: '小说创作',
    },
  },
  {
    path: '/collaboration',
    name: 'Collaboration',
    component: () => import('@/views/Collaboration.vue'),
    meta: {
      title: '智能体协作',
    },
  },
  {
    path: '/scheduler',
    name: 'Scheduler',
    component: () => import('@/views/Scheduler.vue'),
    meta: {
      title: '任务调度',
    },
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: () => import('@/views/Knowledge.vue'),
    meta: {
      title: '知识库',
    },
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: {
      title: '系统设置',
    },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 小说创作智能体`
  }
  next()
})

export default router
