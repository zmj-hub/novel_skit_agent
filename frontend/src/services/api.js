import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api', // 后端API基础URL
  timeout: 10000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 可以在这里添加认证信息，如token等
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 直接返回响应数据
    return response.data
  },
  error => {
    console.error('响应错误:', error)
    // 统一错误处理
    const errorMessage = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(errorMessage))
  }
)

// 基本的API方法
export const apiService = {
  get: (url, params = {}) => {
    return api.get(url, { params })
  },
  post: (url, data = {}) => {
    return api.post(url, data)
  },
  put: (url, data = {}) => {
    return api.put(url, data)
  },
  delete: (url, params = {}) => {
    return api.delete(url, { params })
  },
  patch: (url, data = {}) => {
    return api.patch(url, data)
  }
}

export default api