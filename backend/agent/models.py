from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Anomaly:
    """异常记录"""
    anomaly_id: str
    type: str  # 异常类型：timeout, error, progress_stuck, resource
    severity: str  # 严重程度：low, medium, high
    description: str  # 异常描述
    detected_at: str  # 检测时间
    resolved: bool = False  # 是否已解决
    resolution: str = ""  # 解决方案

    def __init__(self, type: str, severity: str, description: str):
        self.anomaly_id = str(uuid.uuid4())
        self.type = type
        self.severity = severity
        self.description = description
        self.detected_at = datetime.now().isoformat()
        self.resolved = False
        self.resolution = ""

@dataclass
class StepProgress:
    """步骤进度"""
    step_id: str
    step_name: str  # 步骤名称
    status: str  # 状态：pending, running, completed, failed, paused
    progress: float  # 步骤进度（0-100）
    start_time: str  # 开始时间
    end_time: Optional[str] = None  # 结束时间
    estimated_duration: int = 0  # 预计持续时间（分钟）
    actual_duration: int = 0  # 实际持续时间（分钟）
    agent_name: str = ""  # 执行智能体

    def __init__(self, step_name: str, agent_name: str = ""):
        self.step_id = str(uuid.uuid4())
        self.step_name = step_name
        self.status = "pending"
        self.progress = 0.0
        self.start_time = datetime.now().isoformat()
        self.end_time = None
        self.estimated_duration = 0
        self.actual_duration = 0
        self.agent_name = agent_name

    def update_progress(self, progress: float, status: str = "running"):
        """更新进度"""
        self.progress = min(100.0, max(0.0, progress))
        self.status = status
        if status == "completed" and not self.end_time:
            self.end_time = datetime.now().isoformat()
            # 计算实际持续时间
            start = datetime.fromisoformat(self.start_time)
            end = datetime.fromisoformat(self.end_time)
            self.actual_duration = int((end - start).total_seconds() / 60)

@dataclass
class TaskProgress:
    """任务进度"""
    task_id: str
    session_id: str  # 会话ID
    story_type: str  # 故事类型
    status: str  # 状态：pending, running, completed, failed, paused
    start_time: str  # 开始时间
    end_time: Optional[str] = None  # 结束时间
    estimated_end_time: Optional[str] = None  # 预计结束时间
    current_step: str = ""  # 当前步骤
    completed_steps: int = 0  # 已完成步骤数
    total_steps: int = 0  # 总步骤数
    progress: float = 0.0  # 整体进度（0-100）
    step_progress: List[StepProgress] = None  # 各步骤进度
    anomalies: List[Anomaly] = None  # 异常记录
    updated_at: str = ""  # 最后更新时间

    def __init__(self, task_id: str, session_id: str, story_type: str):
        self.task_id = task_id
        self.session_id = session_id
        self.story_type = story_type
        self.status = "pending"
        self.start_time = datetime.now().isoformat()
        self.end_time = None
        self.estimated_end_time = None
        self.current_step = ""
        self.completed_steps = 0
        self.total_steps = 0
        self.progress = 0.0
        self.step_progress = []
        self.anomalies = []
        self.updated_at = self.start_time

    def add_step(self, step_name: str, agent_name: str = ""):
        """添加步骤"""
        step = StepProgress(step_name, agent_name)
        self.step_progress.append(step)
        self.total_steps = len(self.step_progress)
        self.updated_at = datetime.now().isoformat()
        return step

    def update_step_progress(self, step_id: str, progress: float, status: str = "running"):
        """更新步骤进度"""
        for step in self.step_progress:
            if step.step_id == step_id:
                step.update_progress(progress, status)
                # 更新整体进度
                completed = sum(1 for s in self.step_progress if s.status == "completed")
                self.completed_steps = completed
                if self.total_steps > 0:
                    self.progress = (completed / self.total_steps) * 100
                # 更新当前步骤
                if status == "running":
                    self.current_step = step.step_name
                # 更新整体状态
                if self.progress >= 100:
                    self.status = "completed"
                    self.end_time = datetime.now().isoformat()
                else:
                    self.status = "running"
                self.updated_at = datetime.now().isoformat()
                break

    def add_anomaly(self, anomaly: Anomaly):
        """添加异常"""
        self.anomalies.append(anomaly)
        self.updated_at = datetime.now().isoformat()

    def to_dict(self):
        """转换为字典"""
        return {
            "task_id": self.task_id,
            "session_id": self.session_id,
            "story_type": self.story_type,
            "status": self.status,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "estimated_end_time": self.estimated_end_time,
            "current_step": self.current_step,
            "completed_steps": self.completed_steps,
            "total_steps": self.total_steps,
            "progress": self.progress,
            "step_progress": [
                {
                    "step_id": step.step_id,
                    "step_name": step.step_name,
                    "status": step.status,
                    "progress": step.progress,
                    "start_time": step.start_time,
                    "end_time": step.end_time,
                    "estimated_duration": step.estimated_duration,
                    "actual_duration": step.actual_duration,
                    "agent_name": step.agent_name
                }
                for step in self.step_progress
            ],
            "anomalies": [
                {
                    "anomaly_id": anomaly.anomaly_id,
                    "type": anomaly.type,
                    "severity": anomaly.severity,
                    "description": anomaly.description,
                    "detected_at": anomaly.detected_at,
                    "resolved": anomaly.resolved,
                    "resolution": anomaly.resolution
                }
                for anomaly in self.anomalies
            ],
            "updated_at": self.updated_at
        }
