import { defineStore } from 'pinia'

export const useUIStore = defineStore('ui', {
  state: () => ({
    notifications: {
      error: null,
      success: null
    },
    isLoading: false,
    loadingMessage: null
  }),

  getters: {
    hasError: (state) => {
      return state.notifications.error !== null
    },
    hasSuccess: (state) => {
      return state.notifications.success !== null
    },
    isLoading: (state) => {
      return state.isLoading
    }
  },

  actions: {
    showError(message) {
      this.notifications.error = message
      // 3秒后自动清除错误消息
      setTimeout(() => {
        this.clearError()
      }, 3000)
    },

    showSuccess(message) {
      this.notifications.success = message
      // 3秒后自动清除成功消息
      setTimeout(() => {
        this.clearSuccess()
      }, 3000)
    },

    clearError() {
      this.notifications.error = null
    },

    clearSuccess() {
      this.notifications.success = null
    },

    clearAllNotifications() {
      this.notifications.error = null
      this.notifications.success = null
    },

    setLoading(isLoading, message = null) {
      this.isLoading = isLoading
      this.loadingMessage = message
    }
  }
})