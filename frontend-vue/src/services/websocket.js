/**
 * WebSocket服务模块 - 增强版
 * 
 * 特性：
 * - 自动重连机制（指数退避）
 * - 心跳检测
 * - 统一事件处理
 * - 连接状态管理
 */

import { ElNotification } from 'element-plus'

class WebSocketService {
  constructor() {
    this.ws = null
    this.sessionId = null
    this.url = null
    
    // 连接状态
    this.isConnected = false
    this.isConnecting = false
    this.connectionState = 'disconnected' // disconnected, connecting, connected, reconnecting, error
    
    // 重连配置
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 10
    this.reconnectDelay = 1000 // 初始重连延迟1秒
    this.maxReconnectDelay = 30000 // 最大重连延迟30秒
    this.reconnectTimer = null
    
    // 心跳配置
    this.heartbeatInterval = 60000 // 60秒发送一次心跳
    this.heartbeatTimer = null
    this.missedHeartbeats = 0
    this.maxMissedHeartbeats = 5
    
    // 事件回调
    this.eventHandlers = {
      onOpen: [],
      onMessage: [],
      onClose: [],
      onError: [],
      onReconnect: [],
      onStateChange: []
    }
    
    // 消息队列（连接断开时缓存消息）
    this.messageQueue = []
    this.maxQueueSize = 100
  }

  /**
   * 连接到WebSocket服务器
   * @param {string} sessionId - 会话ID
   * @param {string} baseUrl - 基础URL（可选，默认使用当前主机）
   * @returns {Promise<boolean>} - 连接是否成功
   */
  async connect(sessionId, baseUrl = null) {
    if (this.isConnected || this.isConnecting) {
      console.log('[WebSocket] 已经连接或正在连接中')
      return true
    }

    this.sessionId = sessionId
    this.isConnecting = true
    this._setConnectionState('connecting')

    // 构建WebSocket URL
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = baseUrl || window.location.host
    this.url = `${protocol}//${host}/api/scheduler/ws/${sessionId}`

    console.log(`[WebSocket] 正在连接到: ${this.url}`)

    try {
      this.ws = new WebSocket(this.url)
      
      // 设置连接超时
      const connectionTimeout = setTimeout(() => {
        if (!this.isConnected) {
          console.error('[WebSocket] 连接超时')
          this.ws.close()
          this._handleConnectionError(new Error('连接超时'))
        }
      }, 30000) // 30秒超时

      this.ws.onopen = (event) => {
        clearTimeout(connectionTimeout)
        this._handleOpen(event)
      }

      this.ws.onmessage = (event) => {
        this._handleMessage(event)
      }

      this.ws.onclose = (event) => {
        clearTimeout(connectionTimeout)
        this._handleClose(event)
      }

      this.ws.onerror = (error) => {
        clearTimeout(connectionTimeout)
        this._handleError(error)
      }

      // 等待连接建立
      await this._waitForConnection()
      return true

    } catch (error) {
      console.error('[WebSocket] 连接失败:', error)
      this._handleConnectionError(error)
      return false
    }
  }

  /**
   * 断开连接
   */
  disconnect() {
    console.log('[WebSocket] 断开连接')
    
    // 清除重连定时器
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    
    // 清除心跳定时器
    this._stopHeartbeat()
    
    // 重置重连计数
    this.reconnectAttempts = 0
    
    // 关闭连接
    if (this.ws) {
      // 移除事件监听器，避免触发重连
      this.ws.onclose = null
      this.ws.onerror = null
      
      if (this.ws.readyState === WebSocket.OPEN || 
          this.ws.readyState === WebSocket.CONNECTING) {
        this.ws.close(1000, '客户端主动断开')
      }
      
      this.ws = null
    }
    
    this.isConnected = false
    this.isConnecting = false
    this._setConnectionState('disconnected')
  }

