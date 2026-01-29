from fastapi import APIRouter, HTTPException
from models.schemas import NovelWritingRequest, NovelWritingResponse, NovelChaptersResponse, NovelExportResponse
from agent.workflow import novel_workflow
from core.redis import redis_manager

router = APIRouter(prefix="/novel", tags=["novel"])


@router.post("/write", response_model=NovelWritingResponse)
async def novel_writing(request: NovelWritingRequest):
    """
    小说创作接口
    
    该接口用于接收创意框架文档和文风选择，生成具有高吸引力的爆款短篇小说，重点强化文字的情感感染力和叙事张力。
    
    Args:
        request: 小说创作请求参数
            - creative_framework: str, 必填, 创意框架文档
            - style: str, 必填, 文风选择
            - chapter_count: int, 必填, 章节数量
            - session_id: str, 必填, 会话ID
            - model: str, 必填, 选择的模型名称
    
    Returns:
        NovelWritingResponse: 小说创作响应
            - response: str, 响应消息
            - session_id: str, 会话ID
            - novel_content: str, 生成的小说内容
            - chapters: Optional[List[Dict]], 章节信息（暂未实现）
            - quality_evaluation: Optional[Dict], 质量评估（暂未实现）
            - word_count: int, 小说字数
            - style_used: str, 使用的文风
    
    典型调用场景:
        - 场景1: 基于创意框架生成短篇小说
        - 场景2: 按照指定文风生成小说
    
    与其他接口的关联关系:
        - 前置依赖接口: /api/creative/plan (生成创意框架)
        - 后续调用接口: /api/novel/chapters/{session_id} (获取小说章节), /api/novel/export/{session_id} (导出小说)
    
    错误码定义:
        - 200: 成功
        - 400: 请求参数错误
        - 500: 服务器内部错误
    """
    try:
        print(f"Received novel writing request: {request}")
        
        # 构建小说创作工作流的输入状态
        state = {
            "creative_framework": request.creative_framework,
            "style": request.style,
            "chapter_count": request.chapter_count,
            "session_id": request.session_id,
            "model": request.model
        }
        
        # 执行小说创作工作流
        print("Executing novel writing workflow...")
        result = await novel_workflow.ainvoke(state)
        
        print("Workflow execution completed.")
        print(f"Result keys: {list(result.keys())}")
        
        # 获取小说内容，优先使用response字段，然后使用full_novel字段
        novel_content = result.get("response", result.get("full_novel", ""))
        print(f"Novel content length: {len(novel_content)}")
        
        # 构建响应
        response = NovelWritingResponse(
            response="《爆款短篇小说》已生成",
            session_id=request.session_id,
            novel_content=novel_content,
            chapters=None,  # 暂时设置为None，后续可以根据需要解析
            quality_evaluation=None,  # 暂时设置为None，后续可以根据需要解析
            word_count=len(novel_content),
            style_used=request.style
        )
        
        print(f"Returning novel writing response")
        return response
        
    except Exception as e:
        print(f"Error in novel writing: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chapters/{session_id}", response_model=NovelChaptersResponse)
async def get_novel_chapters(session_id: str):
    """
    获取小说章节接口
    
    该接口根据会话ID，返回小说的章节列表，支持按章节查看和修改。
    
    Args:
        session_id: str, 必填, 会话ID
    
    Returns:
        NovelChaptersResponse: 小说章节响应
            - session_id: str, 会话ID
            - chapters: List[NovelChapter], 小说章节列表
            - message: str, 响应消息
    
    典型调用场景:
        - 场景1: 查看小说章节列表
        - 场景2: 按章节查看小说内容
    
    与其他接口的关联关系:
        - 前置依赖接口: /api/novel/write (生成小说)
        - 后续调用接口: 无
    
    错误码定义:
        - 200: 成功
        - 500: 服务器内部错误
    """
    try:
        print(f"Received get chapters request for session: {session_id}")
        
        # 这里简化处理，实际应该从Redis或数据库中获取章节信息
        # 后续可以扩展为从持久化存储中获取
        
        return NovelChaptersResponse(
            session_id=session_id,
            chapters=[],
            message="章节获取功能待实现"
        )
        
    except Exception as e:
        print(f"Error in get chapters: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/{session_id}", response_model=NovelExportResponse)
async def export_novel(session_id: str, format: str = "txt"):
    """
    导出小说接口
    
    该接口根据会话ID，导出小说内容为指定格式，支持txt、pdf等格式。
    
    Args:
        session_id: str, 必填, 会话ID
        format: str, 可选, 导出格式，默认值为"txt"
    
    Returns:
        NovelExportResponse: 小说导出响应
            - session_id: str, 会话ID
            - format: str, 导出格式
            - message: str, 响应消息
    
    典型调用场景:
        - 场景1: 导出小说为txt格式
        - 场景2: 导出小说为pdf格式
    
    与其他接口的关联关系:
        - 前置依赖接口: /api/novel/write (生成小说)
        - 后续调用接口: 无
    
    错误码定义:
        - 200: 成功
        - 500: 服务器内部错误
    """
    try:
        print(f"Received export novel request for session: {session_id}, format: {format}")
        
        # 这里简化处理，实际应该从Redis或数据库中获取小说内容并导出
        # 后续可以扩展为支持多种格式的导出
        
        return NovelExportResponse(
            session_id=session_id,
            format=format,
            message="小说导出功能待实现"
        )
        
    except Exception as e:
        print(f"Error in export novel: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
