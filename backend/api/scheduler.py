from fastapi import APIRouter, HTTPException
from models.schemas import SchedulerRequest, SchedulerResponse, WorkflowSchedule, WorkflowLog, ExceptionReport
from agent.workflow import scheduler_workflow
from typing import Optional

router = APIRouter(prefix="/scheduler", tags=["scheduler"])


@router.post("/schedule", response_model=SchedulerResponse)
async def create_schedule(request: SchedulerRequest) -> SchedulerResponse:
    """
    协同调度接口
    
    该接口用于创建工作流调度计划，包括工作时序规划、冲突处理、优先级调度和智能体适配处理。
    
    Args:
        request: 调度请求参数
            - request_priority: int, 必填, 请求优先级
            - session_id: str, 必填, 会话ID
            - model: str, 必填, 选择的模型名称
    
    Returns:
        SchedulerResponse: 调度响应
            - response: str, 响应消息
            - session_id: str, 会话ID
            - schedule: Optional[WorkflowSchedule], 工作时序表
            - workflow_log: Optional[WorkflowLog], 工作流调度日志
            - exception_report: Optional[ExceptionReport], 异常处理报告
            - processed_at: str, 处理时间
    
    典型调用场景:
        - 场景1: 为高优先级任务创建调度计划
        - 场景2: 为多智能体协作创建调度计划
    
    与其他接口的关联关系:
        - 前置依赖接口: 无
        - 后续调用接口: /api/collaborate (智能体协作)
    
    错误码定义:
        - 200: 成功
        - 400: 请求参数错误
        - 500: 服务器内部错误
    """
    try:
        # 构建工作流输入
        workflow_input = {
            "request_priority": request.request_priority,
            "session_id": request.session_id,
            "model": request.model
        }
        
        # 执行工作流
        result = await scheduler_workflow.ainvoke(workflow_input)
        
        # 构建响应
        workflow_schedule = None
        if "schedule" in result:
            workflow_schedule = WorkflowSchedule(
                schedule=result["schedule"].get("schedule", []),
                created_at=result["schedule"].get("created_at", ""),
                total_duration=result["schedule"].get("total_duration", 0)
            )
        
        workflow_log = None
        if "scheduling_log" in result:
            workflow_log = WorkflowLog(
                log_entries=result["scheduling_log"].get("log_entries", []),
                generated_at=result["scheduling_log"].get("generated_at", ""),
                total_steps=result["scheduling_log"].get("total_steps", 0),
                included_steps=result["scheduling_log"].get("included_steps", 0),
                skipped_steps=result["scheduling_log"].get("skipped_steps", 0)
            )
        
        exception_report = None
        if "exception_report" in result:
            exception_report = ExceptionReport(
                exceptions=result["exception_report"].get("exceptions", []),
                generated_at=result["exception_report"].get("generated_at", ""),
                total_exceptions=result["exception_report"].get("total_exceptions", 0),
                resolved_exceptions=result["exception_report"].get("resolved_exceptions", 0),
                unresolved_exceptions=result["exception_report"].get("unresolved_exceptions", 0)
            )
        
        # 构建响应
        response = SchedulerResponse(
            response=result.get("response", "工作流调度已完成"),
            session_id=request.session_id,
            schedule=workflow_schedule,
            workflow_log=workflow_log,
            exception_report=exception_report,
            processed_at=result.get("processed_at", "")
        )
        
        return response
        
    except Exception as e:
        print(f"Error in scheduler API: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
