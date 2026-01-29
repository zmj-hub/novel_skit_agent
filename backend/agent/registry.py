from typing import Dict, List, Any, Optional, Type
from datetime import datetime
import importlib
import inspect

from agent.agent_collaboration import AgentType
from core.model_version import model_version_manager


class AgentInfo:
    """智能体信息"""
    def __init__(self,
                 agent_type: str,
                 name: str,
                 description: str,
                 capabilities: List[str],
                 class_name: str,
                 module_name: str,
                 model_name: Optional[str] = None,
                 max_instances: int = 1,
                 is_available: bool = True,
                 registered_at: Optional[datetime] = None):
        self.agent_type = agent_type
        self.name = name
        self.description = description
        self.capabilities = capabilities
        self.class_name = class_name
        self.module_name = module_name
        self.model_name = model_name
        self.max_instances = max_instances
        self.is_available = is_available
        self.registered_at = registered_at or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "agent_type": self.agent_type,
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
            "class_name": self.class_name,
            "module_name": self.module_name,
            "model_name": self.model_name,
            "max_instances": self.max_instances,
            "is_available": self.is_available,
            "registered_at": self.registered_at.isoformat()
        }


class AgentRegistry:
    """智能体注册器"""
    def __init__(self):
        self.agents: Dict[str, AgentInfo] = {}
        self.agent_instances: Dict[str, List[Any]] = {}
        self._initialized = False

    def _ensure_initialized(self):
        """确保已初始化"""
        if not self._initialized:
            self._register_default_agents()
            self._initialized = True

    def _register_default_agents(self):
        """注册默认智能体"""
        from core.model_version import model_version_manager
        
        # 注册创意策划智能体
        self.register_agent(
            agent_type=AgentType.CREATIVE.value,
            name="创意策划智能体",
            description="专注于创意生成与方案设计",
            capabilities=["creative_generation", "scenario_design", "concept_development"],
            class_name="CreativePlanningAgent",
            module_name="agent.creative_agent",
            model_name=model_version_manager.get_model_name("creative"),
            max_instances=2,
            is_available=True
        )

        # 注册故事剧本一体化智能体
        self.register_agent(
            agent_type=AgentType.STORY_SCRIPT.value,
            name="故事剧本一体化智能体",
            description="负责剧本内容的创作与优化",
            capabilities=["script_writing", "content_optimization", "story_development"],
            class_name="StoryScriptAgent",
            module_name="agent.story_script_agent",
            model_name=model_version_manager.get_model_name("story_script"),
            max_instances=2,
            is_available=True
        )

        # 注册协调智能体
        self.register_agent(
            agent_type=AgentType.COORDINATION.value,
            name="协调智能体",
            description="负责任务分发、流程控制与跨智能体通信",
            capabilities=["task_distribution", "process_control", "cross_agent_communication"],
            class_name="CoordinationAgent",
            module_name="agent.coordination_agent",
            model_name=model_version_manager.get_model_name("coordination"),
            max_instances=1,
            is_available=True
        )

    def register_agent(self,
                      agent_type: str,
                      name: str,
                      description: str,
                      capabilities: List[str],
                      class_name: str,
                      module_name: str,
                      model_name: Optional[str] = None,
                      max_instances: int = 1,
                      is_available: bool = True) -> bool:
        """注册智能体"""
        try:
            # 检查模块是否存在
            module = importlib.import_module(module_name)
            # 检查类是否存在
            agent_class = getattr(module, class_name)
            
            # 创建智能体信息
            agent_info = AgentInfo(
                agent_type=agent_type,
                name=name,
                description=description,
                capabilities=capabilities,
                class_name=class_name,
                module_name=module_name,
                model_name=model_name,
                max_instances=max_instances,
                is_available=is_available
            )
            
            # 注册智能体
            self.agents[agent_type] = agent_info
            self.agent_instances[agent_type] = []
            
            print(f"成功注册智能体: {name} ({agent_type})")
            return True
        except Exception as e:
            print(f"注册智能体失败: {e}")
            return False

    def unregister_agent(self, agent_type: str) -> bool:
        """注销智能体"""
        if agent_type in self.agents:
            # 清理实例
            if agent_type in self.agent_instances:
                self.agent_instances[agent_type] = []
            # 移除注册
            del self.agents[agent_type]
            print(f"成功注销智能体: {agent_type}")
            return True
        return False

    def get_agent_info(self, agent_type: str) -> Optional[AgentInfo]:
        """获取智能体信息"""
        self._ensure_initialized()
        return self.agents.get(agent_type)

    def get_available_agents(self) -> List[AgentInfo]:
        """获取所有可用的智能体"""
        self._ensure_initialized()
        return [info for info in self.agents.values() if info.is_available]

    def get_agent_by_capability(self, capability: str) -> List[AgentInfo]:
        """根据能力获取智能体"""
        self._ensure_initialized()
        return [info for info in self.agents.values() if capability in info.capabilities and info.is_available]

    def create_agent_instance(self, agent_type: str, **kwargs) -> Optional[Any]:
        """创建智能体实例"""
        self._ensure_initialized()
        agent_info = self.agents.get(agent_type)
        if not agent_info or not agent_info.is_available:
            return None

        # 检查实例数量是否达到上限
        instances = self.agent_instances.get(agent_type, [])
        if len(instances) >= agent_info.max_instances:
            # 如果达到上限，返回最早创建的实例
            return instances[0]

        try:
            # 动态导入模块和类
            module = importlib.import_module(agent_info.module_name)
            agent_class = getattr(module, agent_info.class_name)

            # 创建实例
            model = kwargs.get("model", agent_info.model_name)
            instance = agent_class(model=model)

            # 存储实例
            self.agent_instances[agent_type].append(instance)
            print(f"成功创建智能体实例: {agent_type}")
            return instance
        except Exception as e:
            print(f"创建智能体实例失败: {e}")
            return None

    def get_agent_instance(self, agent_type: str, **kwargs) -> Optional[Any]:
        """获取智能体实例"""
        self._ensure_initialized()
        # 尝试创建新实例
        instance = self.create_agent_instance(agent_type, **kwargs)
        if instance:
            return instance

        # 如果创建失败，返回现有实例
        instances = self.agent_instances.get(agent_type, [])
        return instances[0] if instances else None

    def release_agent_instance(self, agent_type: str, instance: Any) -> bool:
        """释放智能体实例"""
        self._ensure_initialized()
        instances = self.agent_instances.get(agent_type, [])
        if instance in instances:
            instances.remove(instance)
            print(f"成功释放智能体实例: {agent_type}")
            return True
        return False

    def update_agent_config(self, agent_type: str, **kwargs) -> bool:
        """更新智能体配置"""
        self._ensure_initialized()
        agent_info = self.agents.get(agent_type)
        if not agent_info:
            return False

        # 更新配置
        if "model_name" in kwargs:
            agent_info.model_name = kwargs["model_name"]
        if "max_instances" in kwargs:
            agent_info.max_instances = kwargs["max_instances"]
        if "is_available" in kwargs:
            agent_info.is_available = kwargs["is_available"]
        if "capabilities" in kwargs:
            agent_info.capabilities = kwargs["capabilities"]

        print(f"成功更新智能体配置: {agent_type}")
        return True

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        self._ensure_initialized()
        return {
            "agents": {k: v.to_dict() for k, v in self.agents.items()},
            "agent_instances_count": {k: len(v) for k, v in self.agent_instances.items()}
        }


# 创建全局智能体注册器实例
agent_registry = AgentRegistry()
