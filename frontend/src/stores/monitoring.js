import { defineStore } from 'pinia'
import { monitoringService } from '../services/monitoringService'

export const useMonitoringStore = defineStore('monitoring', {
  state: () => ({
    monitoringData: {
      totalTasks: 12,
      successTasks: 8,
      failedTasks: 1,
      runningTasks: 3,
      avgExecutionTime: "50s",
      agentStatuses: {
        creative: "可用",
        novel: "已替换",
        story_script: "可用",
        scheduler: "可用"
      },
      executionHistory: [
        {
          id: "task_1",
          taskGoal: "生成一个关于人工智能的故事创意，并撰写短篇小说",
          status: "completed",
          startTime: "2026-01-26T10:00:00",
          endTime: "2026-01-26T10:45:00",
          duration: "45s",
          agents: ["创意策划智能体", "小说创作智能体"]
        },
        {
          id: "task_2",
          taskGoal: "生成一个关于职场压力的故事创意",
          status: "running",
          startTime: "2026-01-26T11:00:00",
          endTime: null,
          duration: "15s",
          agents: ["创意策划智能体"]
        },
        {
          id: "task_3",
          taskGoal: "撰写一篇关于都市情感的短篇小说",
          status: "failed",
          startTime: "2026-01-26T09:30:00",
          endTime: "2026-01-26T09:40:00",
          duration: "10s",
          agents: ["小说创作智能体"]
        },
        {
          id: "task_4",
          taskGoal: "生成一个关于人工智能的故事创意，并创作故事剧本",
          status: "completed",
          startTime: "2026-01-26T12:00:00",
          endTime: "2026-01-26T12:50:00",
          duration: "50s",
          agents: ["创意策划智能体", "故事剧本一体化智能体"]
        },
        {
          id: "task_5",
          taskGoal: "协调智能体工作流，处理故事创作任务",
          status: "running",
          startTime: "2026-01-26T13:00:00",
          endTime: null,
          duration: "10s",
          agents: ["协调智能体"]
        }
      ],
      workflowDetails: {
        "task_1": [
          {
            stepId: "step_1",
            agentType: "创意策划智能体",
            task: "生成故事创意框架",
            status: "success",
            startTime: "2026-01-26T10:00:00",
            endTime: "2026-01-26T10:15:00",
            duration: "15s",
            parameters: {
              hotspots: ["人工智能", "职场压力", "都市情感"],
              story_type: "都市情感"
            }
          },
          {
            stepId: "step_2",
            agentType: "小说创作智能体",
            task: "撰写小说",
            status: "success",
            startTime: "2026-01-26T10:15:00",
            endTime: "2026-01-26T10:45:00",
            duration: "30s",
            parameters: {
              style: "urban",
              chapter_count: 5
            }
          }
        ],
        "task_2": [
          {
            stepId: "step_1",
            agentType: "创意策划智能体",
            task: "生成故事创意框架",
            status: "running",
            startTime: "2026-01-26T11:00:00",
            endTime: null,
            duration: "15s",
            parameters: {
              hotspots: ["职场压力", "团队协作", "职业发展"],
              story_type: "职场"
            }
          }
        ],
        "task_3": [
          {
            stepId: "step_1",
            agentType: "小说创作智能体",
            task: "撰写小说",
            status: "failed",
            startTime: "2026-01-26T09:30:00",
            endTime: "2026-01-26T09:40:00",
            duration: "10s",
            error: "执行超时",
            parameters: {
              style: "urban",
              chapter_count: 5
            }
          }
        ],
        "task_4": [
          {
            stepId: "step_1",
            agentType: "创意策划智能体",
            task: "生成故事创意框架",
            status: "success",
            startTime: "2026-01-26T12:00:00",
            endTime: "2026-01-26T12:15:00",
            duration: "15s",
            parameters: {
              hotspots: ["人工智能", "职场压力", "都市情感"],
              story_type: "都市情感"
            }
          },
          {
            stepId: "step_2",
            agentType: "故事剧本一体化智能体",
            task: "创作故事剧本",
            status: "success",
            startTime: "2026-01-26T12:15:00",
            endTime: "2026-01-26T12:50:00",
            duration: "35s",
            parameters: {
              style: "urban",
              medium_type: "novel",
              chapter_count: 5
            }
          }
        ],
        "task_5": [
          {
            stepId: "step_1",
            agentType: "协调智能体",
            task: "协调智能体工作流",
            status: "running",
            startTime: "2026-01-26T13:00:00",
            endTime: null,
            duration: "10s",
            parameters: {
              request_priority: 3,
              task_goal: "处理故事创作任务"
            }
          }
        ]
      }
    },
    selectedWorkflowId: null,
    isLoading: false,
    error: null
  }),

  getters: {
    getSelectedWorkflowDetails: (state) => {
      if (!state.selectedWorkflowId) return []
      return state.monitoringData.workflowDetails[state.selectedWorkflowId] || []
    },
    getExecutionHistory: (state) => {
      return state.monitoringData.executionHistory
    },
    getAgentStatuses: (state) => {
      return state.monitoringData.agentStatuses
    }
  },

  actions: {
    async fetchMonitoringData() {
      try {
        this.isLoading = true
        this.error = null
        const data = await monitoringService.debouncedGetMonitoringData()
        this.monitoringData = data
      } catch (error) {
        console.error('获取监控数据失败:', error)
        this.error = error.message || '获取监控数据失败'
        // 使用模拟数据 - 保留现有的模拟数据结构
        console.log('使用模拟数据')
      } finally {
        this.isLoading = false
      }
    },

    setSelectedWorkflowId(taskId) {
      this.selectedWorkflowId = taskId
    },

    async updateStepParameters(stepId, parameters) {
      try {
        this.isLoading = true
        this.error = null
        const success = await monitoringService.updateStepParameters(stepId, parameters)
        return success
      } catch (error) {
        console.error('更新参数失败:', error)
        this.error = error.message || '更新参数失败'
        return false
      } finally {
        this.isLoading = false
      }
    }
  }
})