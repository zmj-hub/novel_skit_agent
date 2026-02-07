import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // State
  const userInfo = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  const isLoggedIn = computed(() => !!token.value)
  
  // Actions
  function setUserInfo(info) {
    userInfo.value = info
  }
  
  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }
  
  function logout() {
    userInfo.value = null
    token.value = ''
    localStorage.removeItem('token')
  }
  
  return {
    userInfo,
    token,
    isLoggedIn,
    setUserInfo,
    setToken,
    logout,
  }
})
