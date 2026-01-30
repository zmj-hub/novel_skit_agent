import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证信息
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    // 统一错误处理
    if (error.response) {
      // 服务器返回错误状态码
      switch (error.response.status) {
        case 401:
          // 未授权，跳转到登录页
          // window.location.href = '/login';
          break;
        case 403:
          // 禁止访问
          console.error('Forbidden');
          break;
        case 404:
          // 资源不存在
          console.error('Not Found');
          break;
        case 500:
          // 服务器内部错误
          console.error('Server Error');
          break;
        default:
          console.error('Request Error');
      }
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      console.error('Network Error');
    } else {
      // 请求配置出错
      console.error('Request Config Error');
    }
    return Promise.reject(error);
  }
);

export default api;