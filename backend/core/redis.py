import redis
import json
from typing import List, Dict, Any, Optional, Union

from core.config import settings


class RedisManager:
    def __init__(self):
        self.pool = None
        self.initialized = False
        self.error = None
        # 内存缓存，用于频繁访问的数据
        self.memory_cache: Dict[str, Any] = {}
        # 内存缓存过期时间（秒）
        self.memory_cache_ttl = 300
    
    async def initialize(self):
        try:
            self.pool = redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                db=settings.REDIS_DB,
                decode_responses=True
            )
            # 测试连接
            conn = redis.Redis(connection_pool=self.pool)
            conn.ping()
            conn.close()
            self.initialized = True
            self.error = None
        except Exception as e:
            print(f"Warning: Failed to initialize Redis: {e}")
            print("Application will start, but chat history features will be unavailable until Redis is configured")
            self.error = str(e)
            self.initialized = False
    
    async def get_connection(self):
        if not self.initialized:
            await self.initialize()
        if not self.initialized:
            raise ValueError(f"Redis not initialized: {self.error}")
        return redis.Redis(connection_pool=self.pool)
    
    async def store_chat_history(self, session_id: str, history: List[Dict[str, Any]]):
        try:
            conn = await self.get_connection()
            key = f"chat:history:{session_id}"
            conn.setex(key, 86400, json.dumps(history))
            conn.close()
        except Exception as e:
            print(f"Warning: Failed to store chat history: {e}")
    
    async def get_chat_history(self, session_id: str) -> List[Dict[str, Any]]:
        try:
            conn = await self.get_connection()
            key = f"chat:history:{session_id}"
            data = conn.get(key)
            conn.close()
            if data:
                return json.loads(data)
            return []
        except Exception as e:
            print(f"Warning: Failed to get chat history: {e}")
            return []
    
    async def clear_chat_history(self, session_id: str):
        try:
            conn = await self.get_connection()
            key = f"chat:history:{session_id}"
            conn.delete(key)
            conn.close()
        except Exception as e:
            print(f"Warning: Failed to clear chat history: {e}")
    
    async def store_agent_response(self, agent_type: str, request_hash: str, response: Any, ttl: int = 3600):
        """
        存储智能体响应到Redis和内存缓存
        
        Args:
            agent_type: 智能体类型
            request_hash: 请求哈希值
            response: 响应数据
            ttl: 过期时间（秒）
        """
        try:
            # 存储到Redis
            conn = await self.get_connection()
            key = f"agent:response:{agent_type}:{request_hash}"
            conn.setex(key, ttl, json.dumps(response))
            conn.close()
        except Exception as e:
            print(f"Warning: Failed to store agent response: {e}")
        
        # 存储到内存缓存
        memory_key = f"agent:response:{agent_type}:{request_hash}"
        self.memory_cache[memory_key] = {
            "data": response,
            "expiry": time.time() + ttl
        }
    
    async def get_agent_response(self, agent_type: str, request_hash: str) -> Optional[Any]:
        """
        从内存缓存或Redis获取智能体响应
        
        Args:
            agent_type: 智能体类型
            request_hash: 请求哈希值
            
        Returns:
            响应数据，如果不存在返回None
        """
        # 先检查内存缓存
        memory_key = f"agent:response:{agent_type}:{request_hash}"
        if memory_key in self.memory_cache:
            cached_item = self.memory_cache[memory_key]
            if time.time() < cached_item["expiry"]:
                return cached_item["data"]
            else:
                # 过期，删除
                del self.memory_cache[memory_key]
        
        # 检查Redis
        try:
            conn = await self.get_connection()
            key = f"agent:response:{agent_type}:{request_hash}"
            data = conn.get(key)
            conn.close()
            if data:
                response = json.loads(data)
                # 更新内存缓存
                self.memory_cache[memory_key] = {
                    "data": response,
                    "expiry": time.time() + 3600
                }
                return response
        except Exception as e:
            print(f"Warning: Failed to get agent response: {e}")
        
        return None
    
    async def store_novel_chapters(self, session_id: str, chapters: List[Dict[str, Any]], ttl: int = 86400):
        """
        存储小说章节到Redis
        
        Args:
            session_id: 会话ID
            chapters: 章节列表
            ttl: 过期时间（秒）
        """
        try:
            conn = await self.get_connection()
            key = f"novel:chapters:{session_id}"
            conn.setex(key, ttl, json.dumps(chapters))
            conn.close()
        except Exception as e:
            print(f"Warning: Failed to store novel chapters: {e}")
    
    async def get_novel_chapters(self, session_id: str) -> List[Dict[str, Any]]:
        """
        从Redis获取小说章节
        
        Args:
            session_id: 会话ID
            
        Returns:
            章节列表，如果不存在返回空列表
        """
        try:
            conn = await self.get_connection()
            key = f"novel:chapters:{session_id}"
            data = conn.get(key)
            conn.close()
            if data:
                return json.loads(data)
            return []
        except Exception as e:
            print(f"Warning: Failed to get novel chapters: {e}")
            return []
    
    async def clear_novel_chapters(self, session_id: str):
        """
        清除小说章节
        
        Args:
            session_id: 会话ID
        """
        try:
            conn = await self.get_connection()
            key = f"novel:chapters:{session_id}"
            conn.delete(key)
            conn.close()
        except Exception as e:
            print(f"Warning: Failed to clear novel chapters: {e}")
    
    async def store_task_result(self, task_id: str, result: Any, ttl: int = 3600):
        """
        存储任务结果到Redis
        
        Args:
            task_id: 任务ID
            result: 任务结果
            ttl: 过期时间（秒）
        """
        try:
            conn = await self.get_connection()
            key = f"task:result:{task_id}"
            conn.setex(key, ttl, json.dumps(result))
            conn.close()
        except Exception as e:
            print(f"Warning: Failed to store task result: {e}")
    
    async def get_task_result(self, task_id: str) -> Optional[Any]:
        """
        从Redis获取任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务结果，如果不存在返回None
        """
        try:
            conn = await self.get_connection()
            key = f"task:result:{task_id}"
            data = conn.get(key)
            conn.close()
            if data:
                return json.loads(data)
        except Exception as e:
            print(f"Warning: Failed to get task result: {e}")
        
        return None
    
    async def clear_expired_cache(self):
        """
        清理过期的内存缓存
        """
        expired_keys = []
        current_time = time.time()
        
        for key, item in self.memory_cache.items():
            if current_time >= item["expiry"]:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.memory_cache[key]
    
    async def close(self):
        if self.pool:
            try:
                # Redis ConnectionPool 不需要显式关闭
                pass
            except Exception as e:
                print(f"Warning: Failed to close Redis connection: {e}")


import time

redis_manager = RedisManager()
