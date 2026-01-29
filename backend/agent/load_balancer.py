from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import asyncio
import heapq
import uuid

from agent.agent_collaboration import AgentType, ExecutionStatus
from agent.registry import agent_registry
from core.agent_config import agent_config
from core.redis import redis_manager


class Task:
    """任务类"""
    def __init__(self,
                 task_id: str = None,
                 agent_type: str = None,
                 task: str = None,
                 parameters: Dict[str, Any] = None,
                 priority: int = 1,
                 created_at: Optional[datetime] = None,
                 started_at: Optional[datetime] = None,
                 completed_at: Optional[datetime] = None,
                 status: str = "pending",
                 error: Optional[str] = None):
        self.task_id = task_id or f"task_{uuid.uuid4().hex[:12]}"
        self.agent_type = agent_type
        self.task = task
        self.parameters = parameters or {}
        self.priority = priority  # 1-5, 5最高
        self.created_at = created_at or datetime.now()
        self.started_at = started_at
        self.completed_at = completed_at
        self.status = status  # pending, running, completed, failed
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "task_id": self.task_id,
            "agent_type": self.agent_type,
            "task": self.task,
            "parameters": self.parameters,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status,
            "error": self.error
        }

    def __lt__(self, other):
        """用于优先队列排序"""
        # 优先级高的任务排在前面
        return self.priority > other.priority


