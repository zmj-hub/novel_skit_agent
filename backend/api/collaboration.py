from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
from models.schemas import CollaborationRequest, CollaborationResponse, CollaborationStatusResponse, CollaborationCancelResponse
from agent.collaboration_workflow import collaboration_workflow
from agent.agent_collaboration import CollaborationState, WorkflowState

router = APIRouter(prefix="/collaboration", tags=["collaboration"])


@router.post("/collaborate", response_model=CollaborationResponse)
async def collaborate(request: CollaborationRequest) -> CollaborationResponse:
    """
    智能体协作接口
    
    该接口用于启动智能体协作工作流，实现基于React范式的思考-行动循环。
    
    Args:
        request: 协作请求参数
            - task_goal: str, 必填, 任务目标
            - session_id: str, 必填, 会话ID
            - model: str, 必填, 选择的模型名称
        
    Returns:
        CollaborationResponse: 协作响应
            - session_id: str, 会话ID
            - task_goal: str, 任务目标
            - workflow_state: str, 工作流状态
            - result: Dict, 执行结果
            - error: Optional[str], 错误信息
            - execution_history: List[Dict], 执行历史
            - reflection_records: List[Dict], 反思记录
        
    典型调用场景:
        - 场景1: 启动多智能体协作完成复杂任务
        - 场景2: 基于特定目标执行智能体协作工作流
        
    与其他接口的关联关系:
        - 前置依赖接口: /api/scheduler/schedule (工作流调度)
        - 后续调用接口: /api/collaboration/status/{session_id} (获取协作状态)
        
    错误码定义:
        - 200: 成功
        - 400: 请求参数错误
        - 500: 服务器内部错误
    """
    try:
        # 构建协作状态
        collaboration_state = CollaborationState(
            task_goal=request.task_goal,
            session_id=request.session_id
        )
        
        # 添加请求参数到协作状态
        collaboration_state.request_params = {
            "model": request.model,
            "timeout": request.timeout,
            "priority": request.priority,
            "writing_style": request.writing_style,
            "medium_type": request.medium_type,
            "chapter_count": request.chapter_count,
            "models": request.models
        }
        
        # 执行工作流
        result = await collaboration_workflow.ainvoke(collaboration_state.to_dict())
        
        # 从结果中获取协作状态
        final_state = CollaborationState.from_dict(result)
        
        # 构建响应
        response = CollaborationResponse(
            session_id=final_state.session_id,
            task_goal=final_state.task_goal,
            workflow_state=final_state.workflow_state.value,
            result={
                "execution_history": [step.to_dict() for step in final_state.execution_history],
                "reflection_records": [record.to_dict() for record in final_state.reflection_records],
                "agent_states": {k: v.to_dict() for k, v in final_state.agent_states.items()}
            },
            error=None,
            execution_history=[step.to_dict() for step in final_state.execution_history],
            reflection_records=[record.to_dict() for record in final_state.reflection_records]
        )
        
        # 检查是否有错误
        if final_state.error_records:
            response.error = final_state.error_records[-1]["message"]
        
        return response
        
    except Exception as e:
        print(f"协作接口错误: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/status/{session_id}", response_model=CollaborationStatusResponse)
async def get_collaboration_status(session_id: str) -> CollaborationStatusResponse:
    """
    获取协作状态
    
    该接口用于获取指定会话的协作状态。
    
    Args:
        session_id: str, 必填, 会话ID
    
    Returns:
        CollaborationStatusResponse: 协作状态响应
            - session_id: str, 会话ID
            - status: str, 协作状态
            - message: str, 响应消息
    
    典型调用场景:
        - 场景1: 查看协作任务的执行状态
        - 场景2: 监控协作工作流的进展
    
    与其他接口的关联关系:
        - 前置依赖接口: /api/collaboration/collaborate (启动协作)
        - 后续调用接口: 无
    
    错误码定义:
        - 200: 成功
        - 500: 服务器内部错误
    """
    try:
        # 这里可以从存储中获取协作状态
        # 暂时返回一个示例响应
        return CollaborationStatusResponse(
            session_id=session_id,
            status="completed",
            message="协作状态查询功能正在开发中"
        )
    except Exception as e:
        print(f"获取协作状态错误: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/cancel/{session_id}", response_model=CollaborationCancelResponse)
async def cancel_collaboration(session_id: str) -> CollaborationCancelResponse:
    """
    取消协作
    
    该接口用于取消指定会话的协作。
    
    Args:
        session_id: str, 必填, 会话ID
    
    Returns:
        CollaborationCancelResponse: 协作取消响应
            - session_id: str, 会话ID
            - status: str, 取消状态
            - message: str, 响应消息
    
    典型调用场景:
        - 场景1: 取消长时间运行的协作任务
        - 场景2: 取消执行失败的协作任务
    
    与其他接口的关联关系:
        - 前置依赖接口: /api/collaboration/collaborate (启动协作)
        - 后续调用接口: 无
    
    错误码定义:
        - 200: 成功
        - 500: 服务器内部错误
    """
    try:
        # 这里可以实现取消协作的逻辑
        # 暂时返回一个示例响应
        return CollaborationCancelResponse(
            session_id=session_id,
            status="cancelled",
            message="协作取消功能正在开发中"
        )
    except Exception as e:
        print(f"取消协作错误: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
