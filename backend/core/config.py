from pydantic_settings import BaseSettings
from typing import Optional, Dict
from .agent_config import agent_config, AgentType, get_agent_model, get_agent_config


class Settings(BaseSettings):
    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    DASHSCOPE_API_KEY: Optional[str] = None
    
    # Model Configuration
    DEFAULT_MODEL: str = "Qwen/Qwen3-30B-A3B-Instruct-2507"
    MODEL_PROVIDERS: Dict[str, str] = {
        "gpt-3.5-turbo": "openai",
        "gpt-4": "openai",
        "deepseek-chat": "deepseek",
        "deepseek-coder": "deepseek",
        "qwen-plus": "qwen",
        "qwen-turbo": "qwen",
        "qwen-vl-plus": "qwen-multimodal",
        "Qwen/Qwen3-30B-A3B-Instruct-2507": "modelscope",
        "Qwen/Qwen3-72B-A3B-Instruct": "modelscope",
        "Qwen/Qwen3-235B-A22B-Instruct-2507": "modelscope",
        "meta-llama/Meta-Llama-3-8B-Instruct": "modelscope",
        "meta-llama/Meta-Llama-3-70B-Instruct": "modelscope",
        "google/gemma-7b-it": "modelscope"
    }
    
    # ModelScope Configuration
    MODELSCOPE_API_KEY: Optional[str] = "ms-28a9e148-b281-404d-a7bf-4b732cb1a61e"
    MODELSCOPE_BASE_URL: str = "https://api-inference.modelscope.cn/v1"
    
    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = ""
    REDIS_DB: int = 0
    
    # Vector Database Configuration
    VECTOR_STORE_TYPE: str = "chromadb"
    VECTOR_STORE_PATH: str = "./vector_store"
    
    # Application Configuration
    APP_NAME: str = "Novel Skit Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Embedding Model
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # File Upload Configuration
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Security Configuration
    CORS_ORIGINS: str = "*"
    
    # Log Configuration
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "./logs"
    
    # Agent Configuration
    def get_agent_model(self, agent_type: AgentType) -> str:
        """获取指定类型智能体的模型"""
        return get_agent_model(agent_type)
    
    def get_agent_config(self, agent_type: AgentType):
        """获取指定类型智能体的配置"""
        return get_agent_config(agent_type)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
# 导出agent_config供其他模块使用
from .agent_config import agent_config as agent_config_settings