  /**
   * 发送消息
   * @param {string} message - 要发送的消息
   * @returns {boolean} - 是否发送成功
   */
  send(message) {
    if (this.isConnected && this.ws && this.ws.readyState === WebSocket.OPEN) {
      try {
        this.ws.send(message)
        return true
      } catch (error) {
        console.error('[WebSocket] 发送消息失败:', error)
        // 将消息加入队列
        this._queueMessage(message)
        return false
      }
    } else {
      // 连接未建立，将消息加入队列
      this._queueMessage(message)
      console.warn('[WebSocket] 连接未建立，消息已加入队列')
      return false
    }
  }

  /**
   * 发送JSON消息
   * @param {object} data - 要发送的数据
   * @returns {boolean} - 是否发送成功
   */
  sendJSON(data) {
    return this.send(JSON.stringify(data))
  }

  /**
   * 发送心跳
   */
  sendHeartbeat() {
    if (this.isConnected) {
      this.send('ping')
      this.missedHeartbeats++
      
      // 如果连续未收到响应超过阈值，认为连接已断开
      if (this.missedHeartbeats > this.maxMissedHeartbeats) {
        console.warn('[WebSocket] 心跳超时，连接可能已断开')
        this._handleConnectionError(new Error('心跳超时'))
      }
    }
  }

  /**
   * 获取连接状态
   * @returns {object} - 连接状态信息
   */
  getStatus() {
    return {
      isConnected: this.isConnected,
      isConnecting: this.isConnecting,
      state: this.connectionState,
      sessionId: this.sessionId,
      reconnectAttempts: this.reconnectAttempts,
      maxReconnectAttempts: this.maxReconnectAttempts,
      queuedMessages: this.messageQueue.length
    }
  }

  /**
   * 注册事件处理器
   * @param {string} event - 事件类型
   * @param {function} handler - 处理函数
   */
  on(event, handler) {
    if (this.eventHandlers[event]) {
      this.eventHandlers[event].push(handler)
    } else {
      console.warn(`[WebSocket] 未知事件类型: ${event}`)
    }
  }

  /**
   * 移除事件处理器
   * @param {string} event - 事件类型
   * @param {function} handler - 处理函数
   */
  off(event, handler) {
    if (this.eventHandlers[event]) {
      const index = this.eventHandlers[event].indexOf(handler)
      if (index > -1) {
        this.eventHandlers[event].splice(index, 1)
      }
    }
  }

  // ============ 私有方法 ============

  /**
   * 处理连接打开
   */
  _handleOpen(event) {
    console.log('[WebSocket] 连接已建立')
    this.isConnected = true
    this.isConnecting = false
    this.reconnectAttempts = 0
    this.missedHeartbeats = 0
    this._setConnectionState('connected')
    
    // 启动心跳
    this._startHeartbeat()
    
    // 发送队列中的消息
    this._flushMessageQueue()
    
    // 触发事件
    this._emit('onOpen', event)
    
    // 显示通知
    ElNotification.success({
      title: '实时连接已建立',
      message: '您将实时收到任务执行进度更新',
      duration: 3000
    })
  }

  /**
   * 处理消息接收
   */
  _handleMessage(event) {
    try {
      const data = JSON.parse(event.data)
      
      // 处理心跳响应
      if (data.type === 'pong') {
        this.missedHeartbeats = 0
        console.log('[WebSocket] 收到心跳响应')
        return
      }
      
      // 处理连接确认
      if (data.type === 'connection_established') {
        console.log('[WebSocket] 连接确认:', data.message)
        return
      }
      
      // 触发消息事件
      this._emit('onMessage', data)
      
    } catch (error) {
      console.error('[WebSocket] 解析消息失败:', error)
      // 触发原始消息事件
      this._emit('onMessage', event.data)
    }
  }

