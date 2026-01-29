"""
监控装饰器模块
提供独立的监控装饰器，避免循环导入问题
"""
from typing import Callable, Any
import time


class SimpleMonitoringSystem:
    """简化的监控系统，不依赖其他模块"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._metrics = {}
        return cls._instance
    
    def record_response_time(self, agent_type: str, response_time: float):
        """记录响应时间"""
        if agent_type not in self._metrics:
            self._metrics[agent_type] = {
                "request_count": 0,
                "total_response_time": 0.0,
                "error_count": 0
            }
        self._metrics[agent_type]["request_count"] += 1
        self._metrics[agent_type]["total_response_time"] += response_time
    
    def record_error(self, agent_type: str):
        """记录错误"""
        if agent_type not in self._metrics:
            self._metrics[agent_type] = {
                "request_count": 0,
                "total_response_time": 0.0,
                "error_count": 0
            }
        self._metrics[agent_type]["error_count"] += 1
    
    def get_metrics(self, agent_type: str = None):
        """获取指标"""
        if agent_type:
            return self._metrics.get(agent_type, {})
        return self._metrics


# 创建全局简化监控系统实例
simple_monitoring_system = SimpleMonitoringSystem()


def monitor_execution_time(agent_type: str) -> Callable:
    """
    监控函数执行时间的装饰器（独立版本，不依赖其他模块）
    """
    def decorator(func: Callable) -> Callable:
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                response_time = time.time() - start_time
                simple_monitoring_system.record_response_time(agent_type, response_time)
                return result
            except Exception as e:
                response_time = time.time() - start_time
                simple_monitoring_system.record_response_time(agent_type, response_time)
                simple_monitoring_system.record_error(agent_type)
                raise
        
        def sync_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                response_time = time.time() - start_time
                simple_monitoring_system.record_response_time(agent_type, response_time)
                return result
            except Exception as e:
                response_time = time.time() - start_time
                simple_monitoring_system.record_response_time(agent_type, response_time)
                simple_monitoring_system.record_error(agent_type)
                raise
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator
