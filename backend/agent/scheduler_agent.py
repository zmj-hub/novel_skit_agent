from utils.async_llm import llm_manager
from core.config import settings
from typing import Dict, List, Any, Optional
import asyncio
import datetime
import time


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
    
    async def adapt_agent_workflow(self, schedule: Dict[str, Any]) -> Dict[str, Any]:
        """
        适配智能体工作流
        
        Args:
            schedule: 工作时序表
            
        Returns:
            适配结果，包含跳过的环节和原因
        """
        adapted_workflow = []
        skipped_steps = []
        
        for step in schedule["schedule"]:
            if step["agent_available"]:
                adapted_workflow.append({
                    "step_id": step["step_id"],
                    "step_name": step["step_name"],
                    "status": "included",
                    "reason": "智能体可用"
                })
            else:
                adapted_workflow.append({
                    "step_id": step["step_id"],
                    "step_name": step["step_name"],
                    "status": "skipped",
                    "reason": "智能体尚未部署"
                })
                skipped_steps.append({
                    "step_id": step["step_id"],
                    "step_name": step["step_name"],
                    "reason": "智能体尚未部署",
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