  /**
   * 处理连接关闭
   */
  _handleClose(event) {
    console.log(`[WebSocket] 连接已关闭: code=${event.code}, reason=${event.reason}`)
    
    const wasConnected = this.isConnected
    this.isConnected = false
    this.isConnecting = false
    this._stopHeartbeat()
    
    this._emit('onClose', event)
    
    // 如果之前是连接状态且不是正常关闭，尝试重连
    if (wasConnected && event.code !== 1000 && event.code !== 1001) {
      console.log('[WebSocket] 连接异常断开，准备重连')
      this._setConnectionState('reconnecting')
      this._scheduleReconnect()
    } else {
      this._setConnectionState('disconnected')
    }
  }

  /**
   * 处理错误
   */
  _handleError(error) {
    console.error('[WebSocket] 连接错误:', error)
    this._setConnectionState('error')
    this._emit('onError', error)
    
    // 显示错误通知
    ElNotification.error({
      title: '实时连接错误',
      message: 'WebSocket连接发生错误，正在尝试重连...',
      duration: 3000
    })
  }

  /**
   * 处理连接错误
   */
  _handleConnectionError(error) {
    this.isConnecting = false
    this._handleError(error)
    this._scheduleReconnect()
  }

  /**
   * 安排重连
   */
  _scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('[WebSocket] 达到最大重连次数，停止重连')
      this._setConnectionState('error')
      
      ElNotification.error({
        title: '连接失败',
        message: '无法建立实时连接，请刷新页面重试',
        duration: 0 // 不自动关闭
      })
      
      return
    }
    
    this.reconnectAttempts++
    
    // 计算重连延迟（指数退避）
    const delay = Math.min(
      this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1),
      this.maxReconnectDelay
    )
    
    console.log(`[WebSocket] 计划第${this.reconnectAttempts}次重连，延迟${delay}ms`)
    
    this.reconnectTimer = setTimeout(() => {
      console.log(`[WebSocket] 开始第${this.reconnectAttempts}次重连`)
      this._emit('onReconnect', { attempt: this.reconnectAttempts })
      this.connect(this.sessionId)
    }, delay)
  }

  /**
   * 启动心跳
   */
  _startHeartbeat() {
    this._stopHeartbeat()
    this.heartbeatTimer = setInterval(() => {
      this.sendHeartbeat()
    }, this.heartbeatInterval)
    console.log('[WebSocket] 心跳检测已启动')
  }

  /**
   * 停止心跳
   */
  _stopHeartbeat() {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer)
      this.heartbeatTimer = null
      console.log('[WebSocket] 心跳检测已停止')
    }
    this.missedHeartbeats = 0
  }

  /**
   * 等待连接建立
   */
  _waitForConnection() {
    return new Promise((resolve) => {
      const checkConnection = () => {
        if (this.isConnected) {
          resolve(true)
        } else if (!this.isConnecting) {
          resolve(false)
        } else {
          setTimeout(checkConnection, 100)
        }
      }
      checkConnection()
    })
  }

  /**
   * 设置连接状态
   */
  _setConnectionState(state) {
    const oldState = this.connectionState
    this.connectionState = state
    
    if (oldState !== state) {
      console.log(`[WebSocket] 连接状态变化: ${oldState} -> ${state}`)
      this._emit('onStateChange', { oldState, newState: state })
    }
  }

  /**
   * 触发事件
   */
  _emit(event, data) {
    if (this.eventHandlers[event]) {
      this.eventHandlers[event].forEach(handler => {
        try {
          handler(data)
        } catch (error) {
          console.error(`[WebSocket] 事件处理器错误: ${event}`, error)
        }
      })
    }
  }

  /**
   * 将消息加入队列
   */
  _queueMessage(message) {
    if (this.messageQueue.length >= this.maxQueueSize) {
      this.messageQueue.shift() // 移除最旧的消息
    }
    this.messageQueue.push(message)
  }

  /**
   * 发送队列中的消息
   */
  _flushMessageQueue() {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift()
      this.send(message)
    }
  }
}

// 创建单例实例
const websocketService = new WebSocketService()

export default websocketService
export { WebSocketService }