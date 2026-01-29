from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from core.config import settings

router = APIRouter(prefix="/example", tags=["example"])


@router.get("/chat")
async def get_chat_example():
    """
    获取对话接口示例
    
    该接口用于获取对话接口的示例请求和响应，帮助开发者了解如何使用对话接口。
    
    Args:
        无
    
    Returns:
        Dict[str, Any]: 对话接口示例
            - endpoint: str, 接口路径
            - method: str, 请求方法
            - example_request: Dict, 示例请求
            - example_response: Dict, 示例响应
            - available_models: List[str], 可用模型列表
    
    典型调用场景:
        - 场景1: 开发者了解对话接口的使用方法
        - 场景2: 测试对话接口的请求和响应格式
    
    与其他接口的关联关系:
        - 前置依赖接口: 无
        - 后续调用接口: /api/chat (对话接口)
    
    错误码定义:
        - 200: 成功
        - 500: 服务器内部错误
    """
    example_request = ChatRequest(
        message="什么是 RAG 技术？",
        session_id="user_123",
        use_knowledge=True,
        model=settings.DEFAULT_MODEL
    )
    
    example_response = ChatResponse(
        response="RAG (Retrieval-Augmented Generation) 是一种结合了检索和生成的 AI 技术，它通过从外部知识库中检索相关信息，增强了大语言模型的生成能力，从而提高了回答的准确性和可靠性。",
        session_id="user_123",
        sources=[]
    )
    
    # 获取所有支持的模型
    available_models = list(settings.MODEL_PROVIDERS.keys())
    
    return {
        "endpoint": "/api/chat",
        "method": "POST",
        "example_request": example_request.model_dump(),
        "example_response": example_response.model_dump(),
        "available_models": available_models
    }


@router.get("/upload")
async def get_upload_example():
    """
    获取文件上传接口示例
    
    该接口用于获取文件上传接口的示例信息，帮助开发者了解如何使用文件上传接口。
    
    Args:
        无
    
    Returns:
        Dict[str, Any]: 文件上传接口示例
            - endpoint: str, 接口路径
            - method: str, 请求方法
            - content_type: str, 内容类型
            - fields: Dict, 表单字段
            - example_response: Dict, 示例响应
    
    典型调用场景:
        - 场景1: 开发者了解文件上传接口的使用方法
        - 场景2: 测试文件上传接口的请求和响应格式
    
    与其他接口的关联关系:
        - 前置依赖接口: 无
        - 后续调用接口: /api/upload (文件上传接口)
    
    错误码定义:
        - 200: 成功
        - 500: 服务器内部错误
    """
    return {
        "endpoint": "/api/upload",
        "method": "POST",
        "content_type": "multipart/form-data",
        "fields": {
            "file": "选择要上传的 PDF 或文本文件"
        },
        "example_response": {
            "filename": "example.pdf",
            "chunks_count": 10,
            "status": "success"
        }
    }


@router.get("/knowledge")
async def get_knowledge_example():
    """
    获取知识库接口示例
    
    该接口用于获取知识库接口的示例信息，帮助开发者了解如何使用知识库接口。
    
    Args:
        无
    
    Returns:
        Dict[str, Any]: 知识库接口示例
            - endpoints: Dict, 接口列表
            - example_response: Dict, 示例响应
    
    典型调用场景:
        - 场景1: 开发者了解知识库接口的使用方法
        - 场景2: 测试知识库接口的请求和响应格式
    
    与其他接口的关联关系:
        - 前置依赖接口: 无
        - 后续调用接口: /api/knowledge (知识库状态接口), /api/knowledge/clear (清空知识库接口)
    
    错误码定义:
        - 200: 成功
        - 500: 服务器内部错误
    """
    return {
        "endpoints": {
            "get_status": {
                "endpoint": "/api/knowledge",
                "method": "GET",
                "description": "获取知识库状态"
            },
            "clear": {
                "endpoint": "/api/knowledge/clear",
                "method": "POST",
                "description": "清空知识库"
            }
        },
        "example_response": {
            "document_count": 5,
            "vector_store_type": "chromadb",
            "status": "active"
        }
    }
