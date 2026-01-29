// 应用类型定义

/**
 * 智能体状态类型
 * @typedef {Object} AgentStatus
 * @property {string} creative - 创意策划智能体状态
 * @property {string} novel - 小说创作智能体状态
 * @property {string} scheduler - 协同调度智能体状态
 */

/**
 * 工作流执行历史项类型
 * @typedef {Object} ExecutionHistoryItem
 * @property {string} taskId - 任务ID
 * @property {string} taskGoal - 任务目标
 * @property {string} status - 任务状态
 * @property {string} startTime - 开始时间
 * @property {string} endTime - 结束时间
 * @property {number} duration - 持续时间（秒）
 * @property {Object} metrics - 任务指标
 */

/**
 * 工作流步骤类型
 * @typedef {Object} WorkflowStep
 * @property {string} stepId - 步骤ID
 * @property {string} name - 步骤名称
 * @property {string} status - 步骤状态
 * @property {string} startTime - 开始时间
 * @property {string} endTime - 结束时间
 * @property {Object} parameters - 步骤参数
 * @property {Object} result - 步骤结果
 */

/**
 * 监控数据类型
 * @typedef {Object} MonitoringData
 * @property {string} workflowStatus - 工作流状态
 * @property {number} executionCount - 执行次数
 * @property {number} successCount - 成功次数
 * @property {number} failureCount - 失败次数
 * @property {number} averageExecutionTime - 平均执行时间
 * @property {AgentStatus} agentStatuses - 智能体状态
 * @property {ExecutionHistoryItem[]} executionHistory - 执行历史
 * @property {WorkflowStep[]} workflowSteps - 工作流步骤
 */

/**
 * 执行参数类型
 * @typedef {Object} ExecutionParams
 * @property {string} taskGoal - 任务目标
 * @property {string} sessionId - 会话ID
 * @property {string} model - 模型名称
 * @property {number} timeout - 超时时间（秒）
 * @property {string} priority - 优先级
 */

/**
 * 通知类型
 * @typedef {Object} Notification
 * @property {string} error - 错误信息
 * @property {string} success - 成功信息
 * @property {string} warning - 警告信息
 * @property {string} info - 信息
 */

/**
 * UI状态类型
 * @typedef {Object} UIState
 * @property {boolean} loading - 加载状态
 * @property {Notification} notifications - 通知信息
 * @property {string} selectedWorkflowId - 选中的工作流ID
 */

/**
 * 监控状态类型
 * @typedef {Object} MonitoringState
 * @property {MonitoringData} monitoringData - 监控数据
 * @property {string} selectedWorkflowId - 选中的工作流ID
 * @property {boolean} loading - 加载状态
 * @property {string} error - 错误信息
 */

/**
 * 工作流状态类型
 * @typedef {Object} WorkflowState
 * @property {ExecutionParams} executionParams - 执行参数
 * @property {boolean} isExecuting - 是否正在执行
 * @property {string} executionError - 执行错误
 */
