from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
from models.schemas import SchedulerRequest, SchedulerResponse, WorkflowSchedule, WorkflowLog, ExceptionReport
from agent.workflow import scheduler_workflow
from typing import Optional, Dict, Any, Set
import logging
import time
from datetime import datetime
import json
import asyncio

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scheduler", tags=["scheduler"])

# 存储会话进度的内存存储（实际生产环境应使用Redis等持久化存储）
session_progress_store: Dict[str, Dict[str, Any]] = {}

# WebSocket连接管理器
class ConnectionManager:
    def __init__(self):
        # 存储活动的WebSocket连接，格式: {session_id: {"websockets": Set[WebSocket], "last_progress": Dict}}
        self.active_connections: Dict[str, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """
        接受WebSocket连接
        
        Args:
            websocket: WebSocket连接对象
            session_id: 会话ID
        """
        await websocket.accept()
        
        if session_id not in self.active_connections:
            self.active_connections[session_id] = {
                "websockets": set(),
                "last_progress": None
            }
        
        self.active_connections[session_id]["websockets"].add(websocket)
        logger.info(f"WebSocket连接已建立: session_id={session_id}")
        
        # 发送当前进度（如果有）
        if session_id in session_progress_store:
            await self.send_personal_message(session_progress_store[session_id], websocket)
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        """
        断开WebSocket连接
        
        Args:
            websocket: WebSocket连接对象
            session_id: 会话ID
        """
        if session_id in self.active_connections:
            self.active_connections[session_id]["websockets"].discard(websocket)
            logger.info(f"WebSocket连接已断开: session_id={session_id}")
            
            # 如果没有连接了，清理
            if not self.active_connections[session_id]["websockets"]:
                del self.active_connections[session_id]
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """
        发送个人消息
        
        Args:
            message: 消息内容
            websocket: WebSocket连接对象
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"发送消息失败: {str(e)}")
    
    async def broadcast_progress(self, session_id: str, progress_data: Dict[str, Any]):
        """
        广播进度更新
        
        Args:
            session_id: 会话ID
            progress_data: 进度数据
        """
        if session_id in self.active_connections:
            # 更新最后进度
            self.active_connections[session_id]["last_progress"] = progress_data
            
            # 发送给所有连接的客户端
            disconnected_websockets = []
            for connection in self.active_connections[session_id]["websockets"]:
                try:
                    await connection.send_json(progress_data)
                except Exception as e:
                    logger.error(f"广播消息失败: {str(e)}")
                    disconnected_websockets.append(connection)
            
            # 清理断开的连接
            for websocket in disconnected_websockets:
                self.disconnect(websocket, session_id)


# 创建连接管理器实例
manager = ConnectionManager()


def validate_request_params(request: SchedulerRequest) -> None:
    """
    验证请求参数的有效性
    
    Args:
        request: 调度请求参数
        
    Raises:
        HTTPException: 如果参数无效
    """
    # 验证故事描述
    if not request.story_description or len(request.story_description.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="故事描述不能为空且长度至少为10个字符"
        )
    
    # 验证故事类型
    valid_story_types = ["科幻", "悬疑", "爱情", "奇幻", "历史", "都市", "武侠", "恐怖"]
    if not request.story_type or request.story_type not in valid_story_types:
        raise HTTPException(
            status_code=400,
            detail=f"故事类型必须是以下之一: {', '.join(valid_story_types)}"
        )
    
    # 验证优先级
    if not (1 <= request.request_priority <= 5):
        raise HTTPException(
            status_code=400,
            detail="优先级必须在1到5之间"
        )
    
    # 验证会话ID
    if not request.session_id or len(request.session_id.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="会话ID不能为空且长度至少为5个字符"
        )
    
    # 验证模型
    valid_models = ["qwen3-30b", "deepseek-chat", "gpt-4"]
    if not request.model or request.model not in valid_models:
        raise HTTPException(
            status_code=400,
            detail=f"模型必须是以下之一: {', '.join(valid_models)}"
        )


async def update_session_progress(session_id: str, update_data: Dict[str, Any]) -> None:
    """
    更新会话进度
    
    Args:
        session_id: 会话ID
        update_data: 进度更新数据
    """
    if session_id not in session_progress_store:
        session_progress_store[session_id] = {
            "updates": [],
            "overall_progress": 0,
            "status": "pending",
            "start_time": datetime.now().isoformat()
        }
    
    # 添加时间戳
    update_data["timestamp"] = datetime.now().isoformat()
    
    # 更新进度数据
    session_progress_store[session_id]["updates"].append(update_data)
    
    # 更新整体进度
    if "overall_progress" in update_data:
        session_progress_store[session_id]["overall_progress"] = update_data["overall_progress"]
    
    # 更新状态
    if "status" in update_data:
        session_progress_store[session_id]["status"] = update_data["status"]
    
    # 通过WebSocket广播进度更新
    await manager.broadcast_progress(session_id, session_progress_store[session_id])


@router.post("/schedule", response_model=SchedulerResponse)
async def create_schedule(request: SchedulerRequest) -> SchedulerResponse:
    """
    协同调度接口
    
    该接口用于创建故事创作工作流调度计划，包括任务规划、拆解、智能体分配、进度跟踪和结果汇总。
    
    Args:
        request: 调度请求参数
            - story_description: str, 必填, 故事详细描述文本
            - story_type: str, 必填, 故事类型
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
        - 场景1: 为故事创作任务创建完整的智能体协作计划
        - 场景2: 为不同类型的故事（科幻、悬疑、爱情等）分配相应的创作智能体
    
    与其他接口的关联关系:
        - 前置依赖接口: 无
        - 后续调用接口: /api/collaborate (智能体协作)
    
    错误码定义:
        - 200: 成功
        - 400: 请求参数错误
        - 500: 服务器内部错误
    """
    try:
        # 验证请求参数
        validate_request_params(request)
        
        # 记录开始时间
        start_time = datetime.now()
        logger.info(f"开始处理调度请求: session_id={request.session_id}, story_type={request.story_type}")
        
        # 初始化会话进度
        await update_session_progress(request.session_id, {
            "status": "starting",
            "message": "开始处理调度请求",
            "overall_progress": 0
        })
        
        # 构建工作流输入
        workflow_input = {
            "story_description": request.story_description,
            "story_type": request.story_type,
            "request_priority": request.request_priority,
            "session_id": request.session_id,
            "model": request.model,
            "progress_callback": lambda data: asyncio.create_task(update_session_progress(request.session_id, data))
        }
        
        # 执行工作流
        logger.info(f"执行工作流: session_id={request.session_id}")
        await update_session_progress(request.session_id, {
            "status": "running",
            "message": "执行工作流",
            "overall_progress": 10
        })
        
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
            processed_at=datetime.now().isoformat()
        )
        
        # 更新最终进度
        await update_session_progress(request.session_id, {
            "status": "completed",
            "message": "工作流调度已完成",
            "overall_progress": 100
        })
        
        # 记录结束时间
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        logger.info(f"调度请求处理完成: session_id={request.session_id}, execution_time={execution_time:.2f}s")
        
        return response
        
    except HTTPException as e:
        # 处理已知错误
        logger.error(f"请求参数错误: {str(e)}")
        raise
    except Exception as e:
        # 处理未知错误
        logger.error(f"服务器内部错误: {str(e)}")
        # 更新进度为失败
        if hasattr(request, 'session_id') and request.session_id:
            await update_session_progress(request.session_id, {
                "status": "failed",
                "message": f"处理失败: {str(e)}",
                "error": str(e)
            })
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")


@router.get("/progress/{session_id}")
async def get_session_progress(session_id: str):
    """
    获取会话进度
    
    Args:
        session_id: 会话ID
        
    Returns:
        Dict: 会话进度数据
    """
    if session_id not in session_progress_store:
        return JSONResponse(
            status_code=404,
            content={"detail": "会话不存在或未开始处理"}
        )
    
    return session_progress_store[session_id]


@router.get("/progress")
async def get_all_progress():
    """
    获取所有会话进度
    
    Returns:
        Dict: 所有会话进度数据
    """
    return session_progress_store


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket端点，用于实时推送进度更新
    
    Args:
        websocket: WebSocket连接对象
        session_id: 会话ID
    """
    await manager.connect(websocket, session_id)
    
    try:
        # 持续监听消息
        while True:
            # 接收消息（可选，这里我们主要是推送消息）
            data = await websocket.receive_text()
            logger.info(f"收到WebSocket消息: session_id={session_id}, data={data}")
            
            # 可以根据需要处理客户端发送的消息
            if data == "ping":
                await manager.send_personal_message({"type": "pong"}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
    except Exception as e:
        logger.error(f"WebSocket错误: {str(e)}")
        manager.disconnect(websocket, session_id)
