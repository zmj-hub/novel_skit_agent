from pydantic_settings import BaseSettings
from typing import Dict, Optional, List
from enum import Enum


class AgentType(str, Enum):
    """智能体类型枚举"""
    COORDINATION = "coordination"
    CREATIVE = "creative"
    STORY_SCRIPT = "story_script"


class ModelParameters(BaseSettings):
    """模型参数配置"""
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 2048
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


class AgentConfig(BaseSettings):
    """单个智能体配置"""
    model: str
    parameters: ModelParameters = ModelParameters()
    capabilities: List[str] = []
    max_instances: int = 1
    timeout: int = 300


class AgentConfigSettings(BaseSettings):
    """智能体配置设置"""
    # 默认智能体配置
    agents: Dict[AgentType, AgentConfig] = {
        AgentType.COORDINATION: AgentConfig(
            model="Qwen/Qwen3-235B-A22B-Instruct-2507",
            parameters=ModelParameters(
                temperature=0.6,
                top_p=0.95,
                max_tokens=4096
            ),
            capabilities=["task_distribution", "process_control", "cross_agent_communication"],
            max_instances=1
        ),
        AgentType.CREATIVE: AgentConfig(
            model="deepseek-chat",
            parameters=ModelParameters(
                temperature=0.8,
                top_p=0.9,
                max_tokens=2048
            ),
            capabilities=["creative_generation", "scenario_design", "concept_development"],
            max_instances=2
        ),
        AgentType.STORY_SCRIPT: AgentConfig(
            model="Qwen/Qwen3-30B-A3B-Instruct-2507",
            parameters=ModelParameters(
                temperature=0.7,
                top_p=0.9,
                max_tokens=3072
            ),
            capabilities=["script_writing", "content_optimization", "story_development"],
            max_instances=2
        )
    }
    
    # 智能体通信配置
    communication_timeout: int = 60
    communication_max_retries: int = 3
    communication_retry_delay: int = 5
    
    # 负载均衡配置
    load_balancing_enabled: bool = True
    load_balancing_strategy: str = "round_robin"  # round_robin, least_busy, random
    load_balancing_max_queue_size: int = 100
    
    # 监控配置
    monitoring_enabled: bool = True
    monitoring_metrics_interval: int = 30  # seconds
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = False
        extra = "allow"  # 允许额外的环境变量


# 创建全局配置实例
agent_config = AgentConfigSettings()


# 辅助函数
def get_agent_config(agent_type: AgentType) -> AgentConfig:
    """获取指定类型智能体的配置"""
    return agent_config.agents.get(agent_type, None)


def get_agent_model(agent_type: AgentType) -> str:
    """获取指定类型智能体的模型"""
    config = get_agent_config(agent_type)
    return config.model if config else None


def get_agent_parameters(agent_type: AgentType) -> ModelParameters:
    """获取指定类型智能体的模型参数"""
    config = get_agent_config(agent_type)
    return config.parameters if config else ModelParameters()


def update_agent_config(agent_type: AgentType, config: AgentConfig):
    """更新智能体配置"""
    agent_config.agents[agent_type] = config