class LoadBalancer:
    """负载均衡器"""
    def __init__(self):
        # 任务队列（优先队列）
        self.task_queue = []
        # 正在执行的任务
        self.running_tasks: Dict[str, Task] = {}
        # 智能体实例使用情况
        self.agent_instance_usage: Dict[str, List[bool]] = {}
        # 锁
        self.lock = asyncio.Lock()
        # 初始化智能体实例使用情况
        self._init_agent_instance_usage()

    def _init_agent_instance_usage(self):
        """初始化智能体实例使用情况"""
        available_agents = agent_registry.get_available_agents()
        for agent_info in available_agents:
            self.agent_instance_usage[agent_info.agent_type] = [False] * agent_info.max_instances

    async def add_task(self, agent_type: str, task: str, parameters: Dict[str, Any], priority: int = 1) -> str:
        """添加任务到队列"""
        async with self.lock:
            # 创建任务
            new_task = Task(
                agent_type=agent_type,
                task=task,
                parameters=parameters,
                priority=priority
            )

            # 添加到优先队列
            heapq.heappush(self.task_queue, new_task)
            print(f"任务已添加到队列: {new_task.task_id}, 智能体类型: {agent_type}, 优先级: {priority}")

            # 尝试执行任务
            await self._process_tasks()

            return new_task.task_id

    async def _process_tasks(self):
        """处理任务队列"""
        while self.task_queue:
            # 获取智能体可用实例
            available_agent_instance = await self._get_available_agent_instance()
            if not available_agent_instance:
                break

            agent_type, instance_index = available_agent_instance

            # 获取最高优先级的任务
            task = heapq.heappop(self.task_queue)
            task.status = "running"
            task.started_at = datetime.now()

            # 标记实例为使用中
            self.agent_instance_usage[agent_type][instance_index] = True

            # 存储正在执行的任务
            self.running_tasks[task.task_id] = task

            print(f"开始执行任务: {task.task_id}, 智能体类型: {agent_type}, 实例索引: {instance_index}")

            # 异步执行任务
            asyncio.create_task(self._execute_task(task, agent_type, instance_index))

    async def _get_available_agent_instance(self) -> Optional[Tuple[str, int]]:
        """获取可用的智能体实例"""
        for agent_type, usage_list in self.agent_instance_usage.items():
            for i, in_use in enumerate(usage_list):
                if not in_use:
                    return agent_type, i
        return None

    async def _execute_task(self, task: Task, agent_type: str, instance_index: int):
        """
        执行任务
        """
        try:
            # 检查任务结果缓存
            cached_result = await redis_manager.get_task_result(task.task_id)
            if cached_result:
                task.status = "completed"
                task.completed_at = datetime.now()
                print(f"任务执行完成（从缓存获取）: {task.task_id}")
                return

            # 获取智能体实例
            agent_instance = agent_registry.get_agent_instance(agent_type, model=task.parameters.get("model"))
            if not agent_instance:
                task.status = "failed"
                task.error = "无法获取智能体实例"
                task.completed_at = datetime.now()
                print(f"任务执行失败: {task.task_id}, 原因: 无法获取智能体实例")
                return

            # 执行任务
            if agent_type == AgentType.CREATIVE.value:
                if task.task == "生成故事创意框架":
                    result = await agent_instance.process_creative_request(
                        hotspots=task.parameters.get("hotspots", []),
                        story_type=task.parameters.get("story_type", "都市情感")
                    )
            elif agent_type == AgentType.STORY_SCRIPT.value:
                if task.task == "创作故事剧本":
                    result = await agent_instance.process_story_request(
                        creative_framework=task.parameters.get("creative_framework", ""),
                        style=task.parameters.get("style", "urban"),
                        medium_type=task.parameters.get("medium_type", "novel"),
                        chapter_count=task.parameters.get("chapter_count", 5)
                    )
            elif agent_type == AgentType.COORDINATION.value:
                if task.task == "协调智能体工作流":
                    result = await agent_instance.process_coordination_request(
                        task_goal=task.parameters.get("task_goal", ""),
                        request_priority=task.parameters.get("request_priority", 1)
                    )
            else:
                result = {"error": "未知的智能体类型"}

            # 存储任务结果到缓存
            await redis_manager.store_task_result(task.task_id, result)

            # 更新任务状态
            task.status = "completed"
            task.completed_at = datetime.now()
            print(f"任务执行完成: {task.task_id}")

        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            task.completed_at = datetime.now()
            print(f"任务执行失败: {task.task_id}, 错误: {e}")
        finally:
            # 释放智能体实例
            async with self.lock:
                self.agent_instance_usage[agent_type][instance_index] = False
                if task.task_id in self.running_tasks:
                    del self.running_tasks[task.task_id]

                # 尝试处理下一个任务
                await self._process_tasks()

    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        async with self.lock:
            # 检查正在执行的任务
            if task_id in self.running_tasks:
                return self.running_tasks[task_id].to_dict()

            # 检查任务队列
            for task in self.task_queue:
                if task.task_id == task_id:
                    return task.to_dict()

            return None

    async def get_queue_status(self) -> Dict[str, Any]:
        """获取队列状态"""
        async with self.lock:
            queue_size = len(self.task_queue)
            running_tasks_count = len(self.running_tasks)
            agent_usage = {}

            for agent_type, usage_list in self.agent_instance_usage.items():
                used_count = sum(usage_list)
                total_count = len(usage_list)
                agent_usage[agent_type] = {
                    "used": used_count,
                    "total": total_count,
                    "available": total_count - used_count
                }

            return {
                "queue_size": queue_size,
                "running_tasks_count": running_tasks_count,
                "agent_usage": agent_usage
            }

    async def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        async with self.lock:
            # 检查正在执行的任务
            if task_id in self.running_tasks:
                # 这里只能标记为失败，因为任务已经在执行
                task = self.running_tasks[task_id]
                task.status = "failed"
                task.error = "任务已取消"
                task.completed_at = datetime.now()
                print(f"任务已取消: {task_id}")
                return True

            # 检查任务队列
            new_queue = []
            task_found = False
            for task in self.task_queue:
                if task.task_id == task_id:
                    task_found = True
                    print(f"任务已从队列中移除: {task_id}")
                else:
                    new_queue.append(task)

            if task_found:
                # 重新构建优先队列
                self.task_queue = new_queue
                heapq.heapify(self.task_queue)
                return True

            return False

    async def get_load_balancing_strategy(self) -> str:
        """获取负载均衡策略"""
        return agent_config.load_balancing_strategy

    async def set_load_balancing_strategy(self, strategy: str) -> bool:
        """设置负载均衡策略"""
        if strategy in ["round_robin", "least_busy", "random"]:
            # 这里可以更新配置
            print(f"负载均衡策略已设置为: {strategy}")
            return True
        return False


# 创建全局负载均衡器实例
load_balancer = LoadBalancer()
