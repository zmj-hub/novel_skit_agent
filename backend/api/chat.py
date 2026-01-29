from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from core.redis import redis_manager
from utils.async_llm import llm_manager

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    对话功能接口
    
    该接口用于处理用户的对话请求，支持多轮对话、知识库使用和模型选择。
    
    Args:
        request: 对话请求参数
            - message: str, 必填, 用户输入的消息内容
            - session_id: str, 必填, 会话ID，用于保持对话上下文
            - use_knowledge: bool, 必填, 是否使用知识库
            - model: str, 必填, 选择的模型名称
    
    Returns:
        ChatResponse: 对话响应
            - response: str, AI生成的回复内容
            - session_id: str, 会话ID
            - sources: List[str], 引用的知识库来源
    
    典型调用场景:
        - 场景1: 普通对话 - 用户发送消息，获取AI回复
        - 场景2: 知识库增强对话 - 用户发送消息并启用知识库，获取基于知识库的回复
    
    与其他接口的关联关系:
        - 前置依赖接口: 无
        - 后续调用接口: 无
    
    错误码定义:
        - 200: 成功
        - 400: 请求参数错误
        - 500: 服务器内部错误
    """
    try:
        print(f"Received chat request: {request}")
        
        # 从 Redis 获取对话历史
        history = await redis_manager.get_chat_history(request.session_id)
        print(f"Retrieved chat history: {history}")
        
        # 获取指定的模型
        llm = llm_manager.get_llm(request.model)
        
        # 生成响应
        response_content = await llm.generate_with_history(request.message, history)
        print(f"Generated response: {response_content}")
        
        # 更新对话历史
        updated_history = history + [
            {"role": "user", "content": request.message},
            {"role": "assistant", "content": response_content}
        ]
        
        # 保存对话历史到 Redis
        await redis_manager.store_chat_history(request.session_id, updated_history)
        print(f"Saved updated chat history")
        
        # 构建响应
        response = ChatResponse(
            response=response_content,
            session_id=request.session_id,
            sources=[]
        )
        
        print(f"Returning response: {response}")
        return response
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
