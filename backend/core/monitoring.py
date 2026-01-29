from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import time
import asyncio
import psutil
import threading
import json
import os


class Metrics:
    """性能指标类"""
    def __init__(self,
                 agent_type: str,
                 request_count: int = 0,
                 error_count: int = 0,
                 total_response_time: float = 0.0,
                 avg_response_time: float = 0.0,
                 min_response_time: float = float('inf'),
                 max_response_time: float = 0.0,
                 resource_usage: Dict[str, float] = None,
                 task_completion_rate: float = 0.0,
                 last_updated: Optional[datetime] = None):
        self.agent_type = agent_type
        self.request_count = request_count
        self.error_count = error_count
        self.total_response_time = total_response_time
        self.avg_response_time = avg_response_time
        self.min_response_time = min_response_time
        self.max_response_time = max_response_time
        self.resource_usage = resource_usage or {
            "cpu": 0.0,
            "memory": 0.0,
            "disk": 0.0
        }
        self.task_completion_rate = task_completion_rate
        self.last_updated = last_updated or datetime.now()

    def update_response_time(self, response_time: float):
        """更新响应时间"""
        self.request_count += 1
        self.total_response_time += response_time
        self.avg_response_time = self.total_response_time / self.request_count
        self.min_response_time = min(self.min_response_time, response_time)
        self.max_response_time = max(self.max_response_time, response_time)
        self.last_updated = datetime.now()

    def update_error(self):
        """更新错误计数"""
        self.error_count += 1
        self.last_updated = datetime.now()

    def update_resource_usage(self):
        """更新资源使用情况"""
        try:
            process = psutil.Process(os.getpid())
            self.resource_usage = {
                "cpu": process.cpu_percent(interval=0.1),
                "memory": process.memory_percent(),
                "disk": psutil.disk_usage('/').percent
            }
            self.last_updated = datetime.now()
        except Exception as e:
            print(f"更新资源使用情况失败: {e}")

    def update_task_completion_rate(self, completed_tasks: int, total_tasks: int):
        """更新任务完成率"""
        if total_tasks > 0:
            self.task_completion_rate = (completed_tasks / total_tasks) * 100
            self.last_updated = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "agent_type": self.agent_type,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "total_response_time": self.total_response_time,
            "avg_response_time": self.avg_response_time,
            "min_response_time": self.min_response_time,
            "max_response_time": self.max_response_time,
            "resource_usage": self.resource_usage,
            "task_completion_rate": self.task_completion_rate,
            "last_updated": self.last_updated.isoformat()
        }


