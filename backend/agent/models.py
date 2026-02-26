from typing import List, Optional, Any, Dict
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


@dataclass
class StepExecutionReport:
    """步骤执行报告"""
    report_id: str  # 报告唯一ID
    task_id: str  # 所属任务ID
    session_id: str  # 会话ID
    step_name: str  # 步骤名称
    step_type: str  # 步骤类型
    step_index: int  # 步骤索引
    total_steps: int  # 总步骤数
    status: str  # 执行状态：completed, failed
    start_time: str  # 开始时间
    end_time: Optional[str]  # 结束时间
    execution_time: float  # 执行时长（秒）
    output: Any  # 详细输出内容
    error: Optional[str]  # 错误信息
    stack_trace: Optional[str]  # 异常堆栈信息
    created_at: str  # 报告创建时间

    def __init__(
        self,
        task_id: str,
        session_id: str,
        step_name: str,
        step_type: str,
        step_index: int,
        total_steps: int
    ):
        self.report_id = str(uuid.uuid4())
        self.task_id = task_id
        self.session_id = session_id
        self.step_name = step_name
        self.step_type = step_type
        self.step_index = step_index
        self.total_steps = total_steps
        self.status = "pending"
        self.start_time = datetime.now().isoformat()
        self.end_time = None
        self.execution_time = 0.0
        self.output = None
        self.error = None
        self.stack_trace = None
        self.created_at = datetime.now().isoformat()

    def mark_completed(self, output: Any):
        """标记为执行完成"""
        self.status = "completed"
        self.end_time = datetime.now().isoformat()
        self.output = output
        # 计算执行时长
        start = datetime.fromisoformat(self.start_time)
        end = datetime.fromisoformat(self.end_time)
        self.execution_time = (end - start).total_seconds()

    def mark_failed(self, error: str, stack_trace: Optional[str] = None):
        """标记为执行失败"""
        self.status = "failed"
        self.end_time = datetime.now().isoformat()
        self.error = error
        self.stack_trace = stack_trace
        # 计算执行时长
        start = datetime.fromisoformat(self.start_time)
        end = datetime.fromisoformat(self.end_time)
        self.execution_time = (end - start).total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "report_id": self.report_id,
            "task_id": self.task_id,
            "session_id": self.session_id,
            "step_name": self.step_name,
            "step_type": self.step_type,
            "step_index": self.step_index,
            "total_steps": self.total_steps,
            "status": self.status,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "execution_time": self.execution_time,
            "output": self.output,
            "error": self.error,
            "stack_trace": self.stack_trace,
            "created_at": self.created_at
        }


# ============================================
# 小说剧本创作系统数据模型
# ============================================

@dataclass
class CharacterMemory:
    """人物记忆 - 维护角色的完整记忆信息"""
    character_id: str
    name: str
    basic_info: Dict[str, Any]  # 基本信息：背景、性格、目标等
    experiences: List[Dict[str, Any]]  # 经历记录（按时间线）
    relationships: Dict[str, str]  # 关系网络 {角色名: 关系描述}
    long_term_memory: Dict[str, Any]  # 长期记忆（核心特质、重要经历）
    short_term_memory: List[Dict[str, Any]]  # 短期记忆（近期事件）
    memory_weights: Dict[str, float]  # 记忆权重 {记忆项: 权重值}
    created_at: str
    updated_at: str

    def __init__(self, character_id: str, name: str, basic_info: Dict[str, Any]):
        self.character_id = character_id
        self.name = name
        self.basic_info = basic_info
        self.experiences = []
        self.relationships = {}
        self.long_term_memory = {
            "core_traits": basic_info.get("personality", ""),
            "important_events": [],
            "beliefs": basic_info.get("motivation", "")
        }
        self.short_term_memory = []
        self.memory_weights = {}
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def add_experience(self, event: str, chapter: int, impact: str = "medium"):
        """添加经历记录"""
        experience = {
            "event": event,
            "chapter": chapter,
            "impact": impact,  # high/medium/low
            "timestamp": datetime.now().isoformat()
        }
        self.experiences.append(experience)
        
        # 根据影响程度更新记忆权重
        weight = 1.0 if impact == "high" else 0.6 if impact == "medium" else 0.3
        self.memory_weights[event] = weight
        
        # 添加到短期记忆
        self.short_term_memory.append(experience)
        # 保持短期记忆数量限制（最近10条）
        if len(self.short_term_memory) > 10:
            self.short_term_memory.pop(0)
        
        self.updated_at = datetime.now().isoformat()

    def update_relationship(self, character_name: str, relationship: str):
        """更新关系网络"""
        self.relationships[character_name] = relationship
        self.updated_at = datetime.now().isoformat()

    def get_weighted_memories(self, current_chapter: int) -> Dict[str, Any]:
        """获取加权后的记忆（用于创作上下文）"""
        # 长期记忆始终高权重
        weighted_memories = {
            "core_traits": self.long_term_memory["core_traits"],
            "recent_experiences": self.short_term_memory[-5:],  # 最近5条
            "important_past": [e for e in self.experiences if e.get("impact") == "high"],
            "relationships": self.relationships
        }
        return weighted_memories

    def to_dict(self) -> Dict[str, Any]:
        return {
            "character_id": self.character_id,
            "name": self.name,
            "basic_info": self.basic_info,
            "experiences": self.experiences,
            "relationships": self.relationships,
            "long_term_memory": self.long_term_memory,
            "short_term_memory": self.short_term_memory,
            "memory_weights": self.memory_weights,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


@dataclass
class Scene:
    """场景 - 剧本的基本单位"""
    scene_id: str
    setting: str  # 场景描述：时间、地点、环境
    characters_present: List[str]  # 在场角色
    dialogues: List[Dict[str, str]]  # 对话列表
    actions: str  # 动作指示
    emotional_tone: str  # 情感基调
    plot_progression: str  # 情节推进点

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "setting": self.setting,
            "characters_present": self.characters_present,
            "dialogues": self.dialogues,
            "actions": self.actions,
            "emotional_tone": self.emotional_tone,
            "plot_progression": self.plot_progression
        }


