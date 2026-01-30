from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
import json

router = APIRouter(tags=["monitoring"])


@router.get("/data", response_model=Dict[str, Any])
async def get_monitoring_data() -> Dict[str, Any]:
    """
    获取监控数据
    
    该接口用于获取工作流监控数据，包括工作流状态概览、智能体状态和执行历史。
    
    Args:
        无
    
    Returns:
        Dict[str, Any]: 监控数据
            - totalTasks: int, 总任务数
            - successTasks: int, 成功任务数
            - failedTasks: int, 失败任务数
            - runningTasks: int, 运行中任务数
            - avgExecutionTime: str, 平均执行时间
            - agentStatuses: Dict[str, str], 智能体状态
            - executionHistory: List[Dict], 执行历史
    
    典型调用场景:
        - 场景1: 前端获取监控数据更新界面
        - 场景2: 后端监控系统获取执行状态
    
    与其他接口的关联关系:
        - 前置依赖接口: 无
        - 后续调用接口: 无
    
    错误码定义:
        - 200: 成功
        - 500: 服务器内部错误
    """
    # 这里可以从存储中获取实际的监控数据
    # 暂时返回一个示例响应
    return {
        "totalTasks": 10,
        "successTasks": 7,
        "failedTasks": 1,
        "runningTasks": 2,
        "avgExecutionTime": "45s",
        "agentStatuses": {
            "creative": "available",
            "novel": "available", 
            "scheduler": "available"
        },
        "executionHistory": [
            {
                "id": "task_1",
                "taskGoal": "Generate AI story idea and write short story",
                "status": "completed",
                "startTime": "2026-01-26T10:00:00",
                "endTime": "2026-01-26T10:45:00",
                "duration": "45s",
                "agents": ["Creative Agent", "Novel Agent"]
            },
            {
                "id": "task_2",
                "taskGoal": "Generate workplace stress story idea",
                "status": "running",
                "startTime": "2026-01-26T11:00:00",
                "endTime": None,
                "duration": "15s",
                "agents": ["Creative Agent"]
            },
            {
                "id": "task_3",
                "taskGoal": "Write urban emotion short story",
                "status": "failed",
                "startTime": "2026-01-26T09:30:00",
                "endTime": "2026-01-26T09:40:00",
                "duration": "10s",
                "agents": ["Novel Agent"]
            }
        ]
    }


@router.get("/workflow/{task_id}", response_model=Dict[str, Any])
async def get_workflow_details(task_id: str) -> Dict[str, Any]:
    """
    获取工作流详情
    
    该接口用于获取指定工作流的详细步骤信息。
    
    Args:
        task_id: str, 工作流任务ID
    
    Returns:
        Dict[str, Any]: 工作流详情
            - taskId: str, 任务ID
            - steps: List[Dict], 工作流步骤列表
    
    典型调用场景:
        - 场景1: 前端查看工作流执行详情
        - 场景2: 调试工作流执行过程
    
    错误码定义:
        - 200: 成功
        - 404: 工作流不存在
        - 500: 服务器内部错误
    """
    # 模拟工作流详情数据
    workflow_details = {
        "task_1": [
            {
                "stepId": "step_1",
                "agentType": "创意策划智能体",
                "task": "生成故事创意框架",
                "status": "success",
                "startTime": "2026-01-26T10:00:00",
                "endTime": "2026-01-26T10:15:00",
                "duration": "15s"
            },
            {
                "stepId": "step_2",
                "agentType": "小说创作智能体",
                "task": "撰写小说",
                "status": "success",
                "startTime": "2026-01-26T10:15:00",
                "endTime": "2026-01-26T10:45:00",
                "duration": "30s"
            }
        ],
        "task_2": [
            {
                "stepId": "step_1",
                "agentType": "创意策划智能体",
                "task": "生成故事创意框架",
                "status": "running",
                "startTime": "2026-01-26T11:00:00",
                "endTime": None,
                "duration": "15s"
            }
        ],
        "task_3": [
            {
                "stepId": "step_1",
                "agentType": "小说创作智能体",
                "task": "撰写小说",
                "status": "failed",
                "startTime": "2026-01-26T09:30:00",
                "endTime": "2026-01-26T09:40:00",
                "duration": "10s",
                "error": "执行超时"
            }
        ]
    }
    
    if task_id not in workflow_details:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    return {
        "taskId": task_id,
        "steps": workflow_details[task_id]
    }
