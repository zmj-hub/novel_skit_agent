from fastapi import APIRouter, HTTPException, UploadFile, File
from models.schemas import FileUploadResponse
from rag.processor import processor
from core.config import settings
import os

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    文件上传接口
    
    该接口用于上传PDF和文本文件，自动处理并添加到知识库。
    
    Args:
        file: UploadFile, 必填, 要上传的文件
            - filename: str, 文件名称
            - content: bytes, 文件内容
            - content_type: str, 文件类型
    
    Returns:
        FileUploadResponse: 文件上传响应
            - filename: str, 上传的文件名
            - chunks_count: int, 处理后的文件块数量
            - status: str, 上传状态
    
    典型调用场景:
        - 场景1: 上传PDF文档到知识库
        - 场景2: 上传文本文件到知识库
    
    与其他接口的关联关系:
        - 前置依赖接口: 无
        - 后续调用接口: /api/knowledge (查看知识库状态)
    
    错误码定义:
        - 200: 成功
        - 400: 请求参数错误
        - 500: 服务器内部错误
    """
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        chunks_count = processor.process_document(file_path)
        
        return FileUploadResponse(
            filename=file.filename,
            chunks_count=chunks_count,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