@dataclass
class ChapterScript:
    """章节剧本 - 完整的章节剧本内容"""
    chapter_number: int
    chapter_title: str
    overview: str  # 章节概述
    scenes: List[Scene]  # 场景列表
    key_events: List[str]  # 关键事件
    character_development: Dict[str, str]  # 角色发展 {角色名: 发展描述}
    emotional_arc: str  # 情感弧线
    word_count: int
    created_at: str

    def __init__(self, chapter_number: int, chapter_title: str, overview: str):
        self.chapter_number = chapter_number
        self.chapter_title = chapter_title
        self.overview = overview
        self.scenes = []
        self.key_events = []
        self.character_development = {}
        self.emotional_arc = ""
        self.word_count = 0
        self.created_at = datetime.now().isoformat()

    def add_scene(self, scene: Scene):
        """添加场景"""
        self.scenes.append(scene)
        # 更新字数统计
        scene_text = scene.setting + " " + scene.actions + " " + " ".join(
            d.get("content", "") for d in scene.dialogues
        )
        self.word_count += len(scene_text)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chapter_number": self.chapter_number,
            "chapter_title": self.chapter_title,
            "overview": self.overview,
            "scenes": [s.to_dict() for s in self.scenes],
            "key_events": self.key_events,
            "character_development": self.character_development,
            "emotional_arc": self.emotional_arc,
            "word_count": self.word_count,
            "created_at": self.created_at
        }


@dataclass
class ChapterContext:
    """章节创作上下文 - 创作时传递给智能体的完整上下文"""
    chapter_number: int
    chapter_overview: str  # 当前章节概述
    story_blueprint: Dict[str, Any]  # 故事蓝图
    character_memories: Dict[str, CharacterMemory]  # 相关人物记忆
    previous_chapters_summary: List[str]  # 前文关键信息摘要
    style_guide: Dict[str, Any]  # 风格指南

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chapter_number": self.chapter_number,
            "chapter_overview": self.chapter_overview,
            "story_blueprint": self.story_blueprint,
            "character_memories": {k: v.to_dict() for k, v in self.character_memories.items()},
            "previous_chapters_summary": self.previous_chapters_summary,
            "style_guide": self.style_guide
        }


@dataclass
class StoryBlueprint:
    """故事蓝图 - 完整的创作规划"""
    blueprint_id: str
    title: str
    genre: str  # 题材
    style: str  # 风格
    theme: str  # 核心主题
    total_chapters: int
    chapters: List[Dict[str, Any]]  # 每章规划 [{number, title, overview, key_points, scenes_plan}]
    characters: List[Dict[str, Any]]  # 人物列表
    created_at: str

    def __init__(self, title: str, genre: str, style: str, theme: str, total_chapters: int):
        self.blueprint_id = str(uuid.uuid4())
        self.title = title
        self.genre = genre
        self.style = style
        self.theme = theme
        self.total_chapters = total_chapters
        self.chapters = []
        self.characters = []
        self.created_at = datetime.now().isoformat()

    def add_chapter_plan(self, number: int, title: str, overview: str, key_points: List[str], scenes_plan: int):
        """添加章节规划"""
        self.chapters.append({
            "number": number,
            "title": title,
            "overview": overview,
            "key_points": key_points,
            "scenes_plan": scenes_plan
        })

    def add_character(self, name: str, role: str, background: str, personality: str, goals: str):
        """添加人物规划"""
        self.characters.append({
            "character_id": f"char_{uuid.uuid4().hex[:8]}",
            "name": name,
            "role": role,  # protagonist/antagonist/supporting
            "background": background,
            "personality": personality,
            "goals": goals
        })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "blueprint_id": self.blueprint_id,
            "title": self.title,
            "genre": self.genre,
            "style": self.style,
            "theme": self.theme,
            "total_chapters": self.total_chapters,
            "chapters": self.chapters,
            "characters": self.characters,
            "created_at": self.created_at
        }
