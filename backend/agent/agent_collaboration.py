from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime
import uuid


class WorkflowState(Enum):
    """工作流状态枚举"""
    INITIALIZED = "initialized"
    PLANNING = "planning"
    EXECUTING = "executing"
    REFLECTING = "reflecting"
    ERROR = "error"
    COMPLETED = "completed"


class AgentType(Enum):
    """智能体类型枚举"""
    CREATIVE = "creative"
    NOVEL = "novel"
    STORY_SCRIPT = "story_script"
    COORDINATION = "coordination"


class ExecutionStatus(Enum):
    """执行状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMED_OUT = "timed_out"


class ExecutionStep:
    """执行步骤"""
    def __init__(self,
                 step_id: str,
                 agent_type: AgentType,
                 task: str,
                 parameters: Dict[str, Any],
                 status: ExecutionStatus = ExecutionStatus.PENDING,
                 result: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None,
                 start_time: Optional[datetime] = None,
                 end_time: Optional[datetime] = None):
        self.step_id = step_id
        self.agent_type = agent_type
        self.task = task
        self.parameters = parameters
        self.status = status
        self.result = result
        self.error = error
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "step_id": self.step_id,
            "agent_type": self.agent_type.value,
            "task": self.task,
            "parameters": self.parameters,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None
        }


class ReflectionRecord:
    """反思记录"""
    def __init__(self,
                 reflection_id: str,
                 execution_history: List[ExecutionStep],
                 evaluation: str,
                 adjustment_needed: bool,
                 adjustment_reason: Optional[str] = None,
                 new_plan: Optional[List[Dict[str, Any]]] = None,
                 timestamp: Optional[datetime] = None):
        self.reflection_id = reflection_id
        self.execution_history = execution_history
        self.evaluation = evaluation
        self.adjustment_needed = adjustment_needed
        self.adjustment_reason = adjustment_reason
        self.new_plan = new_plan
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "reflection_id": self.reflection_id,
            "execution_history": [step.to_dict() for step in self.execution_history],
            "evaluation": self.evaluation,
            "adjustment_needed": self.adjustment_needed,
            "adjustment_reason": self.adjustment_reason,
            "new_plan": self.new_plan,
            "timestamp": self.timestamp.isoformat()
        }


class AgentState:
    """智能体状态"""
    def __init__(self,
                 agent_type: AgentType,
                 is_available: bool = True,
                 current_task: Optional[str] = None,
                 last_execution: Optional[datetime] = None,
                 error: Optional[str] = None):
        self.agent_type = agent_type
        self.is_available = is_available
        self.current_task = current_task
        self.last_execution = last_execution
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "agent_type": self.agent_type.value,
            "is_available": self.is_available,
            "current_task": self.current_task,
            "last_execution": self.last_execution.isoformat() if self.last_execution else None,
            "error": self.error
        }


class Message:
    """智能体间通信消息"""
    def __init__(self,
                 message_id: str = None,
                 sender: str = None,
                 recipient: str = None,
                 message_type: str = "task",
                 content: Dict[str, Any] = None,
                 status: str = "pending",
                 created_at: Optional[datetime] = None,
                 processed_at: Optional[datetime] = None):
        self.message_id = message_id or f"msg_{uuid.uuid4().hex[:12]}"
        self.sender = sender
        self.recipient = recipient
        self.message_type = message_type  # task, response, notification, error
        self.content = content or {}
        self.status = status  # pending, processing, processed, failed
        self.created_at = created_at or datetime.now()
        self.processed_at = processed_at

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "message_type": self.message_type,
            "content": self.content,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "processed_at": self.processed_at.isoformat() if self.processed_at else None
        }


class CollaborationState:
    """智能体协作状态"""
    def __init__(self,
                 task_goal: str,
                 session_id: str,
                 workflow_state: WorkflowState = WorkflowState.INITIALIZED,
                 current_plan: Optional[List[Dict[str, Any]]] = None,
                 execution_history: Optional[List[ExecutionStep]] = None,
                 reflection_records: Optional[List[ReflectionRecord]] = None,
                 agent_states: Optional[Dict[str, AgentState]] = None,
                 error_records: Optional[List[Dict[str, Any]]] = None,
                 request_params: Optional[Dict[str, Any]] = None,
                 messages: Optional[List[Message]] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.task_goal = task_goal
        self.session_id = session_id
        self.workflow_state = workflow_state
        self.current_plan = current_plan or []
        self.execution_history = execution_history or []
        self.reflection_records = reflection_records or []
        self.agent_states = agent_states or {
            AgentType.CREATIVE.value: AgentState(AgentType.CREATIVE),
            AgentType.NOVEL.value: AgentState(AgentType.NOVEL),
            AgentType.STORY_SCRIPT.value: AgentState(AgentType.STORY_SCRIPT),
            AgentType.COORDINATION.value: AgentState(AgentType.COORDINATION)
        }
        self.error_records = error_records or []
        self.request_params = request_params or {}
        self.messages = messages or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "task_goal": self.task_goal,
            "session_id": self.session_id,
            "workflow_state": self.workflow_state.value,
            "current_plan": self.current_plan,
            "execution_history": [step.to_dict() for step in self.execution_history],
            "reflection_records": [record.to_dict() for record in self.reflection_records],
            "agent_states": {k: v.to_dict() for k, v in self.agent_states.items()},
            "error_records": self.error_records,
            "request_params": self.request_params,
            "messages": [msg.to_dict() for msg in self.messages],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CollaborationState":
        """从字典创建实例"""
        execution_history = []
        for step_data in data.get("execution_history", []):
            step = ExecutionStep(
                step_id=step_data["step_id"],
                agent_type=AgentType(step_data["agent_type"]),
                task=step_data["task"],
                parameters=step_data["parameters"],
                status=ExecutionStatus(step_data["status"]),
                result=step_data.get("result"),
                error=step_data.get("error"),
                start_time=datetime.fromisoformat(step_data["start_time"]) if step_data.get("start_time") else None,
                end_time=datetime.fromisoformat(step_data["end_time"]) if step_data.get("end_time") else None
            )
            execution_history.append(step)

        reflection_records = []
        for record_data in data.get("reflection_records", []):
            reflection_execution_history = []
            for step_data in record_data.get("execution_history", []):
                step = ExecutionStep(
                    step_id=step_data["step_id"],
                    agent_type=AgentType(step_data["agent_type"]),
                    task=step_data["task"],
                    parameters=step_data["parameters"],
                    status=ExecutionStatus(step_data["status"]),
                    result=step_data.get("result"),
                    error=step_data.get("error"),
                    start_time=datetime.fromisoformat(step_data["start_time"]) if step_data.get("start_time") else None,
                    end_time=datetime.fromisoformat(step_data["end_time"]) if step_data.get("end_time") else None
                )
                reflection_execution_history.append(step)

            record = ReflectionRecord(
                reflection_id=record_data["reflection_id"],
                execution_history=reflection_execution_history,
                evaluation=record_data["evaluation"],
                adjustment_needed=record_data["adjustment_needed"],
                adjustment_reason=record_data.get("adjustment_reason"),
                new_plan=record_data.get("new_plan"),
                timestamp=datetime.fromisoformat(record_data["timestamp"]) if record_data.get("timestamp") else None
            )
            reflection_records.append(record)

        agent_states = {}
        for agent_type_str, agent_state_data in data.get("agent_states", {}).items():
            agent_state = AgentState(
                agent_type=AgentType(agent_type_str),
                is_available=agent_state_data["is_available"],
                current_task=agent_state_data.get("current_task"),
                last_execution=datetime.fromisoformat(agent_state_data["last_execution"]) if agent_state_data.get("last_execution") else None,
                error=agent_state_data.get("error")
            )
            agent_states[agent_type_str] = agent_state

        messages = []
        for msg_data in data.get("messages", []):
            msg = Message(
                message_id=msg_data["message_id"],
                sender=msg_data.get("sender"),
                recipient=msg_data.get("recipient"),
                message_type=msg_data.get("message_type", "task"),
                content=msg_data.get("content", {}),
                status=msg_data.get("status", "pending"),
                created_at=datetime.fromisoformat(msg_data["created_at"]) if msg_data.get("created_at") else None,
                processed_at=datetime.fromisoformat(msg_data["processed_at"]) if msg_data.get("processed_at") else None
            )
            messages.append(msg)

        return cls(
            task_goal=data["task_goal"],
            session_id=data["session_id"],
            workflow_state=WorkflowState(data["workflow_state"]),
            current_plan=data.get("current_plan"),
            execution_history=execution_history,
            reflection_records=reflection_records,
            agent_states=agent_states,
            error_records=data.get("error_records"),
            request_params=data.get("request_params"),
            messages=messages,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None
        )

    def send_message(self, sender: str, recipient: str, message_type: str, content: Dict[str, Any]) -> Message:
        """发送智能体间消息"""
        message = Message(
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            content=content
        )
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message

    def get_messages_for_recipient(self, recipient: str, status: str = "pending") -> List[Message]:
        """获取指定接收者的消息"""
        return [msg for msg in self.messages if msg.recipient == recipient and msg.status == status]

    def mark_message_processed(self, message_id: str, status: str = "processed") -> bool:
        """标记消息为已处理"""
        for msg in self.messages:
            if msg.message_id == message_id:
                msg.status = status
                msg.processed_at = datetime.now()
                self.updated_at = datetime.now()
                return True
        return False

    def process_messages(self, agent_type: str) -> List[Dict[str, Any]]:
        """处理智能体的待处理消息"""
        processed_results = []
        pending_messages = self.get_messages_for_recipient(agent_type, "pending")
        
        for msg in pending_messages:
            # 标记消息为处理中
            msg.status = "processing"
            
            try:
                # 处理消息内容
                result = {
                    "message_id": msg.message_id,
                    "sender": msg.sender,
                    "message_type": msg.message_type,
                    "content": msg.content,
                    "processed_at": datetime.now().isoformat()
                }
                processed_results.append(result)
                
                # 标记消息为已处理
                msg.status = "processed"
                msg.processed_at = datetime.now()
            except Exception as e:
                # 标记消息为处理失败
                msg.status = "failed"
                msg.processed_at = datetime.now()
                self.error_records.append({
                    "error_id": f"error_{uuid.uuid4().hex[:8]}",
                    "phase": "message_processing",
                    "message": f"Failed to process message {msg.message_id}: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                })
        
        if processed_results:
            self.updated_at = datetime.now()
        
        return processed_results


class CollaborationRequest:
    """协作请求"""
    def __init__(self,
                 task_goal: str,
                 session_id: str,
                 model: Optional[str] = None,
                 timeout: Optional[int] = None,
                 priority: Optional[int] = None):
        self.task_goal = task_goal
        self.session_id = session_id
        self.model = model
        self.timeout = timeout
        self.priority = priority

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "task_goal": self.task_goal,
            "session_id": self.session_id,
            "model": self.model,
            "timeout": self.timeout,
            "priority": self.priority
        }


class CollaborationResponse:
    """协作响应"""
    def __init__(self,
                 session_id: str,
                 task_goal: str,
                 workflow_state: WorkflowState,
                 result: Optional[Dict[str, Any]] = None,
                 error: Optional[str] = None,
                 execution_history: Optional[List[ExecutionStep]] = None,
                 reflection_records: Optional[List[ReflectionRecord]] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.session_id = session_id
        self.task_goal = task_goal
        self.workflow_state = workflow_state
        self.result = result
        self.error = error
        self.execution_history = execution_history or []
        self.reflection_records = reflection_records or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "session_id": self.session_id,
            "task_goal": self.task_goal,
            "workflow_state": self.workflow_state.value,
            "result": self.result,
            "error": self.error,
            "execution_history": [step.to_dict() for step in self.execution_history],
            "reflection_records": [record.to_dict() for record in self.reflection_records],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
