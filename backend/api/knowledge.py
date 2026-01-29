from fastapi import APIRouter, HTTPException
from models.schemas import KnowledgeBaseStatus, ClearKnowledgeBaseResponse
from rag.retriever import retriever
from core.config import settings

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("", response_model=KnowledgeBaseStatus)
async def get_knowledge_base_status():
    """
    获取知识库状态接口
    
    该接口用于获取知识库的当前状态，包括文档数量、向量存储类型和状态。
    
    Args:
        无
    
    Returns:
        KnowledgeBaseStatus: 知识库状态
            - document_count: int, 知识库中的文档数量
            - vector_store_type: str, 向量存储类型
            - status: str, 知识库状态
    
    典型调用场景:
        - 场景1: 上传文件后查看知识库状态
        - 场景2: 定期检查知识库状态
    
    与其他接口的关联关系:
        - 前置依赖接口: /api/upload (文件上传)
        - 后续调用接口: 无
    
    错误码定义:
        - 200: 成功
        - 500: 服务器内部错误
    """
    try:
        document_count = retriever.get_document_count()
        
        status = KnowledgeBaseStatus(
            document_count=document_count,
            vector_store_type=settings.VECTOR_STORE_TYPE,
            status="active"
        )
        
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear", response_model=ClearKnowledgeBaseResponse)
async def clear_knowledge_base():
    """
    清空知识库接口
    
    该接口用于清空知识库中的所有文档。
    
    Args:
        无
    
    Returns:
        ClearKnowledgeBaseResponse: 清空结果
            - status: str, 操作状态
            - message: str, 操作消息
    
    典型调用场景:
        - 场景1: 知识库内容过时需要更新
        - 场景2: 测试环境清理
    
    与其他接口的关联关系:
        - 前置依赖接口: /api/knowledge (查看知识库状态)
        - 后续调用接口: /api/upload (重新上传文件)
    
    错误码定义:
        - 200: 成功
        - 500: 服务器内部错误
    """
    try:
        retriever.clear_knowledge_base()
        return ClearKnowledgeBaseResponse(status="success", message="Knowledge base cleared")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