class MonitoringSystem:
    """性能监控系统"""
    def __init__(self):
        self.metrics: Dict[str, Metrics] = {}
        self.lock = threading.Lock()
        self.metrics_interval = 30  # 默认值
        self.log_file = "logs/agent_monitoring.log"
        self._init_metrics()
        self._start_monitoring_thread()

    def _init_metrics(self):
        """初始化性能指标"""
        from agent.registry import agent_registry
        from core.agent_config import agent_config
        
        try:
            self.metrics_interval = agent_config.monitoring_metrics_interval
        except Exception:
            self.metrics_interval = 30
        
        available_agents = agent_registry.get_available_agents()
        for agent_info in available_agents:
            self.metrics[agent_info.agent_type] = Metrics(agent_type=agent_info.agent_type)

        # 添加系统级指标
        self.metrics["system"] = Metrics(agent_type="system")

    def _start_monitoring_thread(self):
        """启动监控线程"""
        threading.Thread(target=self._monitoring_loop, daemon=True).start()

    def _monitoring_loop(self):
        """监控循环"""
        while True:
            try:
                # 更新资源使用情况
                self._update_all_resource_usage()
                
                # 记录指标
                self._log_metrics()
                
                # 等待指定时间
                time.sleep(self.metrics_interval)
            except Exception as e:
                print(f"监控循环错误: {e}")
                time.sleep(5)

    def _update_all_resource_usage(self):
        """更新所有智能体的资源使用情况"""
        with self.lock:
            for metrics in self.metrics.values():
                metrics.update_resource_usage()

    def _log_metrics(self):
        """记录指标到日志文件"""
        try:
            # 确保日志目录存在
            log_dir = os.path.dirname(self.log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # 写入日志
            with open(self.log_file, "a", encoding="utf-8") as f:
                timestamp = datetime.now().isoformat()
                metrics_data = {}
                with self.lock:
                    for agent_type, metrics in self.metrics.items():
                        metrics_data[agent_type] = metrics.to_dict()
                
                log_entry = {
                    "timestamp": timestamp,
                    "metrics": metrics_data
                }
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"记录指标失败: {e}")

    def record_response_time(self, agent_type: str, response_time: float):
        """记录响应时间"""
        with self.lock:
            if agent_type not in self.metrics:
                self.metrics[agent_type] = Metrics(agent_type=agent_type)
            self.metrics[agent_type].update_response_time(response_time)

    def record_error(self, agent_type: str):
        """记录错误"""
        with self.lock:
            if agent_type not in self.metrics:
                self.metrics[agent_type] = Metrics(agent_type=agent_type)
            self.metrics[agent_type].update_error()

    def record_task_completion(self, agent_type: str, completed_tasks: int, total_tasks: int):
        """记录任务完成情况"""
        with self.lock:
            if agent_type not in self.metrics:
                self.metrics[agent_type] = Metrics(agent_type=agent_type)
            self.metrics[agent_type].update_task_completion_rate(completed_tasks, total_tasks)

    def get_metrics(self, agent_type: Optional[str] = None) -> Dict[str, Any]:
        """获取性能指标"""
        with self.lock:
            if agent_type:
                if agent_type in self.metrics:
                    return self.metrics[agent_type].to_dict()
                else:
                    return {}
            else:
                return {
                    agent_type: metrics.to_dict()
                    for agent_type, metrics in self.metrics.items()
                }

    def get_agent_metrics(self) -> Dict[str, Any]:
        """获取智能体性能指标"""
        with self.lock:
            agent_metrics = {}
            for agent_type, metrics in self.metrics.items():
                if agent_type != "system":
                    agent_metrics[agent_type] = metrics.to_dict()
            return agent_metrics

    def get_system_metrics(self) -> Dict[str, Any]:
        """获取系统性能指标"""
        with self.lock:
            if "system" in self.metrics:
                return self.metrics["system"].to_dict()
            else:
                return {}

    def get_metrics_summary(self) -> Dict[str, Any]:
        """获取指标摘要"""
        with self.lock:
            summary = {
                "total_requests": 0,
                "total_errors": 0,
                "avg_response_time": 0.0,
                "system_resource_usage": {},
                "agent_metrics": {}
            }

            total_response_time = 0.0
            total_requests = 0

            for agent_type, metrics in self.metrics.items():
                if agent_type == "system":
                    summary["system_resource_usage"] = metrics.resource_usage
                else:
                    summary["total_requests"] += metrics.request_count
                    summary["total_errors"] += metrics.error_count
                    total_response_time += metrics.total_response_time
                    total_requests += metrics.request_count
                    summary["agent_metrics"][agent_type] = {
                        "request_count": metrics.request_count,
                        "error_count": metrics.error_count,
                        "avg_response_time": metrics.avg_response_time,
                        "task_completion_rate": metrics.task_completion_rate
                    }

            if total_requests > 0:
                summary["avg_response_time"] = total_response_time / total_requests

            return summary

    def clear_metrics(self, agent_type: Optional[str] = None):
        """清除指标"""
        with self.lock:
            if agent_type:
                if agent_type in self.metrics:
                    self.metrics[agent_type] = Metrics(agent_type=agent_type)
            else:
                self._init_metrics()


# 创建全局监控系统实例
monitoring_system = MonitoringSystem()


# 装饰器：用于监控函数执行时间
def monitor_execution_time(agent_type: str):
    """监控函数执行时间的装饰器"""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                response_time = time.time() - start_time
                monitoring_system.record_response_time(agent_type, response_time)
                return result
            except Exception as e:
                response_time = time.time() - start_time
                monitoring_system.record_response_time(agent_type, response_time)
                monitoring_system.record_error(agent_type)
                raise
        
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                response_time = time.time() - start_time
                monitoring_system.record_response_time(agent_type, response_time)
                return result
            except Exception as e:
                response_time = time.time() - start_time
                monitoring_system.record_response_time(agent_type, response_time)
                monitoring_system.record_error(agent_type)
                raise
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator
