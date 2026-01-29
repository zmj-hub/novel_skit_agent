from fastapi import APIRouter, HTTPException
from models.schemas import CreativePlanningRequest, CreativePlanningResponse
from agent.workflow import creative_workflow
from core.redis import redis_manager

router = APIRouter(prefix="/creative", tags=["creative"])


@router.post("/plan", response_model=CreativePlanningResponse)
async def creative_planning(request: CreativePlanningRequest):
    """
    创意策划接口
    
    该接口用于接收市场热点元素和故事类型，生成标准化的《故事创意框架》文档，包含人物小传、剧情大纲和核心反转节点。
    
    Args:
        request: 创意策划请求参数
            - hotspots: List[str], 必填, 市场热点元素列表
            - story_type: str, 必填, 故事类型
            - session_id: str, 必填, 会话ID
            - model: str, 必填, 选择的模型名称
    
    Returns:
        CreativePlanningResponse: 创意策划响应
            - response: str, 响应消息
            - session_id: str, 会话ID
            - creative_document: str, 生成的创意文档
            - story_framework: Optional[Dict], 故事框架（暂未实现）
            - sources: List[str], 引用的来源
    
    典型调用场景:
        - 场景1: 基于当前热点生成故事创意
        - 场景2: 为特定类型的故事生成创意框架
    
    与其他接口的关联关系:
        - 前置依赖接口: 无
        - 后续调用接口: /api/novel/write (基于创意框架撰写小说)
    
    错误码定义:
        - 200: 成功
        - 400: 请求参数错误
        - 500: 服务器内部错误
    """
    try:
        print(f"Received creative planning request: {request}")
        
        # 构建创意策划工作流的输入状态
        state = {
            "hotspots": request.hotspots,
            "story_type": request.story_type,
            "session_id": request.session_id,
            "model": request.model
        }
        
        # 执行创意策划工作流
        print("Executing creative planning workflow...")
        result = await creative_workflow.ainvoke(state)
        
        print("Workflow execution completed.")
        print(f"Result keys: {list(result.keys())}")
        
        # 构建响应
        response = CreativePlanningResponse(
            response="《故事创意框架》文档已生成",
            session_id=request.session_id,
            creative_document=result.get("response", ""),
            story_framework=None,  # 暂时设置为None，后续可以根据需要解析
            sources=[]
        )
        
        print(f"Returning creative planning response")
        return response
        
    except Exception as e:
        print(f"Error in creative planning: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
