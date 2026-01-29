from typing import Dict, List, Any, Optional, Callable, TypeVar, Union
from datetime import datetime
import asyncio
import time
import traceback
import logging
import functools

from core.monitoring import monitoring_system

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 定义错误类型
class AgentError(Exception):
    """智能体错误基类"""
    def __init__(self, message: str, error_code: int = 500, retryable: bool = False):
        self.message = message
        self.error_code = error_code
        self.retryable = retryable
        super().__init__(self.message)

class ModelError(AgentError):
    """模型错误"""
    def __init__(self, message: str, error_code: int = 503, retryable: bool = True):
        super().__init__(message, error_code, retryable)

class NetworkError(AgentError):
    """网络错误"""
    def __init__(self, message: str, error_code: int = 502, retryable: bool = True):
        super().__init__(message, error_code, retryable)

class TimeoutError(AgentError):
    """超时错误"""
    def __init__(self, message: str, error_code: int = 408, retryable: bool = True):
        super().__init__(message, error_code, retryable)

class ValidationError(AgentError):
    """验证错误"""
    def __init__(self, message: str, error_code: int = 400, retryable: bool = False):
        super().__init__(message, error_code, retryable)

class ResourceError(AgentError):
    """资源错误"""
    def __init__(self, message: str, error_code: int = 507, retryable: bool = True):
        super().__init__(message, error_code, retryable)

# 重试装饰器
T = TypeVar('T')

def retry(max_retries: int = 3,
          retry_delay: float = 1.0,
          backoff_factor: float = 2.0,
          retryable_exceptions: tuple = (ModelError, NetworkError, TimeoutError, ResourceError),
          agent_type: Optional[str] = None):
    """重试装饰器"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            retries = 0
            current_delay = retry_delay
            
            while retries < max_retries:
                try:
                    result = await func(*args, **kwargs)
                    return result
                except retryable_exceptions as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"函数 {func.__name__} 执行失败，已达到最大重试次数: {e}")
                        if agent_type:
                            monitoring_system.record_error(agent_type)
                        raise
                    
                    logger.warning(f"函数 {func.__name__} 执行失败，将在 {current_delay:.2f} 秒后重试 ({retries}/{max_retries}): {e}")
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff_factor
                except Exception as e:
                    logger.error(f"函数 {func.__name__} 执行失败，非重试able异常: {e}")
                    if agent_type:
                        monitoring_system.record_error(agent_type)
                    raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            retries = 0
            current_delay = retry_delay
            
            while retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result
                except retryable_exceptions as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"函数 {func.__name__} 执行失败，已达到最大重试次数: {e}")
                        if agent_type:
                            monitoring_system.record_error(agent_type)
                        raise
                    
                    logger.warning(f"函数 {func.__name__} 执行失败，将在 {current_delay:.2f} 秒后重试 ({retries}/{max_retries}): {e}")
                    time.sleep(current_delay)
                    current_delay *= backoff_factor
                except Exception as e:
                    logger.error(f"函数 {func.__name__} 执行失败，非重试able异常: {e}")
                    if agent_type:
                        monitoring_system.record_error(agent_type)
                    raise
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

# 错误处理工具类
class ErrorHandler:
    """错误处理工具类"""
    @staticmethod
    def handle_error(error: Exception, agent_type: Optional[str] = None) -> Dict[str, Any]:
        """处理错误"""
        error_info = {
            "error_type": type(error).__name__,
            "message": str(error),
            "timestamp": datetime.now().isoformat(),
            "traceback": traceback.format_exc(),
            "retryable": False
        }
        
        # 记录错误
        logger.error(f"错误处理: {error_info['error_type']} - {error_info['message']}")
        
        # 记录到监控系统
        if agent_type:
            monitoring_system.record_error(agent_type)
        
        # 处理不同类型的错误
        if isinstance(error, AgentError):
            error_info["error_code"] = error.error_code
            error_info["retryable"] = error.retryable
        elif isinstance(error, asyncio.TimeoutError):
            error_info["error_code"] = 408
            error_info["retryable"] = True
            error_info["error_type"] = "TimeoutError"
        elif isinstance(error, ConnectionError):
            error_info["error_code"] = 502
            error_info["retryable"] = True
            error_info["error_type"] = "NetworkError"
        else:
            error_info["error_code"] = 500
            error_info["retryable"] = False
        
        return error_info
    
    @staticmethod
    def format_error_response(error: Exception) -> Dict[str, Any]:
        """格式化错误响应"""
        error_info = ErrorHandler.handle_error(error)
        
        return {
            "error": {
                "code": error_info.get("error_code", 500),
                "message": error_info["message"],
                "type": error_info["error_type"],
                "retryable": error_info["retryable"]
            }
        }
    
    @staticmethod
    def is_retryable(error: Exception) -> bool:
        """判断错误是否可重试"""
        if isinstance(error, AgentError):
            return error.retryable
        elif isinstance(error, (asyncio.TimeoutError, ConnectionError)):
            return True
        return False
    
    @staticmethod
    def get_error_code(error: Exception) -> int:
        """获取错误代码"""
        if isinstance(error, AgentError):
            return error.error_code
        elif isinstance(error, asyncio.TimeoutError):
            return 408
        elif isinstance(error, ConnectionError):
            return 502
        elif isinstance(error, ValueError):
            return 400
        elif isinstance(error, PermissionError):
            return 403
        else:
            return 500

# 异常捕获上下文管理器
class ErrorContext:
    """异常捕获上下文管理器"""
    def __init__(self, agent_type: Optional[str] = None, operation: Optional[str] = None):
        self.agent_type = agent_type
        self.operation = operation
    
    async def __aenter__(self):
        self.start_time = time.time()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            error_info = ErrorHandler.handle_error(exc_val, self.agent_type)
            logger.error(f"操作 {self.operation} 执行失败: {error_info['message']}")
        else:
            execution_time = time.time() - self.start_time
            if self.agent_type:
                monitoring_system.record_response_time(self.agent_type, execution_time)
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            error_info = ErrorHandler.handle_error(exc_val, self.agent_type)
            logger.error(f"操作 {self.operation} 执行失败: {error_info['message']}")
        else:
            execution_time = time.time() - self.start_time
            if self.agent_type:
                monitoring_system.record_response_time(self.agent_type, execution_time)

# 工具函数
def create_error_response(error: Exception, status_code: int = 500) -> Dict[str, Any]:
    """创建错误响应"""
    return ErrorHandler.format_error_response(error)

def handle_api_error(func: Callable) -> Callable:
    """API错误处理装饰器"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            error_response = ErrorHandler.format_error_response(e)
            error_code = ErrorHandler.get_error_code(e)
            from fastapi import HTTPException
            raise HTTPException(status_code=error_code, detail=error_response)
    
    return wrapper
