from utils.async_llm import llm_manager
from core.config import settings
from typing import Dict, List, Any, Optional
import asyncio
import datetime
import time
import uuid
from .models import TaskProgress, StepProgress, Anomaly
from .storage import storage


class CoordinationSchedulerAgent:
    def __init__(self, model: str = None):
        self.model = model or settings.DEFAULT_MODEL
        self.llm = llm_manager.get_llm(self.model)
        self.workflow_steps = [
            {"id": "market_analysis", "name": "市场分析", "estimated_duration": 30},
            {"id": "creative_generation", "name": "创意生成", "estimated_duration": 60},
            {"id": "novel_writing", "name": "小说创作", "estimated_duration": 120},
            {"id": "script_writing", "name": "剧本编写", "estimated_duration": 90},
            {"id": "video_production", "name": "视频制作", "estimated_duration": 180},
            {"id": "content_review", "name": "内容审核", "estimated_duration": 45}
        ]
        self.available_agents = {
            "creative_generation": True,  # 已实现
            "novel_writing": True,  # 已实现
            "market_analysis": False,  # 未实现
            "script_writing": False,  # 未实现
            "video_production": False,  # 未实现
            "content_review": False  # 未实现
        }
    
    async def create_workflow_schedule(self, request_priority: int = 1) -> Dict[str, Any]:
        """
        创建工作时序表
        
        Args:
            request_priority: 请求优先级（1-5，5最高）
            
        Returns:
            工作时序表，包含各环节的开始时间、预计完成时间及依赖关系
        """
        start_time = datetime.datetime.now()
        schedule = []
        current_time = start_time
        
        for step in self.workflow_steps:
            # 计算优先级调整因子
            priority_factor = max(0.5, 1 - (request_priority - 1) * 0.1)
            adjusted_duration = int(step["estimated_duration"] * priority_factor)
            
            # 检查智能体是否可用
            agent_available = self.available_agents.get(step["id"], False)
            
            # 计算开始和结束时间
            step_start = current_time
            step_end = current_time + datetime.timedelta(minutes=adjusted_duration)
            
            # 添加到调度表
            schedule.append({
                "step_id": step["id"],
                "step_name": step["name"],
                "start_time": step_start.isoformat(),
                "estimated_end_time": step_end.isoformat(),
                "duration_minutes": adjusted_duration,
                "agent_available": agent_available,
                "priority": request_priority,
                "dependencies": [self.workflow_steps[i]["id"] for i in range(self.workflow_steps.index(step)) if i < self.workflow_steps.index(step)]
            })
            
            # 更新当前时间
            current_time = step_end
        
        return {
            "schedule": schedule,
            "created_at": start_time.isoformat(),
            "total_duration": (current_time - start_time).total_seconds() / 60
        }
    
    async def detect_conflicts(self, schedule: Dict[str, Any]) -> Dict[str, Any]:
        """
        检测潜在冲突
        
        Args:
            schedule: 工作时序表
            
        Returns:
            冲突检测结果，包含潜在冲突列表
        """
        conflicts = []
        
        # 检查智能体可用性冲突
        for step in schedule["schedule"]:
            if not step["agent_available"]:
                conflicts.append({
                    "conflict_id": f"agent_unavailable_{step['step_id']}",
                    "conflict_type": "agent_unavailable",
                    "step_id": step["step_id"],
                    "step_name": step["step_name"],
                    "description": f"{step['step_name']}环节的智能体尚未部署",
                    "severity": "medium"
                })
        
        # 检查时间冲突
        for i in range(len(schedule["schedule"])):
            for j in range(i + 1, len(schedule["schedule"])):
                step1 = schedule["schedule"][i]
                step2 = schedule["schedule"][j]
                if step1["estimated_end_time"] > step2["start_time"]:
                    conflicts.append({
                        "conflict_id": f"time_conflict_{step1['step_id']}_{step2['step_id']}",
                        "conflict_type": "time_conflict",
                        "step_id": step2["step_id"],
                        "step_name": step2["step_name"],
                        "description": f"{step2['step_name']}环节的开始时间早于{step1['step_name']}环节的预计结束时间",
                        "severity": "low"
                    })
        
        return {
            "conflicts": conflicts,
            "detected_at": datetime.datetime.now().isoformat(),
            "conflict_count": len(conflicts)
        }
    
    async def resolve_conflicts(self, conflict_detection: Dict[str, Any]) -> Dict[str, Any]:
        """
        解决冲突
        
        Args:
            conflict_detection: 冲突检测结果
            
        Returns:
            冲突解决结果，包含解决方案和预防措施
        """
        resolutions = []
        
        for conflict in conflict_detection["conflicts"]:
            if conflict["conflict_type"] == "agent_unavailable":
                resolutions.append({
                    "conflict_id": conflict["conflict_id"],
                    "resolution": "skip",
                    "description": f"跳过{conflict['step_name']}环节，因为相关智能体尚未部署",
                    "prevention": f"建议部署{conflict['step_name']}智能体以完善工作流程",
                    "status": "resolved"
                })
            elif conflict["conflict_type"] == "time_conflict":
                resolutions.append({
                    "conflict_id": conflict["conflict_id"],
                    "resolution": "adjust_time",
                    "description": f"调整{conflict['step_name']}环节的开始时间，确保在依赖环节完成后开始",
                    "prevention": "建议在创建调度表时考虑环节间的依赖关系",
                    "status": "resolved"
                })
        
        return {
            "resolutions": resolutions,
            "resolved_at": datetime.datetime.now().isoformat(),
            "resolved_count": len(resolutions)
        }
    
    async def allocate_resources(self, schedule: Dict[str, Any], request_priority: int = 1) -> Dict[str, Any]:
        """
        动态分配资源
        
        Args:
            schedule: 工作时序表
            request_priority: 请求优先级
            
        Returns:
            资源分配结果，包含计算资源和智能体资源分配情况
        """
        allocations = []
        
        for step in schedule["schedule"]:
            # 根据优先级分配资源
            resource_level = min(5, request_priority + 1)
            
            allocations.append({
                "step_id": step["step_id"],
                "step_name": step["step_name"],
                "cpu_allocation": f"{resource_level} cores",
                "memory_allocation": f"{resource_level * 2} GB",
                "agent_allocation": step["agent_available"],
                "priority": request_priority,
                "allocated_at": datetime.datetime.now().isoformat()
            })
        
        return {
            "allocations": allocations,
            "allocated_at": datetime.datetime.now().isoformat(),
            "total_resources": {
                "cpu_cores": sum([min(5, request_priority + 1) for _ in schedule["schedule"]]),
                "memory_gb": sum([min(5, request_priority + 1) * 2 for _ in schedule["schedule"]])
            }
        }
    
    async def adapt_agent_workflow(self, schedule: Dict[str, Any], story_type: str = "都市") -> Dict[str, Any]:
        """
        适配智能体工作流
        
        Args:
            schedule: 工作时序表
            story_type: 故事类型
            
        Returns:
            适配结果，包含可执行的步骤和类型定义
        """
        adapted_workflow = []
        skipped_steps = []
        
        # 定义步骤类型映射
        step_type_map = {
            "market_analysis": "creative_planning",
            "creative_generation": "creative_planning",
            "novel_writing": "novel_writing",
            "script_writing": "creative_planning",
            "video_production": "generic",
            "content_review": "quality_evaluation"
        }
        
        for step in schedule["schedule"]:
            step_type = step_type_map.get(step["step_id"], "generic")
            
            if step["agent_available"]:
                adapted_workflow.append({
                    "name": step["step_id"],
                    "type": step_type,
                    "params": {
                        "story_type": story_type,
                        "step_name": step["step_name"]
                    }
                })
            else:
                # 即使智能体不可用，也添加到工作流中作为通用步骤执行
                adapted_workflow.append({
                    "name": step["step_id"],
                    "type": "generic",
                    "params": {
                        "story_type": story_type,
                        "step_name": step["step_name"],
                        "note": "智能体尚未部署，使用通用方式执行"
                    }
                })
                skipped_steps.append({
                    "step_id": step["step_id"],
                    "step_name": step["step_name"],
                    "reason": "智能体尚未部署，使用通用方式执行",
                    "skipped_at": datetime.datetime.now().isoformat()
                })
        
        return {
            "adapted_workflow": adapted_workflow,
            "skipped_steps": skipped_steps,
            "adapted_at": datetime.datetime.now().isoformat(),
            "skipped_count": len(skipped_steps)
        }
    
    async def generate_scheduling_log(self, schedule: Dict[str, Any], resource_allocations: Dict[str, Any], adapted_workflow: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成工作流调度日志
        
        Args:
            schedule: 工作时序表
            resource_allocations: 资源分配结果
            adapted_workflow: 适配结果
            
        Returns:
            工作流调度日志，包含各环节的执行状态和资源分配情况
        """
        log_entries = []
        
        for step in schedule["schedule"]:
            allocation = next((a for a in resource_allocations["allocations"] if a["step_id"] == step["step_id"]), None)
            workflow_status = next((w for w in adapted_workflow["adapted_workflow"] if w["step_id"] == step["step_id"]), None)
            
            log_entries.append({
                "step_id": step["step_id"],
                "step_name": step["step_name"],
                "start_time": step["start_time"],
                "estimated_end_time": step["estimated_end_time"],
                "duration_minutes": step["duration_minutes"],
                "status": workflow_status["status"] if workflow_status else "unknown",
                "agent_available": step["agent_available"],
                "cpu_allocation": allocation["cpu_allocation"] if allocation else "N/A",
                "memory_allocation": allocation["memory_allocation"] if allocation else "N/A",
                "priority": step["priority"],
                "dependencies": step["dependencies"],
                "log_time": datetime.datetime.now().isoformat()
            })
        
        return {
            "log_entries": log_entries,
            "generated_at": datetime.datetime.now().isoformat(),
            "total_steps": len(log_entries),
            "included_steps": len([e for e in log_entries if e["status"] == "included"]),
            "skipped_steps": len([e for e in log_entries if e["status"] == "skipped"])
        }
    
    async def generate_exception_report(self, conflict_detection: Dict[str, Any], conflict_resolution: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成异常处理报告
        
        Args:
            conflict_detection: 冲突检测结果
            conflict_resolution: 冲突解决结果
            
        Returns:
            异常处理报告，包含冲突事件描述、处理过程和解决方案
        """
        exceptions = []
        
        for conflict in conflict_detection["conflicts"]:
            resolution = next((r for r in conflict_resolution["resolutions"] if r["conflict_id"] == conflict["conflict_id"]), None)
            
            exceptions.append({
                "conflict_id": conflict["conflict_id"],
                "conflict_type": conflict["conflict_type"],
                "step_name": conflict["step_name"],
                "description": conflict["description"],
                "severity": conflict["severity"],
                "resolution": resolution["resolution"] if resolution else "unresolved",
                "resolution_description": resolution["description"] if resolution else "N/A",
                "prevention": resolution["prevention"] if resolution else "N/A",
                "status": resolution["status"] if resolution else "unresolved"
            })
        
        return {
            "exceptions": exceptions,
            "generated_at": datetime.datetime.now().isoformat(),
            "total_exceptions": len(exceptions),
            "resolved_exceptions": len([e for e in exceptions if e["status"] == "resolved"]),
            "unresolved_exceptions": len([e for e in exceptions if e["status"] != "resolved"])
        }
    
    async def process_scheduling_request(self, request_priority: int = 1) -> Dict[str, Any]:
        """
        处理完整的调度请求
        
        Args:
            request_priority: 请求优先级
            
        Returns:
            完整的调度结果，包含工作时序表、资源分配、冲突处理和日志报告
        """
        # 1. 创建工作时序表
        schedule = await self.create_workflow_schedule(request_priority)
        
        # 2. 检测潜在冲突
        conflict_detection = await self.detect_conflicts(schedule)
        
        # 3. 解决冲突
        conflict_resolution = await self.resolve_conflicts(conflict_detection)
        
        # 4. 动态分配资源
        resource_allocations = await self.allocate_resources(schedule, request_priority)
        
        # 5. 适配智能体工作流
        adapted_workflow = await self.adapt_agent_workflow(schedule)
        
        # 6. 生成工作流调度日志
        scheduling_log = await self.generate_scheduling_log(schedule, resource_allocations, adapted_workflow)
        
        # 7. 生成异常处理报告
        exception_report = await self.generate_exception_report(conflict_detection, conflict_resolution)
        
        return {
            "schedule": schedule,
            "conflict_detection": conflict_detection,
            "conflict_resolution": conflict_resolution,
            "resource_allocations": resource_allocations,
            "adapted_workflow": adapted_workflow,
            "scheduling_log": scheduling_log,
            "exception_report": exception_report,
            "processed_at": datetime.datetime.now().isoformat()
        }
    
    async def plan_story_task(self, story_description: str, story_type: str) -> Dict[str, Any]:
        """
        故事创作任务规划
        
        Args:
            story_description: 故事详细描述文本
            story_type: 故事类型
            
        Returns:
            任务规划结果，包含整体设计和预计工作量
        """
        start_time = datetime.datetime.now()
        
        # 模拟任务规划过程
        print(f"Planning story task for {story_type} story...")
        print(f"Story description: {story_description[:100]}...")
        
        # 模拟不同故事类型的工作量
        type_duration_map = {
            "科幻": 180,  # 分钟
            "悬疑": 150,
            "爱情": 120,
            "奇幻": 160,
            "历史": 140,
            "都市": 100,
            "武侠": 130,
            "恐怖": 110,
        }
        
        estimated_duration = type_duration_map.get(story_type, 120)
        
        # 生成任务规划
        task_plan = {
            "story_type": story_type,
            "story_description": story_description,
            "plan": f"为{story_type}故事创建完整的创作计划，包括创意构思、情节设计、人物塑造和结局安排",
            "estimated_duration": estimated_duration,
            "key_phases": [
                "创意构思与大纲设计",
                "人物设定与关系构建",
                "情节发展与冲突设计",
                "细节描写与场景渲染",
                "结局设计与主题升华"
            ],
            "created_at": start_time.isoformat()
        }
        
        return task_plan
    
    async def breakdown_task(self, task_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        任务拆解
        
        Args:
            task_plan: 任务规划结果
            
        Returns:
            拆解后的子任务列表
        """
        start_time = datetime.datetime.now()
        story_type = task_plan.get("story_type", "未知")
        
        print(f"Breaking down task for {story_type} story...")
        
        # 基础子任务
        base_subtasks = [
            {
                "subtask_id": "subtask_1",
                "name": "创意构思与大纲设计",
                "description": "根据故事类型和描述，设计故事大纲和整体结构",
                "estimated_duration": 30,
                "agent_type": "creative",
                "priority": 1
            },
            {
                "subtask_id": "subtask_2",
                "name": "人物设定与关系构建",
                "description": "设计主要人物及其关系网络",
                "estimated_duration": 25,
                "agent_type": "creative",
                "priority": 2
            },
            {
                "subtask_id": "subtask_3",
                "name": "情节发展与冲突设计",
                "description": "设计故事的情节发展和主要冲突",
                "estimated_duration": 40,
                "agent_type": "creative",
                "priority": 3
            },
            {
                "subtask_id": "subtask_4",
                "name": "细节描写与场景渲染",
                "description": "为故事添加细节描写和场景渲染",
                "estimated_duration": 35,
                "agent_type": "script",
                "priority": 4
            },
            {
                "subtask_id": "subtask_5",
                "name": "结局设计与主题升华",
                "description": "设计故事结局并升华主题",
                "estimated_duration": 30,
                "agent_type": "script",
                "priority": 5
            }
        ]
        
        # 根据故事类型调整子任务
        if story_type == "科幻":
            base_subtasks.append({
                "subtask_id": "subtask_6",
                "name": "科幻元素设计",
                "description": "设计科幻故事中的科技元素和世界观",
                "estimated_duration": 30,
                "agent_type": "creative",
                "priority": 2
            })
        elif story_type == "悬疑":
            base_subtasks.append({
                "subtask_id": "subtask_6",
                "name": "悬疑元素设计",
                "description": "设计悬疑故事中的线索和谜题",
                "estimated_duration": 25,
                "agent_type": "creative",
                "priority": 3
            })
        elif story_type == "爱情":
            base_subtasks.append({
                "subtask_id": "subtask_6",
                "name": "情感线索设计",
                "description": "设计爱情故事中的情感发展线索",
                "estimated_duration": 20,
                "agent_type": "script",
                "priority": 3
            })
        
        task_breakdown = {
            "subtasks": base_subtasks,
            "total_subtasks": len(base_subtasks),
            "total_estimated_duration": sum(st["estimated_duration"] for st in base_subtasks),
            "breakdown_at": start_time.isoformat()
        }
        
        return task_breakdown
    
    async def allocate_tasks_to_agents(self, task_breakdown: Dict[str, Any]) -> Dict[str, Any]:
        """
        子任务分配给智能体
        
        Args:
            task_breakdown: 拆解后的子任务列表
            
        Returns:
            智能体分配结果
        """
        start_time = datetime.datetime.now()
        allocations = []
        
        print("Allocating subtasks to agents...")
        
        for subtask in task_breakdown.get("subtasks", []):
            # 分配智能体
            agent_type = subtask.get("agent_type", "creative")
            agent_name = "创意智能体" if agent_type == "creative" else "剧本智能体"
            
            allocation = {
                "subtask_id": subtask["subtask_id"],
                "subtask_name": subtask["name"],
                "agent_type": agent_type,
                "agent_name": agent_name,
                "estimated_duration": subtask["estimated_duration"],
                "priority": subtask["priority"],
                "allocated_at": start_time.isoformat()
            }
            
            allocations.append(allocation)
        
        # 统计分配情况
        creative_count = sum(1 for a in allocations if a["agent_type"] == "creative")
        script_count = sum(1 for a in allocations if a["agent_type"] == "script")
        
        agent_allocation = {
            "allocations": allocations,
            "allocated_at": start_time.isoformat(),
            "statistics": {
                "total_tasks": len(allocations),
                "creative_agent_tasks": creative_count,
                "script_agent_tasks": script_count
            }
        }
        
        return agent_allocation
    
    async def track_task_progress(self, agent_allocation: Dict[str, Any], story_type: str = "都市", session_id: str = None) -> Dict[str, Any]:
        """
        任务进度跟踪
        
        Args:
            agent_allocation: 智能体分配结果
            story_type: 故事类型
            session_id: 会话ID
            
        Returns:
            进度跟踪结果
        """
        start_time = datetime.datetime.now()
        
        print("Tracking task progress...")
        
        # 生成任务ID
        task_id = f"task_{uuid.uuid4()}"
        
        # 创建会话ID（如果未提供）
        if session_id is None:
            session_id = f"session_{uuid.uuid4()}"
        
        # 创建TaskProgress对象
        task_progress = TaskProgress(task_id, session_id, story_type)
        
        # 为每个子任务添加步骤
        allocations = agent_allocation.get("allocations", [])
        step_map = {}
        
        for allocation in allocations:
            step = task_progress.add_step(allocation["subtask_name"], allocation["agent_name"])
            step_map[allocation["subtask_id"]] = step.step_id
        
        # 模拟进度跟踪
        progress_updates = []
        total_tasks = len(allocations)
        
        for i, allocation in enumerate(allocations):
            # 模拟任务完成情况
            is_completed = i < total_tasks * 0.7  # 模拟70%的任务已完成
            progress = 100 if is_completed else 50
            status = "completed" if is_completed else "in_progress"
            
            # 更新步骤进度
            step_id = step_map[allocation["subtask_id"]]
            task_progress.update_step_progress(step_id, progress, status)
            
            progress_update = {
                "subtask_id": allocation["subtask_id"],
                "subtask_name": allocation["subtask_name"],
                "agent_name": allocation["agent_name"],
                "progress": progress,
                "status": status,
                "updated_at": start_time.isoformat()
            }
            
            progress_updates.append(progress_update)
        
        # 计算整体进度
        overall_progress = task_progress.progress
        
        # 保存到存储系统
        storage.save(task_progress)
        
        # 生成详细的进度跟踪结果
        progress_tracking = {
            "task_id": task_id,
            "session_id": session_id,
            "story_type": story_type,
            "progress_updates": progress_updates,
            "overall_progress": overall_progress,
            "status": task_progress.status,
            "tracking_at": start_time.isoformat(),
            "completed_tasks": task_progress.completed_steps,
            "total_tasks": task_progress.total_steps,
            "current_step": task_progress.current_step,
            "start_time": task_progress.start_time,
            "estimated_end_time": task_progress.estimated_end_time,
            "end_time": task_progress.end_time,
            "step_details": [
                {
                    "step_id": step.step_id,
                    "step_name": step.step_name,
                    "agent_name": step.agent_name,
                    "progress": step.progress,
                    "status": step.status,
                    "start_time": step.start_time,
                    "end_time": step.end_time,
                    "estimated_duration": step.estimated_duration,
                    "actual_duration": step.actual_duration
                }
                for step in task_progress.step_progress
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
                for anomaly in task_progress.anomalies
            ]
        }
        
        return progress_tracking
    
    async def get_task_progress(self, task_id: str) -> Dict[str, Any]:
        """
        获取任务进度
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务进度信息
        """
        progress = storage.get(task_id)
        if progress:
            return progress.to_dict()
        else:
            return {
                "error": "Task not found",
                "task_id": task_id
            }
    
    async def update_task_progress(self, task_id: str, step_id: str, progress: float, status: str = "running") -> Dict[str, Any]:
        """
        更新任务进度
        
        Args:
            task_id: 任务ID
            step_id: 步骤ID
            progress: 进度（0-100）
            status: 状态
            
        Returns:
            更新后的任务进度信息
        """
        task_progress = storage.get(task_id)
        if task_progress:
            task_progress.update_step_progress(step_id, progress, status)
            storage.save(task_progress)
            return task_progress.to_dict()
        else:
            return {
                "error": "Task not found",
                "task_id": task_id
            }
    
    async def list_tasks(self, session_id: str = None) -> List[Dict[str, Any]]:
        """
        列出所有任务
        
        Args:
            session_id: 会话ID（可选）
            
        Returns:
            任务列表
        """
        if session_id:
            tasks = storage.get_by_session(session_id)
        else:
            tasks = storage.list_all()
        
        return [task.to_dict() for task in tasks]
    
    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        """
        删除任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            删除结果
        """
        storage.delete(task_id)
        return {
            "message": "Task deleted successfully",
            "task_id": task_id
        }
    
    async def summarize_task_results(self, progress_tracking: Dict[str, Any]) -> Dict[str, Any]:
        """
        任务结果汇总
        
        Args:
            progress_tracking: 进度跟踪结果
            
        Returns:
            结果汇总
        """
        start_time = datetime.datetime.now()
        overall_progress = progress_tracking.get("overall_progress", 0)
        
        print(f"Summarizing task results with progress: {overall_progress:.1f}%")
        
        # 生成结果汇总
        result_summary = {
            "overall_progress": overall_progress,
            "status": "completed" if overall_progress >= 100 else "in_progress",
            "completed_tasks": progress_tracking.get("completed_tasks", 0),
            "total_tasks": progress_tracking.get("total_tasks", 0),
            "summary": f"任务已完成{overall_progress:.1f}%，共完成{progress_tracking.get('completed_tasks', 0)}个任务，总计{progress_tracking.get('total_tasks', 0)}个任务",
            "key_achievements": [
                "完成故事大纲设计",
                "构建主要人物关系",
                "设计核心情节冲突",
                "渲染关键场景细节"
            ],
            "next_steps": [
                "完成剩余任务",
                "整合所有内容",
                "进行质量评估",
                "提交最终结果"
            ],
            "completed_at": start_time.isoformat() if overall_progress >= 100 else None
        }
        
        return result_summary

    async def dynamic_planning(self, story_description: str, story_type: str, request_priority: int = 1) -> Dict[str, Any]:
        """
        动态规划 - 根据故事类型和内容生成动态执行计划
        
        这是新工作流的核心方法，替代原有的固定工作流步骤。
        根据故事描述分析需求，动态生成最适合的工作流步骤和智能体分配。
        
        Args:
            story_description: 故事详细描述
            story_type: 故事类型
            request_priority: 请求优先级
            
        Returns:
            动态执行计划，包含步骤列表、智能体分配、时间安排
        """
        start_time = datetime.datetime.now()
        
        print(f"开始动态规划: story_type={story_type}, priority={request_priority}")
        
        # 基于故事类型定义基础工作流模板
        type_workflow_templates = {
            "科幻": {
                "required_steps": ["creative_planning", "world_building", "novel_writing", "quality_evaluation"],
                "optional_steps": ["science_consulting"],
                "estimated_duration": 180
            },
            "悬疑": {
                "required_steps": ["creative_planning", "plot_design", "novel_writing", "quality_evaluation"],
                "optional_steps": ["logic_verification"],
                "estimated_duration": 150
            },
            "爱情": {
                "required_steps": ["creative_planning", "character_development", "novel_writing", "quality_evaluation"],
                "optional_steps": ["emotional_analysis"],
                "estimated_duration": 120
            },
            "奇幻": {
                "required_steps": ["creative_planning", "world_building", "novel_writing", "quality_evaluation"],
                "optional_steps": ["mythology_research"],
                "estimated_duration": 160
            },
            "历史": {
                "required_steps": ["creative_planning", "historical_research", "novel_writing", "quality_evaluation"],
                "optional_steps": ["expert_review"],
                "estimated_duration": 140
            },
            "都市": {
                "required_steps": ["creative_planning", "novel_writing", "quality_evaluation"],
                "optional_steps": ["trend_analysis"],
                "estimated_duration": 100
            },
            "武侠": {
                "required_steps": ["creative_planning", "martial_arts_design", "novel_writing", "quality_evaluation"],
                "optional_steps": ["culture_research"],
                "estimated_duration": 130
            },
            "恐怖": {
                "required_steps": ["creative_planning", "atmosphere_design", "novel_writing", "quality_evaluation"],
                "optional_steps": ["psychology_analysis"],
                "estimated_duration": 110
            }
        }
        
        # 获取模板
        template = type_workflow_templates.get(story_type, type_workflow_templates["都市"])
        
        # 根据优先级调整时间
        priority_factor = max(0.7, 1 - (request_priority - 1) * 0.08)
        base_duration = template["estimated_duration"]
        adjusted_duration = int(base_duration * priority_factor)
        
        # 构建执行步骤
        steps = []
        current_time = start_time
        step_duration = adjusted_duration // len(template["required_steps"])
        
        # 智能体类型映射
        step_agent_map = {
            "creative_planning": "CreativePlanningAgent",
            "world_building": "CreativePlanningAgent",
            "plot_design": "CreativePlanningAgent",
            "character_development": "CreativePlanningAgent",
            "historical_research": "CreativePlanningAgent",
            "martial_arts_design": "CreativePlanningAgent",
            "atmosphere_design": "CreativePlanningAgent",
            "novel_writing": "NovelWritingAgent",
            "quality_evaluation": "NovelWritingAgent"
        }
        
        for i, step_type in enumerate(template["required_steps"]):
            step_start = current_time
            step_end = current_time + datetime.timedelta(minutes=step_duration)
            
            steps.append({
                "step_id": f"step_{i+1}_{step_type}",
                "step_type": step_type,
                "step_name": self._get_step_name(step_type),
                "agent_type": step_agent_map.get(step_type, "GenericAgent"),
                "start_time": step_start.isoformat(),
                "estimated_end_time": step_end.isoformat(),
                "duration_minutes": step_duration,
                "priority": request_priority,
                "dependencies": [steps[j]["step_id"] for j in range(i)] if i > 0 else []
            })
            
            current_time = step_end
        
        # 构建执行计划
        execution_plan = {
            "plan_id": f"plan_{uuid.uuid4()}",
            "story_type": story_type,
            "story_description": story_description[:200] + "..." if len(story_description) > 200 else story_description,
            "request_priority": request_priority,
            "steps": steps,
            "total_steps": len(steps),
            "estimated_duration": adjusted_duration,
            "created_at": start_time.isoformat(),
            "plan_summary": f"为{story_type}故事设计的动态执行计划，包含{len(steps)}个核心步骤，预计耗时{adjusted_duration}分钟"
        }
        
        print(f"动态规划完成: {execution_plan['plan_summary']}")
        
        return execution_plan
    
    def _get_step_name(self, step_type: str) -> str:
        """获取步骤类型的中文名称"""
        name_map = {
            "creative_planning": "创意策划",
            "world_building": "世界观构建",
            "plot_design": "情节设计",
            "character_development": "人物塑造",
            "historical_research": "历史考证",
            "martial_arts_design": "武功设计",
            "atmosphere_design": "氛围设计",
            "novel_writing": "小说创作",
            "quality_evaluation": "质量评估"
        }
        return name_map.get(step_type, step_type)

    async def evaluate_and_decide(self, content: str, content_type: str = "novel", 
                                  quality_threshold: float = 75.0) -> Dict[str, Any]:
        """
        质量评估与决策 - 评估内容质量并决定是否需要优化
        
        这是新工作流的关键节点，支持迭代优化循环。
        
        Args:
            content: 需要评估的内容
            content_type: 内容类型 (novel/chapter/outline)
            quality_threshold: 质量阈值 (0-100)
            
        Returns:
            评估结果，包含质量分数、维度分析、决策建议
        """
        start_time = datetime.datetime.now()
        
        print(f"开始质量评估: content_type={content_type}, threshold={quality_threshold}")
        
        # 模拟多维度质量评估
        # 实际实现中应该使用LLM进行真正的质量评估
        content_length = len(content)
        
        # 基于内容长度和类型计算基础分数
        base_score = min(85, 60 + content_length / 100)
        
        # 多维度评估
        dimensions = {
            "readability": {
                "score": min(95, base_score + 10),
                "description": "可读性",
                "factors": ["语言流畅", "段落结构清晰", "过渡自然"]
            },
            "consistency": {
                "score": min(90, base_score + 5),
                "description": "一致性",
                "factors": ["人物设定一致", "情节逻辑连贯", "文风统一"]
            },
            "attractiveness": {
                "score": min(92, base_score + 8),
                "description": "吸引力",
                "factors": ["开头吸引人", "悬念设置合理", "情节有张力"]
            },
            "creativity": {
                "score": min(88, base_score + 3),
                "description": "创意性",
                "factors": ["情节新颖", "人物立体", "主题深刻"]
            },
            "completeness": {
                "score": min(95, base_score + 10),
                "description": "完整性",
                "factors": ["结构完整", "结局合理", "伏笔回收"]
            }
        }
        
        # 计算综合分数
        overall_score = sum(d["score"] for d in dimensions.values()) / len(dimensions)
        
        # 生成问题列表
        issues = []
        if dimensions["readability"]["score"] < quality_threshold:
            issues.append({"dimension": "readability", "issue": "可读性有待提升", "severity": "medium"})
        if dimensions["consistency"]["score"] < quality_threshold:
            issues.append({"dimension": "consistency", "issue": "内容一致性需要改进", "severity": "high"})
        if dimensions["attractiveness"]["score"] < quality_threshold:
            issues.append({"dimension": "attractiveness", "issue": "情节吸引力不足", "severity": "medium"})
        
        # 生成优化建议
        suggestions = []
        if issues:
            suggestions.append("优化段落结构，提升阅读流畅度")
            suggestions.append("加强人物刻画，使角色更加立体")
            suggestions.append("增加情节转折，提升故事张力")
        
        # 决策逻辑
        needs_revision = overall_score < quality_threshold or any(i["severity"] == "high" for i in issues)
        
        # 决策建议
        if needs_revision:
            decision = "revise"
            decision_reason = f"综合评分{overall_score:.1f}低于阈值{quality_threshold}，需要优化"
        else:
            decision = "approve"
            decision_reason = f"综合评分{overall_score:.1f}达到要求，可以通过"
        
        evaluation_report = {
            "evaluation_id": f"eval_{uuid.uuid4()}",
            "content_type": content_type,
            "overall_score": round(overall_score, 1),
            "quality_threshold": quality_threshold,
            "dimensions": dimensions,
            "issues": issues,
            "suggestions": suggestions,
            "decision": decision,
            "decision_reason": decision_reason,
            "needs_revision": needs_revision,
            "evaluated_at": start_time.isoformat()
        }
        
        print(f"质量评估完成: score={overall_score:.1f}, decision={decision}")
        
        return evaluation_report

    async def integrate_results(self, creative_framework: Dict[str, Any], 
                                novel_content: Dict[str, Any],
                                quality_report: Dict[str, Any],
                                execution_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        结果整合 - 整合所有执行结果并生成最终报告
        
        Args:
            creative_framework: 创意框架结果
            novel_content: 小说内容结果
            quality_report: 质量评估报告
            execution_metadata: 执行元数据
            
        Returns:
            整合后的最终结果
        """
        start_time = datetime.datetime.now()
        
        print("开始结果整合...")
        
        # 计算执行指标
        start_time_obj = datetime.datetime.fromisoformat(execution_metadata.get("start_time", start_time.isoformat()))
        execution_time = (start_time - start_time_obj).total_seconds()
        
        # 统计字数
        word_count = novel_content.get("word_count", 0)
        if not word_count and "full_novel" in novel_content:
            word_count = len(novel_content["full_novel"])
        
        # 整合结果
        final_result = {
            "result_id": f"result_{uuid.uuid4()}",
            "response": "故事创作工作流已完成",
            "content": {
                "creative_framework": creative_framework,
                "novel_content": novel_content,
                "quality_report": quality_report
            },
            "execution_summary": {
                "total_time_seconds": execution_time,
                "word_count": word_count,
                "quality_score": quality_report.get("overall_score", 0),
                "steps_completed": execution_metadata.get("steps_completed", 0),
                "total_steps": execution_metadata.get("total_steps", 0)
            },
            "metrics": {
                "efficiency": round(word_count / max(execution_time / 60, 1), 2),  # 字/分钟
                "quality_level": "优秀" if quality_report.get("overall_score", 0) >= 85 else "良好" if quality_report.get("overall_score", 0) >= 70 else "待改进",
                "completion_rate": execution_metadata.get("steps_completed", 0) / max(execution_metadata.get("total_steps", 1), 1) * 100
            },
            "logs": {
                "execution_start": execution_metadata.get("start_time"),
                "execution_end": start_time.isoformat(),
                "key_milestones": execution_metadata.get("milestones", [])
            },
            "integrated_at": start_time.isoformat()
        }
        
        print(f"结果整合完成: word_count={word_count}, quality_score={quality_report.get('overall_score', 0)}")
        
        return final_result
