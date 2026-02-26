from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
from models.schemas import SchedulerRequest, SchedulerResponse, WorkflowSchedule, WorkflowLog, ExceptionReport
from agent.workflow import scheduler_workflow
from agent.storage import storage
from agent.anomaly import anomaly_monitor
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

# WebSocket连接管理器（增强版）
class ConnectionManager:
    """
    增强型WebSocket连接管理器
    
    特性：
    - 心跳检测机制（自动清理死连接）
    - 连接超时处理
    - 连接状态监控
    - 改进的错误处理和连接清理
    """
    
    def __init__(self):
        # 存储活动的WebSocket连接，格式: {session_id: {"websockets": Set[WebSocket], "last_progress": Dict, "last_heartbeat": datetime}}
        self.active_connections: Dict[str, Dict[str, Any]] = {}
        # 心跳超时时间（秒）
        self.heartbeat_timeout = 60
        # 启动心跳检测任务
        self._start_heartbeat_checker()
    
    def _start_heartbeat_checker(self):
        """启动心跳检测定时任务"""
        async def heartbeat_checker():
            while True:
                await asyncio.sleep(30)  # 每30秒检查一次
                await self._check_heartbeats()
        
        # 创建后台任务
        asyncio.create_task(heartbeat_checker())
        logger.info("心跳检测任务已启动")
    
    async def _check_heartbeats(self):
        """检查所有连接的心跳，清理超时连接"""
        current_time = datetime.now()
        sessions_to_remove = []
        
        for session_id, connection_data in self.active_connections.items():
            last_heartbeat = connection_data.get("last_heartbeat", current_time)
            elapsed = (current_time - last_heartbeat).total_seconds()
            
            # 如果超时，清理连接
            if elapsed > self.heartbeat_timeout:
                logger.warning(f"会话 {session_id} 心跳超时，清理连接")
                websockets = list(connection_data["websockets"])
                for ws in websockets:
                    try:
                        await ws.close()
                    except:
                        pass
                sessions_to_remove.append(session_id)
        
        # 移除超时会话
        for session_id in sessions_to_remove:
            if session_id in self.active_connections:
                del self.active_connections[session_id]
    
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
                "last_progress": None,
                "last_heartbeat": datetime.now(),
                "connected_at": datetime.now()
            }
        
        self.active_connections[session_id]["websockets"].add(websocket)
        self.active_connections[session_id]["last_heartbeat"] = datetime.now()
        
        logger.info(f"WebSocket连接已建立: session_id={session_id}, 当前连接数: {len(self.active_connections[session_id]['websockets'])}")
        
        # 发送连接确认消息
        await self.send_personal_message({
            "type": "connection_established",
            "session_id": session_id,
            "message": "WebSocket连接已成功建立",
            "timestamp": datetime.now().isoformat()
        }, websocket)
        
        # 发送当前进度（如果有）
        if session_id in session_progress_store:
            progress_data = session_progress_store[session_id].copy()
            progress_data["type"] = "progress_update"
            await self.send_personal_message(progress_data, websocket)
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        """
        断开WebSocket连接
        
        Args:
            websocket: WebSocket连接对象
            session_id: 会话ID
        """
        if session_id in self.active_connections:
            self.active_connections[session_id]["websockets"].discard(websocket)
            remaining = len(self.active_connections[session_id]["websockets"])
            logger.info(f"WebSocket连接已断开: session_id={session_id}, 剩余连接数: {remaining}")
            
            # 如果没有连接了，清理
            if remaining == 0:
                del self.active_connections[session_id]
                logger.info(f"会话 {session_id} 的所有连接已断开，清理会话数据")
    
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
            # 标记连接为断开
            raise
    
    async def broadcast_progress(self, session_id: str, progress_data: Dict[str, Any]):
        """
        广播进度更新（增强版）
        
        Args:
            session_id: 会话ID
            progress_data: 进度数据
        """
        if session_id not in self.active_connections:
            return
        
        # 确保进度数据包含必要字段
        enhanced_progress = self._enhance_progress_data(progress_data, session_id)
        
        # 更新最后进度
        self.active_connections[session_id]["last_progress"] = enhanced_progress
        
        # 发送给所有连接的客户端
        disconnected_websockets = []
        for connection in list(self.active_connections[session_id]["websockets"]):
            try:
                await connection.send_json(enhanced_progress)
            except Exception as e:
                logger.error(f"广播消息失败: {str(e)}")
                disconnected_websockets.append(connection)
        
        # 清理断开的连接
        for websocket in disconnected_websockets:
            self.disconnect(websocket, session_id)
    
    def _enhance_progress_data(self, progress_data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        增强进度数据，添加时间估算等字段
        
        Args:
            progress_data: 原始进度数据
            session_id: 会话ID
            
        Returns:
            增强后的进度数据
        """
        enhanced = progress_data.copy()
        
        # 确保类型字段
        if "type" not in enhanced:
            enhanced["type"] = "progress_update"
        
        # 添加会话ID
        enhanced["session_id"] = session_id
        
        # 添加时间戳
        if "timestamp" not in enhanced:
            enhanced["timestamp"] = datetime.now().isoformat()
        
        # 计算预计剩余时间
        if "overall_progress" in enhanced and enhanced["overall_progress"] > 0:
            if session_id in session_progress_store:
                start_time_str = session_progress_store[session_id].get("start_time")
                if start_time_str:
                    try:
                        start_time = datetime.fromisoformat(start_time_str)
                        elapsed = (datetime.now() - start_time).total_seconds()
                        progress = enhanced["overall_progress"]
                        
                        # 估算总时间 = 已用时间 / 进度百分比
                        if progress > 0:
                            estimated_total = elapsed / (progress / 100)
                            remaining = estimated_total - elapsed
                            enhanced["estimated_remaining_time"] = int(remaining)
                            enhanced["elapsed_time"] = int(elapsed)
                    except:
                        pass
        
        return enhanced
    
    def update_heartbeat(self, session_id: str):
        """更新会话心跳时间"""
        if session_id in self.active_connections:
            self.active_connections[session_id]["last_heartbeat"] = datetime.now()
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """获取连接统计信息"""
        stats = {
            "total_sessions": len(self.active_connections),
            "total_connections": sum(len(data["websockets"]) for data in self.active_connections.values()),
            "sessions": []
        }
        
        for session_id, data in self.active_connections.items():
            stats["sessions"].append({
                "session_id": session_id,
                "connection_count": len(data["websockets"]),
                "connected_at": data.get("connected_at", "").isoformat() if isinstance(data.get("connected_at"), datetime) else data.get("connected_at", ""),
                "last_heartbeat": data.get("last_heartbeat", "").isoformat() if isinstance(data.get("last_heartbeat"), datetime) else data.get("last_heartbeat", "")
            })
        
        return stats


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
    if not request.story_description or len(request.story_description.strip()) < 1:
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
    
    # 验证模型 - 使用配置中定义的所有有效模型
    from core.config import settings
    valid_models = list(settings.MODEL_PROVIDERS.keys())
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


@router.get("/tasks")
async def get_all_tasks():
    """
    获取所有任务
    
    Returns:
        List: 任务列表
    """
    tasks = storage.list_all()
    return [task.to_dict() for task in tasks]


@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """
    获取任务详情
    
    Args:
        task_id: 任务ID
        
    Returns:
        Dict: 任务详情
    """
    task = storage.get(task_id)
    if task:
        return task.to_dict()
    else:
        raise HTTPException(status_code=404, detail="任务不存在")


@router.get("/tasks/session/{session_id}")
async def get_tasks_by_session(session_id: str):
    """
    获取会话的所有任务
    
    Args:
        session_id: 会话ID
        
    Returns:
        List: 任务列表
    """
    tasks = storage.get_by_session(session_id)
    return [task.to_dict() for task in tasks]


@router.post("/tasks/{task_id}/progress")
async def update_task_progress(task_id: str, progress_data: Dict[str, Any]):
    """
    更新任务进度
    
    Args:
        task_id: 任务ID
        progress_data: 进度数据
        
    Returns:
        Dict: 更新后的任务进度
    """
    task = storage.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    step_id = progress_data.get("step_id")
    progress = progress_data.get("progress")
    status = progress_data.get("status", "running")
    
    if step_id and progress is not None:
        task.update_step_progress(step_id, progress, status)
        storage.save(task)
        
        # 监控异常
        anomaly_monitor.monitor_task(task_id)
        
        return task.to_dict()
    else:
        raise HTTPException(status_code=400, detail="缺少必要的参数: step_id 和 progress")


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket端点，用于实时推送进度更新（增强版）
    
    支持：
    - 心跳检测（ping/pong）
    - 连接状态管理
    - 任务查询
    - 进度同步
    
    Args:
        websocket: WebSocket连接对象
        session_id: 会话ID
    """
    await manager.connect(websocket, session_id)
    
    try:
        # 持续监听消息
        while True:
            # 接收消息
            data = await websocket.receive_text()
            logger.info(f"收到WebSocket消息: session_id={session_id}, data={data}")
            
            # 处理客户端发送的消息
            if data == "ping":
                # 心跳检测 - 更新心跳时间并响应pong
                manager.update_heartbeat(session_id)
                await manager.send_personal_message({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }, websocket)
            
            elif data == "get_progress":
                # 获取当前进度
                if session_id in session_progress_store:
                    progress_data = session_progress_store[session_id].copy()
                    progress_data["type"] = "progress_update"
                    await manager.send_personal_message(progress_data, websocket)
                else:
                    await manager.send_personal_message({
                        "type": "error",
                        "message": "会话不存在或未开始处理"
                    }, websocket)
            
            elif data.startswith("get_tasks"):
                # 获取会话的所有任务
                tasks = storage.get_by_session(session_id)
                await manager.send_personal_message({
                    "type": "tasks",
                    "tasks": [task.to_dict() for task in tasks],
                    "timestamp": datetime.now().isoformat()
                }, websocket)
            
            elif data.startswith("get_task:"):
                # 获取特定任务
                task_id = data.split(":")[1]
                task = storage.get(task_id)
                if task:
                    await manager.send_personal_message({
                        "type": "task",
                        "task": task.to_dict(),
                        "timestamp": datetime.now().isoformat()
                    }, websocket)
                else:
                    await manager.send_personal_message({
                        "type": "error",
                        "message": "任务不存在",
                        "timestamp": datetime.now().isoformat()
                    }, websocket)
            
            elif data == "get_stats":
                # 获取连接统计信息
                stats = manager.get_connection_stats()
                await manager.send_personal_message({
                    "type": "connection_stats",
                    "stats": stats,
                    "timestamp": datetime.now().isoformat()
                }, websocket)
            
            else:
                # 未知命令
                await manager.send_personal_message({
                    "type": "error",
                    "message": f"未知命令: {data}",
                    "timestamp": datetime.now().isoformat()
                }, websocket)
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket连接断开: session_id={session_id}")
        manager.disconnect(websocket, session_id)
    except Exception as e:
        logger.error(f"WebSocket错误: session_id={session_id}, error={str(e)}")
        manager.disconnect(websocket, session_id)


@router.websocket("/ws/task/{task_id}")
async def task_websocket_endpoint(websocket: WebSocket, task_id: str):
    """
    WebSocket端点，用于实时推送特定任务的进度更新
    
    Args:
        websocket: WebSocket连接对象
        task_id: 任务ID
    """
    await manager.connect(websocket, task_id)
    
    try:
        # 发送当前任务状态
        task = storage.get(task_id)
        if task:
            await manager.send_personal_message({
                "type": "task_status",
                "task": task.to_dict()
            }, websocket)
        
        # 持续监听消息
        while True:
            # 接收消息
            data = await websocket.receive_text()
            logger.info(f"收到任务WebSocket消息: task_id={task_id}, data={data}")
            
            # 处理消息
            if data == "ping":
                await manager.send_personal_message({"type": "pong"}, websocket)
            elif data == "get_status":
                # 获取任务状态
                task = storage.get(task_id)
                if task:
                    await manager.send_personal_message({
                        "type": "task_status",
                        "task": task.to_dict()
                    }, websocket)
                else:
                    await manager.send_personal_message({
                        "type": "error",
                        "message": "任务不存在"
                    }, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, task_id)
    except Exception as e:
        logger.error(f"任务WebSocket错误: {str(e)}")
        manager.disconnect(websocket, task_id)
