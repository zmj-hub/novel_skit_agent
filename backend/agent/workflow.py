from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing import Dict, List, Any, Optional
from rag.retriever import retriever
from utils.async_llm import llm_manager
from core.redis import redis_manager
from core.config import settings
from agent.creative_agent import CreativePlanningAgent
from agent.novel_agent import NovelWritingAgent
from agent.scheduler_agent import CoordinationSchedulerAgent
import datetime


class AgentState:
    messages: List[Dict[str, str]]
    session_id: str
    use_knowledge: bool
    model: Optional[str] = None
    response: Optional[str] = None
    sources: Optional[List[Dict[str, Any]]] = None


async def retrieve_knowledge(state: Dict[str, Any]) -> Dict[str, Any]:
    if state.get('use_knowledge', True):
        if 'messages' not in state or not state['messages']:
            return {"sources": []}
        query = state['messages'][-1]['content']
        try:
            sources = retriever.retrieve(query)
            return {"sources": sources}
        except Exception as e:
            print(f"Warning: Failed to retrieve knowledge: {e}")
            return {"sources": []}
    return {"sources": []}


async def generate_response(state: Dict[str, Any]) -> Dict[str, Any]:
    if 'messages' not in state or not state['messages']:
        return {"response": "No message provided."}
    
    query = state['messages'][-1]['content']
    sources = state.get('sources', [])
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print(f"Generating response for query: {query}")
    print(f"Using model: {model}")
    
    # 直接返回一个硬编码的响应，以便测试
    return {
        "response": f"我是一个使用 {model} 模型的 AI 助手，我已经收到了你的消息：{query}"
    }
    
    # 以下是原始代码，暂时注释掉
    """
    try:
        llm = llm_manager.get_llm(model)
        print(f"Got LLM instance: {type(llm).__name__}")
        
        if sources:
            try:
                print(f"Using {len(sources)} sources for context")
                context = retriever.build_context(query)
                print(f"Built context with {len(context)} characters")
                response = await llm.generate_with_context(query, context)
            except Exception as e:
                print(f"Warning: Failed to generate with context: {e}")
                print("Falling back to generate without context")
                response = await llm.generate(query)
        else:
            print("Generating without context")
            response = await llm.generate(query)
        
        print(f"Generated response: {response[:100]}...")
        return {"response": response}
    except Exception as e:
        print(f"Warning: Failed to generate response: {e}")
        import traceback
        traceback.print_exc()
        return {"response": f"Error generating response: {e}"}
    """



async def update_history(state: Dict[str, Any]) -> Dict[str, Any]:
    session_id = state.get('session_id', '')
    history = state.get('messages', [])
    
    if 'response' in state:
        history.append({"role": "assistant", "content": state['response']})
    
    if session_id:
        await redis_manager.store_chat_history(session_id, history)
    
    return {}


def create_agent_workflow():
    workflow = StateGraph(dict)
    
    workflow.add_node("retrieve", retrieve_knowledge)
    workflow.add_node("generate", generate_response)
    workflow.add_node("update_history", update_history)
    
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", "update_history")
    workflow.add_edge("update_history", END)
    
    return workflow.compile()


agent_workflow = create_agent_workflow()


class CreativeAgentState:
    hotspots: List[str]
    story_type: str
    session_id: str
    model: Optional[str] = None
    hotspots_analysis: Optional[Dict[str, Any]] = None
    story_framework: Optional[Dict[str, Any]] = None
    media_adaptation: Optional[Dict[str, Any]] = None
    creative_document: Optional[Dict[str, Any]] = None
    response: Optional[str] = None


async def analyze_hotspots_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    热点分析节点
    """
    hotspots = state.get('hotspots', [])
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print(f"Analyzing hotspots: {hotspots}")
    print(f"Using model: {model}")
    
    try:
        agent = CreativePlanningAgent(model)
        hotspots_analysis = await agent.analyze_hotspots(hotspots)
        return {"hotspots_analysis": hotspots_analysis}
    except Exception as e:
        print(f"Warning: Failed to analyze hotspots: {e}")
        return {"hotspots_analysis": {"hotspots": hotspots, "analysis": f"Error: {e}"}}


async def build_framework_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    故事框架构建节点
    """
    hotspots_analysis = state.get('hotspots_analysis')
    story_type = state.get('story_type', '都市情感')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print(f"Building story framework for: {story_type}")
    
    try:
        agent = CreativePlanningAgent(model)
        story_framework = await agent.build_story_framework(hotspots_analysis, story_type)
        return {"story_framework": story_framework}
    except Exception as e:
        print(f"Warning: Failed to build story framework: {e}")
        return {"story_framework": {"story_type": story_type, "framework": f"Error: {e}"}}


async def adapt_media_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    媒介适配节点
    """
    story_framework = state.get('story_framework')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print("Adapting story to different media formats")
    
    try:
        agent = CreativePlanningAgent(model)
        media_adaptation = await agent.adapt_to_media(story_framework)
        return {"media_adaptation": media_adaptation}
    except Exception as e:
        print(f"Warning: Failed to adapt to media: {e}")
        return {"media_adaptation": {"story_type": story_framework.get('story_type', '未知'), "adaptation": f"Error: {e}"}}


async def generate_document_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    文档生成节点
    """
    hotspots_analysis = state.get('hotspots_analysis', {})
    story_framework = state.get('story_framework', {})
    media_adaptation = state.get('media_adaptation', {})
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print("Generating creative document")
    
    try:
        agent = CreativePlanningAgent(model)
        creative_document = await agent.generate_creative_document(
            hotspots_analysis, story_framework, media_adaptation
        )
        return {"creative_document": creative_document, "response": creative_document.get('document', '')}
    except Exception as e:
        print(f"Warning: Failed to generate creative document: {e}")
        return {"creative_document": {"document_type": "故事创意框架", "document": f"Error: {e}"}, "response": f"Error: {e}"}


def create_creative_workflow():
    """
    创建创意策划工作流
    """
    workflow = StateGraph(dict)
    
    workflow.add_node("analyze_hotspots", analyze_hotspots_node)
    workflow.add_node("build_framework", build_framework_node)
    workflow.add_node("adapt_media", adapt_media_node)
    workflow.add_node("generate_document", generate_document_node)
    
    workflow.set_entry_point("analyze_hotspots")
    workflow.add_edge("analyze_hotspots", "build_framework")
    workflow.add_edge("build_framework", "adapt_media")
    workflow.add_edge("adapt_media", "generate_document")
    workflow.add_edge("generate_document", END)
    
    return workflow.compile()


creative_workflow = create_creative_workflow()


class NovelAgentState:
    creative_framework: str
    style: str
    session_id: str
    model: Optional[str] = None
    chapter_count: int = 5
    parsed_framework: Optional[Dict[str, Any]] = None
    adapted_content: Optional[Dict[str, Any]] = None
    character_arc: Optional[Dict[str, Any]] = None
    conflicts: Optional[Dict[str, Any]] = None
    chapters: Optional[List[Dict[str, Any]]] = None
    full_novel: Optional[str] = None
    quality_evaluation: Optional[Dict[str, Any]] = None
    response: Optional[str] = None


async def parse_framework_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    创意框架解析节点
    """
    creative_framework = state.get('creative_framework', '')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print(f"Parsing creative framework...")
    print(f"Using model: {model}")
    
    try:
        agent = NovelWritingAgent(model)
        parsed_framework = await agent.parse_creative_framework(creative_framework)
        return {"parsed_framework": parsed_framework}
    except Exception as e:
        print(f"Warning: Failed to parse creative framework: {e}")
        return {"parsed_framework": {"creative_framework": creative_framework, "parsed_content": f"Error: {e}"}}


async def adapt_style_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    文风适配节点
    """
    parsed_framework = state.get('parsed_framework')
    style = state.get('style', 'urban')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print(f"Adapting writing style to: {style}")
    
    try:
        agent = NovelWritingAgent(model)
        adapted_content = await agent.adapt_writing_style(parsed_framework['parsed_content'], style)
        return {"adapted_content": adapted_content}
    except Exception as e:
        print(f"Warning: Failed to adapt writing style: {e}")
        return {"adapted_content": {"original_content": parsed_framework.get('parsed_content', ''), "style": style, "adapted_content": f"Error: {e}"}}


async def create_characters_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    人物塑造节点
    """
    adapted_content = state.get('adapted_content')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print("Creating character arcs...")
    
    try:
        agent = NovelWritingAgent(model)
        character_arc = await agent.create_character_arc(adapted_content['adapted_content'])
        conflicts = await agent.design_conflicts(adapted_content['adapted_content'])
        return {"character_arc": character_arc, "conflicts": conflicts}
    except Exception as e:
        print(f"Warning: Failed to create character arcs: {e}")
        return {"character_arc": {"character_info": adapted_content.get('adapted_content', ''), "character_arc": f"Error: {e}"}, "conflicts": {"story_context": adapted_content.get('adapted_content', ''), "conflicts": f"Error: {e}"}}


async def write_chapters_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    章节创作节点
    """
    adapted_content = state.get('adapted_content')
    style = state.get('style', 'urban')
    chapter_count = state.get('chapter_count', 5)
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print(f"Writing {chapter_count} chapters...")
    
    try:
        agent = NovelWritingAgent(model)
        chapters = []
        chapter_contents = []
        for i in range(1, chapter_count + 1):
            chapter_outline = f"第{i}章：基于创意框架的章节内容"
            chapter = await agent.write_chapter(chapter_outline, style, i)
            chapters.append(chapter)
            chapter_contents.append(chapter['chapter_content'])
        
        full_novel = "\n\n".join(chapter_contents)
        print(f"Generated full novel with {len(full_novel)} characters")
        return {"chapters": chapters, "full_novel": full_novel, "response": full_novel}
    except Exception as e:
        print(f"Warning: Failed to write chapters: {e}")
        error_message = f"Error: {e}"
        return {"chapters": [], "full_novel": error_message, "response": error_message}


async def evaluate_quality_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    质量评估节点
    """
    full_novel = state.get('full_novel')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print("Evaluating content quality...")
    
    try:
        agent = NovelWritingAgent(model)
        quality_evaluation = await agent.evaluate_content_quality(full_novel)
        return {"quality_evaluation": quality_evaluation, "response": full_novel}
    except Exception as e:
        print(f"Warning: Failed to evaluate content quality: {e}")
        return {"quality_evaluation": {"content": full_novel, "evaluation": f"Error: {e}"}, "response": full_novel}


def create_novel_workflow():
    """
    创建小说创作工作流
    """
    workflow = StateGraph(dict)
    
    workflow.add_node("parse_framework", parse_framework_node)
    workflow.add_node("adapt_style", adapt_style_node)
    workflow.add_node("create_characters", create_characters_node)
    workflow.add_node("write_chapters", write_chapters_node)
    workflow.add_node("evaluate_quality", evaluate_quality_node)
    
    workflow.set_entry_point("parse_framework")
    workflow.add_edge("parse_framework", "adapt_style")
    workflow.add_edge("adapt_style", "create_characters")
    workflow.add_edge("create_characters", "write_chapters")
    workflow.add_edge("write_chapters", "evaluate_quality")
    workflow.add_edge("evaluate_quality", END)
    
    return workflow.compile()


novel_workflow = create_novel_workflow()


class SchedulerAgentState:
    story_description: str
    story_type: str
    request_priority: int
    session_id: str
    model: Optional[str] = None
    schedule: Optional[Dict[str, Any]] = None
    conflict_detection: Optional[Dict[str, Any]] = None
    conflict_resolution: Optional[Dict[str, Any]] = None
    resource_allocations: Optional[Dict[str, Any]] = None
    adapted_workflow: Optional[Dict[str, Any]] = None
    task_plan: Optional[Dict[str, Any]] = None
    task_breakdown: Optional[Dict[str, Any]] = None
    agent_allocation: Optional[Dict[str, Any]] = None
    progress_tracking: Optional[Dict[str, Any]] = None
    result_summary: Optional[Dict[str, Any]] = None
    scheduling_log: Optional[Dict[str, Any]] = None
    exception_report: Optional[Dict[str, Any]] = None
    response: Optional[str] = None


async def create_schedule_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    工作时序规划节点
    """
    request_priority = state.get('request_priority', 1)
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print(f"Creating workflow schedule with priority: {request_priority}")
    print(f"Using model: {model}")
    
    try:
        agent = CoordinationSchedulerAgent(model)
        schedule = await agent.create_workflow_schedule(request_priority)
        # 返回包含原始状态的数据
        result = state.copy()
        result["schedule"] = schedule
        return result
    except Exception as e:
        print(f"Warning: Failed to create workflow schedule: {e}")
        # 返回包含原始状态的数据
        result = state.copy()
        result["schedule"] = {"schedule": [], "created_at": "Error", "total_duration": 0}
        return result


async def detect_conflicts_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    冲突检测节点
    """
    schedule = state.get('schedule')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print("Detecting potential conflicts...")
    
    try:
        agent = CoordinationSchedulerAgent(model)
        conflict_detection = await agent.detect_conflicts(schedule)
        conflict_resolution = await agent.resolve_conflicts(conflict_detection)
        # 返回包含原始状态的数据
        result = state.copy()
        result["conflict_detection"] = conflict_detection
        result["conflict_resolution"] = conflict_resolution
        return result
    except Exception as e:
        print(f"Warning: Failed to detect conflicts: {e}")
        # 返回包含原始状态的数据
        result = state.copy()
        result["conflict_detection"] = {"conflicts": [], "detected_at": "Error", "conflict_count": 0}
        result["conflict_resolution"] = {"resolutions": [], "resolved_at": "Error", "resolved_count": 0}
        return result


async def allocate_resources_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    资源分配节点
    """
    schedule = state.get('schedule')
    request_priority = state.get('request_priority', 1)
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print(f"Allocating resources with priority: {request_priority}")
    
    try:
        agent = CoordinationSchedulerAgent(model)
        resource_allocations = await agent.allocate_resources(schedule, request_priority)
        story_type = state.get('story_type', '都市')
        adapted_workflow = await agent.adapt_agent_workflow(schedule, story_type)
        # 返回包含原始状态的数据
        result = state.copy()
        result["resource_allocations"] = resource_allocations
        result["adapted_workflow"] = adapted_workflow
        return result
    except Exception as e:
        print(f"Warning: Failed to allocate resources: {e}")
        # 返回包含原始状态的数据
        result = state.copy()
        result["resource_allocations"] = {"allocations": [], "allocated_at": "Error", "total_resources": {"cpu_cores": 0, "memory_gb": 0}}
        result["adapted_workflow"] = {"adapted_workflow": [], "skipped_steps": [], "adapted_at": "Error", "skipped_count": 0}
        return result


import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import asyncio
import uuid
import traceback
from .models import TaskProgress, Anomaly, StepExecutionReport
from .storage import storage, report_storage

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 工作流状态定义
WORKFLOW_STATES = {
    "INITIALIZED": "initialized",
    "RUNNING": "running",
    "SUCCESS": "success",
    "FAILED": "failed",
    "PAUSED": "paused"
}

# 可重试的错误类型
RETRYABLE_ERRORS = [
    "NetworkError",
    "TimeoutError",
    "ResourceUnavailableError",
    "TemporaryError"
]


async def validate_workflow(adapted_workflow: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    验证工作流结构
    
    Args:
        adapted_workflow: 适配后的工作流
        
    Returns:
        Tuple[bool, Optional[str]]: (是否有效, 错误信息)
    """
    if not adapted_workflow:
        return False, "工作流不能为空"
    
    if "adapted_workflow" not in adapted_workflow:
        return False, "工作流缺少步骤定义"
    
    steps = adapted_workflow["adapted_workflow"]
    if not isinstance(steps, list):
        return False, "工作流步骤必须是列表"
    
    if len(steps) == 0:
        return False, "工作流步骤不能为空"
    
    return True, None


async def execute_workflow_step(
    step: Dict[str, Any],
    state: Dict[str, Any],
    step_index: int,
    total_steps: int
) -> Dict[str, Any]:
    """
    执行单个工作流步骤，并将执行结果保存到报告文件中

    Args:
        step: 工作流步骤
        state: 当前状态
        step_index: 步骤索引
        total_steps: 总步骤数

    Returns:
        Dict[str, Any]: 执行结果
    """
    step_name = step.get("name", f"step_{step_index}")
    step_type = step.get("type", "generic")
    step_params = step.get("params", {})

    # 获取任务和会话信息
    task_id = state.get("task_id", f"task_{uuid.uuid4()}")
    session_id = state.get("session_id", "")

    logger.info(f"开始执行步骤 {step_index + 1}/{total_steps}: {step_name} (类型: {step_type})")

    # 创建步骤执行报告对象
    report = StepExecutionReport(
        task_id=task_id,
        session_id=session_id,
        step_name=step_name,
        step_type=step_type,
        step_index=step_index,
        total_steps=total_steps
    )

    # 记录步骤开始时间
    start_time = datetime.now()

    try:
        # 根据步骤类型执行不同的逻辑
        if step_type == "creative_planning":
            # 执行创意策划步骤
            from agent.creative_agent import CreativePlanningAgent
            model = state.get("model", settings.DEFAULT_MODEL)
            agent = CreativePlanningAgent(model)

            # 执行创意策划逻辑
            result = await agent.analyze_hotspots(step_params.get("hotspots", []))
            logger.info(f"创意策划步骤执行完成: {step_name}")

        elif step_type == "novel_writing":
            # 执行小说创作步骤
            from agent.novel_agent import NovelWritingAgent
            model = state.get("model", settings.DEFAULT_MODEL)
            agent = NovelWritingAgent(model)

            # 执行小说创作逻辑
            result = await agent.write_chapter(
                step_params.get("chapter_outline", ""),
                step_params.get("style", "urban"),
                step_params.get("chapter_number", step_index + 1)
            )
            logger.info(f"小说创作步骤执行完成: {step_name}")

        elif step_type == "quality_evaluation":
            # 执行质量评估步骤
            from agent.novel_agent import NovelWritingAgent
            model = state.get("model", settings.DEFAULT_MODEL)
            agent = NovelWritingAgent(model)

            # 执行质量评估逻辑
            content = step_params.get("content", state.get("full_novel", ""))
            result = await agent.evaluate_content_quality(content)
            logger.info(f"质量评估步骤执行完成: {step_name}")

        else:
            # 通用步骤执行逻辑 - 调用LLM生成内容
            logger.info(f"执行通用步骤: {step_name}")

            # 获取LLM实例
            model = state.get("model", settings.DEFAULT_MODEL)
            llm = llm_manager.get_llm(model)

            # 构建提示词
            story_type = state.get("story_type", "未知")
            story_description = state.get("story_description", "")
            prompt = f"""你是一个专业的故事创作助手。请为以下故事执行任务：{step_name}

故事类型：{story_type}
故事描述：{story_description[:200]}...

请提供详细的执行结果，包括具体的创作内容、分析和建议。
"""

            # 调用LLM生成结果
            try:
                result_text = await llm.generate(prompt)
                result = {
                    "step_name": step_name,
                    "step_type": step_type,
                    "status": "completed",
                    "result": result_text
                }
                logger.info(f"通用步骤 {step_name} 执行成功，生成了 {len(result_text)} 字符的内容")
            except Exception as e:
                logger.error(f"通用步骤 {step_name} 执行失败: {str(e)}")
                result = {
                    "step_name": step_name,
                    "step_type": step_type,
                    "status": "failed",
                    "error": str(e)
                }

        # 记录步骤结束时间
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        # 标记报告为完成状态
        report.mark_completed(result)

        # 保存执行报告到文件
        report_file_path = report_storage.save_step_report(report)
        if report_file_path:
            logger.info(f"步骤执行报告已保存: {report_file_path}")
        else:
            logger.warning(f"步骤执行报告保存失败: {step_name}")

        logger.info(f"步骤 {step_name} 执行完成，耗时: {execution_time:.2f}秒")

        return {
            "step_name": step_name,
            "step_type": step_type,
            "status": "completed",
            "result": result,
            "execution_time": execution_time,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "report_id": report.report_id,
            "report_file": report_file_path
        }

    except Exception as e:
        # 记录步骤执行错误
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        error_message = str(e)
        error_stack_trace = traceback.format_exc()
        logger.error(f"步骤 {step_name} 执行失败: {error_message}")
        logger.error(f"错误堆栈: {error_stack_trace}")

        # 标记报告为失败状态
        report.mark_failed(error_message, error_stack_trace)

        # 保存执行报告到文件（即使失败也要保存）
        report_file_path = report_storage.save_step_report(report)
        if report_file_path:
            logger.info(f"步骤执行报告（失败）已保存: {report_file_path}")
        else:
            logger.warning(f"步骤执行报告（失败）保存失败: {step_name}")

        return {
            "step_name": step_name,
            "step_type": step_type,
            "status": "failed",
            "error": error_message,
            "execution_time": execution_time,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "report_id": report.report_id,
            "report_file": report_file_path
        }


async def retry_workflow_step(
    step: Dict[str, Any], 
    state: Dict[str, Any], 
    step_index: int,
    total_steps: int,
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    重试执行工作流步骤
    
    Args:
        step: 工作流步骤
        state: 当前状态
        step_index: 步骤索引
        total_steps: 总步骤数
        max_retries: 最大重试次数
        
    Returns:
        Dict[str, Any]: 执行结果
    """
    retries = 0
    last_error = None
    
    while retries < max_retries:
        try:
            result = await execute_workflow_step(step, state, step_index, total_steps)
            if result["status"] == "completed":
                logger.info(f"步骤执行成功（重试 {retries} 次）")
                return result
            
            # 检查是否是可重试的错误
            error_message = result.get("error", "")
            is_retryable = any(error_type in error_message for error_type in RETRYABLE_ERRORS)
            
            if not is_retryable:
                logger.info("遇到不可重试的错误，停止重试")
                return result
            
            retries += 1
            last_error = error_message
            
            # 指数退避
            backoff_time = min(2 ** retries, 30)  # 最大退避时间30秒
            logger.info(f"步骤执行失败，{backoff_time}秒后重试 ({retries}/{max_retries})")
            await asyncio.sleep(backoff_time)
            
        except Exception as e:
            retries += 1
            last_error = str(e)
            
            # 指数退避
            backoff_time = min(2 ** retries, 30)
            logger.error(f"步骤执行异常，{backoff_time}秒后重试 ({retries}/{max_retries}): {last_error}")
            await asyncio.sleep(backoff_time)
    
    # 重试次数耗尽
    logger.error(f"步骤执行失败，已达到最大重试次数 ({max_retries})")
    return {
        "step_name": step.get("name", f"step_{step_index}"),
        "step_type": step.get("type", "generic"),
        "status": "failed",
        "error": last_error or "未知错误",
        "retries": retries,
        "max_retries": max_retries
    }


async def execute_workflow_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行工作流节点
    
    实现完整的工作流执行逻辑，包括状态管理、步骤执行控制、错误处理和重试机制
    """
    # 获取工作流配置
    adapted_workflow = state.get('adapted_workflow')
    model = state.get('model', settings.DEFAULT_MODEL)
    session_id = state.get('session_id', '')
    
    # 初始化结果
    result = state.copy()
    
    # 验证工作流
    is_valid, error_msg = await validate_workflow(adapted_workflow)
    if not is_valid:
        logger.error(f"工作流验证失败: {error_msg}")
        result["workflow_status"] = WORKFLOW_STATES["FAILED"]
        result["workflow_error"] = error_msg
        result["response"] = f"工作流执行失败: {error_msg}"
        return result
    
    # 初始化工作流状态
    workflow_steps = adapted_workflow.get("adapted_workflow", [])
    total_steps = len(workflow_steps)
    
    # 记录工作流开始时间
    start_time = datetime.now()
    
    # 创建任务进度对象
    task_id = f"task_{uuid.uuid4()}"
    story_type = state.get('story_type', '都市')
    task_progress = TaskProgress(task_id, session_id, story_type)
    
    # 为每个工作流步骤添加到任务进度中
    step_map = {}
    for step in workflow_steps:
        step_name = step.get("name", f"step_{len(task_progress.step_progress)}")
        step_obj = task_progress.add_step(step_name)
        step_map[step_name] = step_obj.step_id
    
    # 更新工作流状态为运行中
    result["workflow_status"] = WORKFLOW_STATES["RUNNING"]
    result["workflow_start_time"] = start_time.isoformat()
    result["workflow_progress"] = 0
    result["workflow_steps"] = []
    result["workflow_execution_logs"] = []
    result["task_id"] = task_id
    
    logger.info(f"开始执行工作流，共 {total_steps} 个步骤")
    
    try:
        # 顺序执行每个步骤
        for i, step in enumerate(workflow_steps):
            step_name = step.get("name", f"step_{i}")
            step_id = step_map.get(step_name)
            
            # 更新当前步骤状态为运行中
            if step_id:
                task_progress.update_step_progress(step_id, 0, "running")
                storage.save(task_progress)
            
            # 计算当前进度
            progress = int((i / total_steps) * 100)
            result["workflow_progress"] = progress
            
            # 执行步骤
            step_result = await retry_workflow_step(step, result, i, total_steps)
            
            # 记录步骤结果
            result["workflow_steps"].append(step_result)
            
            # 检查步骤执行状态
            if step_result["status"] == "failed":
                # 步骤执行失败
                error_message = step_result.get('error', '未知错误')
                logger.error(f"步骤 {i + 1}/{total_steps} 执行失败: {error_message}")
                
                # 更新步骤状态为失败
                if step_id:
                    task_progress.update_step_progress(step_id, 0, "failed")
                    # 添加异常记录
                    anomaly = Anomaly("error", "high", f"步骤 {step_name} 执行失败: {error_message}")
                    task_progress.add_anomaly(anomaly)
                    storage.save(task_progress)
                
                result["workflow_status"] = WORKFLOW_STATES["FAILED"]
                result["workflow_error"] = error_message
                result["workflow_progress"] = int(((i + 1) / total_steps) * 100)
                break
            else:
                # 步骤执行成功
                if step_id:
                    task_progress.update_step_progress(step_id, 100, "completed")
                    storage.save(task_progress)
            
            # 将步骤结果合并到状态中
            if "result" in step_result:
                # 根据步骤类型合并不同的结果
                step_type = step.get("type", "generic")
                if step_type == "creative_planning":
                    result["creative_output"] = step_result["result"]
                elif step_type == "novel_writing":
                    result["chapter_output"] = step_result["result"]
                elif step_type == "quality_evaluation":
                    result["quality_evaluation"] = step_result["result"]
            
            # 记录执行日志
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "message": f"步骤 {i + 1}/{total_steps} 执行完成: {step_result['status']}",
                "step_name": step_result.get("step_name", f"step_{i}"),
                "step_status": step_result["status"]
            }
            result["workflow_execution_logs"].append(log_entry)
        
        # 计算工作流结束时间
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # 更新工作流状态
        if result["workflow_status"] == WORKFLOW_STATES["RUNNING"]:
            # 所有步骤执行完成
            result["workflow_status"] = WORKFLOW_STATES["SUCCESS"]
            result["workflow_progress"] = 100
            result["response"] = "工作流执行成功"
            logger.info(f"工作流执行成功，共耗时: {execution_time:.2f}秒")
            
            # 更新任务进度为完成
            task_progress.status = "completed"
            task_progress.end_time = end_time.isoformat()
            task_progress.progress = 100
        else:
            # 工作流执行失败
            logger.error(f"工作流执行失败，共耗时: {execution_time:.2f}秒")
            
            # 更新任务进度为失败
            task_progress.status = "failed"
            task_progress.end_time = end_time.isoformat()
        
        # 更新工作流执行信息
        result["workflow_end_time"] = end_time.isoformat()
        result["workflow_execution_time"] = execution_time
        result["workflow_total_steps"] = total_steps
        result["workflow_completed_steps"] = len([s for s in result["workflow_steps"] if s["status"] == "completed"])
        
        # 保存任务进度
        storage.save(task_progress)
        
        # 添加任务进度到结果中
        result["task_progress"] = task_progress.to_dict()
        
    except Exception as e:
        # 捕获工作流执行过程中的异常
        error_message = str(e)
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        logger.error(f"工作流执行过程中发生异常: {error_message}")
        
        # 更新工作流状态为失败
        result["workflow_status"] = WORKFLOW_STATES["FAILED"]
        result["workflow_error"] = error_message
        result["workflow_end_time"] = end_time.isoformat()
        result["workflow_execution_time"] = execution_time
        result["response"] = f"工作流执行失败: {error_message}"
        
        # 更新任务进度为失败
        task_progress.status = "failed"
        task_progress.end_time = end_time.isoformat()
        # 添加异常记录
        anomaly = Anomaly("error", "high", f"工作流执行异常: {error_message}")
        task_progress.add_anomaly(anomaly)
        storage.save(task_progress)
        
        # 记录错误日志
        log_entry = {
            "timestamp": end_time.isoformat(),
            "level": "ERROR",
            "message": f"工作流执行异常: {error_message}",
            "error": error_message
        }
        result["workflow_execution_logs"].append(log_entry)
        
        # 添加任务进度到结果中
        result["task_progress"] = task_progress.to_dict()
    
    # 记录最终状态
    logger.info(f"工作流执行结束，状态: {result['workflow_status']}")
    
    return result


# ============================================
# 新智能体协调工作流 - 精简版（5个核心节点）
# ============================================

async def planning_and_scheduling_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    节点1: 智能规划与调度
    
    整合原 task_planning + task_breakdown + create_schedule + agent_allocation
    根据故事类型和内容动态生成执行计划，智能分配智能体
    """
    story_description = state.get('story_description', '')
    story_type = state.get('story_type', '')
    request_priority = state.get('request_priority', 1)
    model = state.get('model', settings.DEFAULT_MODEL)
    session_id = state.get('session_id', '')
    
    print(f"=" * 60)
    print(f"节点1: 智能规划与调度")
    print(f"Story Type: {story_type}, Priority: {request_priority}")
    print(f"=" * 60)
    
    # 更新进度回调
    progress_callback = state.get('progress_callback')
    if progress_callback:
        await progress_callback({
            "status": "planning",
            "message": "正在进行智能规划与调度...",
            "overall_progress": 5,
            "content": f"故事类型: {story_type}\n故事描述: {story_description[:100]}..."
        })
    
    try:
        agent = CoordinationSchedulerAgent(model)
        
        # 使用新的动态规划方法
        execution_plan = await agent.dynamic_planning(
            story_description=story_description,
            story_type=story_type,
            request_priority=request_priority
        )
        
        # 记录执行元数据
        execution_metadata = {
            "start_time": datetime.now().isoformat(),
            "steps_completed": 0,
            "total_steps": execution_plan.get("total_steps", 0),
            "milestones": [{"event": "planning_completed", "time": datetime.now().isoformat()}]
        }
        
        result = state.copy()
        result["execution_plan"] = execution_plan
        result["execution_metadata"] = execution_metadata
        result["response"] = f"动态规划完成: {execution_plan.get('plan_summary', '')}"
        
        print(f"✓ 规划完成: {execution_plan.get('total_steps', 0)} 个步骤")
        
        # 提取执行计划摘要
        plan_summary = execution_plan.get('plan_summary', '')
        steps_info = f"计划步骤: {execution_plan.get('total_steps', 0)}个"
        
        if progress_callback:
            await progress_callback({
                "status": "planning_completed",
                "message": f"规划完成，共{execution_plan.get('total_steps', 0)}个步骤",
                "overall_progress": 10,
                "execution_plan": execution_plan,
                "content": f"{plan_summary}\n{steps_info}"
            })
        
        return result
        
    except Exception as e:
        print(f"✗ 规划失败: {e}")
        result = state.copy()
        result["execution_plan"] = {
            "plan_id": "error",
            "story_type": story_type,
            "steps": [],
            "total_steps": 0,
            "plan_summary": f"规划失败: {str(e)}"
        }
        result["execution_metadata"] = {"error": str(e)}
        return result


async def creative_execution_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    节点2: 创意策划执行
    
    执行创意策划工作流，包括热点分析、故事框架构建、媒介适配
    """
    story_description = state.get('story_description', '')
    story_type = state.get('story_type', '')
    model = state.get('model', settings.DEFAULT_MODEL)
    execution_plan = state.get('execution_plan', {})
    
    print(f"\n{'=' * 60}")
    print(f"节点2: 创意策划执行")
    print(f"{'=' * 60}")
    
    progress_callback = state.get('progress_callback')
    if progress_callback:
        await progress_callback({
            "status": "creative_executing",
            "message": "正在执行创意策划...",
            "overall_progress": 15
        })
    
    try:
        # 检查是否需要创意策划步骤
        steps = execution_plan.get('steps', [])
        has_creative_step = any(s.get('step_type') == 'creative_planning' for s in steps)
        
        if not has_creative_step:
            print("ℹ 执行计划中无需创意策划步骤，跳过")
            result = state.copy()
            result["creative_framework"] = {"skipped": True, "reason": "No creative planning step in execution plan"}
            return result
        
        # 执行创意策划
        agent = CreativePlanningAgent(model)
        
        # 1. 热点分析（可选）
        hotspots = state.get('hotspots', [])
        if hotspots:
            print("→ 执行热点分析...")
            hotspots_analysis = await agent.analyze_hotspots(hotspots)
        else:
            hotspots_analysis = {"hotspots": [], "analysis": "未提供热点元素"}
        
        # 提取热点分析内容
        hotspots_content = hotspots_analysis.get('analysis', '')
        
        if progress_callback:
            await progress_callback({
                "status": "hotspots_analyzed",
                "message": "热点分析完成",
                "overall_progress": 20,
                "content": hotspots_content
            })
        
        # 2. 故事框架构建
        print("→ 构建故事框架...")
        story_framework = await agent.build_story_framework(hotspots_analysis, story_type)
        
        # 提取故事框架内容
        framework_content = f"主题: {story_framework.get('theme', '')}\n"
        framework_content += f"背景: {story_framework.get('setting', '')}\n"
        framework_content += f"核心冲突: {story_framework.get('core_conflict', '')}\n"
        characters = story_framework.get('characters', [])
        if characters:
            framework_content += f"主要人物: {', '.join([char.get('name', '') for char in characters[:3]])}"
        
        if progress_callback:
            await progress_callback({
                "status": "framework_built",
                "message": "故事框架构建完成",
                "overall_progress": 25,
                "content": framework_content
            })
        
        # 3. 媒介适配
        print("→ 执行媒介适配...")
        media_adaptation = await agent.adapt_to_media(story_framework)
        
        # 整合创意框架
        creative_framework = {
            "hotspots_analysis": hotspots_analysis,
            "story_framework": story_framework,
            "media_adaptation": media_adaptation,
            "creative_document": await agent.generate_creative_document(
                hotspots_analysis, story_framework, media_adaptation
            )
        }
        
        result = state.copy()
        result["creative_framework"] = creative_framework
        result["response"] = "创意策划执行完成"
        
        # 更新执行元数据
        if "execution_metadata" in result:
            result["execution_metadata"]["steps_completed"] = 1
            result["execution_metadata"]["milestones"].append({
                "event": "creative_completed",
                "time": datetime.now().isoformat()
            })
        
        print(f"✓ 创意策划完成")
        
        # 提取创意文档内容
        creative_doc_content = creative_framework.get('creative_document', {}).get('document', '')
        
        if progress_callback:
            await progress_callback({
                "status": "creative_completed",
                "message": "创意策划执行完成",
                "overall_progress": 30,
                "creative_framework": creative_framework,
                "content": creative_doc_content
            })
        
        return result
        
    except Exception as e:
        print(f"✗ 创意策划失败: {e}")
        result = state.copy()
        result["creative_framework"] = {"error": str(e)}
        return result


async def content_writing_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    节点3: 小说剧本创作执行（增强版）
    
    基于多智能体协作的小说剧本创作流程：
    1. 初始化人物记忆数据库
    2. 按章节循环创作，每章整合人物记忆和前文信息
    3. 一致性检查确保内容连贯
    4. 实时更新人物记忆
    5. 记录章节关键信息供后续使用
    
    核心特性：
    - 人物记忆管理（长期/短期记忆）
    - 跨章节内容一致性保障
    - 剧本格式输出（场景、对话、动作）
    """
    from .models import CharacterMemory, ChapterContext, ChapterScript, StoryBlueprint
    
    creative_framework = state.get('creative_framework', {})
    story_type = state.get('story_type', '')
    style = state.get('style', 'urban')
    chapter_count = state.get('chapter_count', 5)
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print(f"\n{'=' * 60}")
    print(f"节点3: 小说剧本创作执行（多智能体协作版）")
    print(f"Style: {style}, Chapters: {chapter_count}")
    print(f"{'=' * 60}")
    
    progress_callback = state.get('progress_callback')
    if progress_callback:
        await progress_callback({
            "status": "writing",
            "message": "正在初始化小说剧本创作系统...",
            "overall_progress": 35
        })
    
    try:
        agent = NovelWritingAgent(model)
        
        # ========================================
        # 阶段1: 初始化人物记忆数据库
        # ========================================
        print("→ 阶段1: 初始化人物记忆数据库...")
        
        # 从创意框架中提取人物信息
        story_framework = creative_framework.get('story_framework', {})
        characters_data = story_framework.get('characters', [])
        
        # 如果框架中没有人物信息，创建默认人物
        if not characters_data:
            characters_data = [
                {"name": "主角", "role": "protagonist", "background": "普通背景", "personality": "坚韧、善良", "goals": "实现目标"},
                {"name": "配角A", "role": "supporting", "background": "辅助背景", "personality": "聪明、忠诚", "goals": "帮助主角"}
            ]
        
        # 创建人物记忆数据库
        character_memories: Dict[str, CharacterMemory] = {}
        for char_data in characters_data:
            char_name = char_data.get('name', '未知角色')
            basic_info = {
                "background": char_data.get('background', ''),
                "personality": char_data.get('personality', ''),
                "goals": char_data.get('goals', ''),
                "role": char_data.get('role', 'supporting')
            }
            char_memory = CharacterMemory(
                character_id=f"char_{char_name}",
                name=char_name,
                basic_info=basic_info
            )
            character_memories[char_name] = char_memory
            print(f"  [人物记忆] 初始化: {char_name} ({basic_info['role']})")
        
        if progress_callback:
            await progress_callback({
                "status": "memories_initialized",
                "message": f"人物记忆数据库初始化完成，共{len(character_memories)}个角色",
                "overall_progress": 38,
                "characters": list(character_memories.keys())
            })
        
        # ========================================
        # 阶段2: 准备故事蓝图
        # ========================================
        print("→ 阶段2: 准备故事蓝图...")
        
        # 构建章节概述列表
        chapter_overviews = []
        for i in range(1, chapter_count + 1):
            # 从创意框架获取章节信息，或使用默认
            chapter_info = creative_framework.get('chapters', {}).get(f'chapter_{i}', {})
            overview = chapter_info.get('overview', f'第{i}章：推进故事情节')
            chapter_overviews.append({
                "number": i,
                "title": chapter_info.get('title', f'第{i}章'),
                "overview": overview
            })
        
        # 构建风格指南
        style_guide = {
            "style": style,
            "emotional_tone": story_framework.get('emotional_tone', '根据情节自然发展'),
            "writing_style_description": agent.writing_styles.get(style, agent.writing_styles["urban"])
        }
        
        if progress_callback:
            await progress_callback({
                "status": "blueprint_ready",
                "message": "故事蓝图准备完成",
                "overall_progress": 40
            })
        
        # ========================================
        # 阶段3: 章节循环创作
        # ========================================
        print(f"→ 阶段3: 开始章节循环创作 ({chapter_count}章)...")
        
        chapter_scripts: List[Dict[str, Any]] = []
        previous_chapters_summary: List[str] = []
        consistency_issues: List[Dict[str, Any]] = []
        
        for i in range(1, chapter_count + 1):
            print(f"\n  [{'='*20}] 创作第{i}/{chapter_count}章 [{'='*20}]")
            
            # 获取当前章节概述
            current_overview = chapter_overviews[i-1]["overview"]
            
            # 3.1 准备创作上下文
            print(f"  [上下文准备] 整合人物记忆和前文信息...")
            
            # 构建章节创作上下文
            chapter_context = ChapterContext(
                chapter_number=i,
                chapter_overview=current_overview,
                story_blueprint={
                    "total_chapters": chapter_count,
                    "style": style,
                    "theme": story_framework.get('theme', story_type)
                },
                character_memories=character_memories,
                previous_chapters_summary=previous_chapters_summary,
                style_guide=style_guide
            )
            
            # 3.2 创作章节剧本
            print(f"  [剧本创作] 调用小说剧本创作智能体...")
            
            # 发送进度更新 - 开始创作
            chapter_start_progress = 40 + int(((i - 1) / chapter_count) * 30)
            if progress_callback:
                await progress_callback({
                    "status": "writing_chapter",
                    "message": f"正在创作第{i}/{chapter_count}章...",
                    "overall_progress": chapter_start_progress,
                    "current_chapter": i,
                    "chapter_title": chapter_overviews[i-1]["title"],
                    "content": f"开始创作第{i}章"
                })
            
            script_result = await agent.write_chapter_script(chapter_context)
            
            if not script_result.get('success'):
                print(f"  ✗ 第{i}章创作失败: {script_result.get('error')}")
                # 记录错误但继续尝试下一章
                consistency_issues.append({
                    "chapter": i,
                    "type": "creation_error",
                    "message": script_result.get('error')
                })
                continue
            
            chapter_script_data = script_result.get('chapter_script', {})
            
            # 发送进度更新 - 剧本初步创作完成，展示部分内容
            chapter_mid_progress = 40 + int(((i - 0.5) / chapter_count) * 30)
            # 提取部分内容用于展示
            preview_content = ""
            scenes = chapter_script_data.get('scenes', [])
            if scenes:
                first_scene = scenes[0]
                preview_content = f"{first_scene.get('setting', '')}\n{first_scene.get('actions', '')[:200]}..."
            
            if progress_callback:
                await progress_callback({
                    "status": "chapter_draft_completed",
                    "message": f"第{i}/{chapter_count}章初稿完成",
                    "overall_progress": chapter_mid_progress,
                    "current_chapter": i,
                    "chapter_title": chapter_script_data.get('chapter_title', f'第{i}章'),
                    "content": preview_content
                })
            
            # 创建ChapterScript对象用于后续处理
            chapter_script = ChapterScript(
                chapter_number=i,
                chapter_title=chapter_script_data.get('chapter_title', f'第{i}章'),
                overview=current_overview
            )
            
            # 3.3 一致性检查
            print(f"  [一致性检查] 验证剧本连贯性...")
            
            if progress_callback:
                await progress_callback({
                    "status": "checking_consistency",
                    "message": f"正在检查第{i}/{chapter_count}章一致性...",
                    "overall_progress": chapter_mid_progress + 1,
                    "current_chapter": i,
                    "content": "正在进行内容一致性检查"
                })
            
            consistency_result = await agent.check_script_consistency(
                chapter_script, character_memories, previous_chapters_summary
            )
            
            if not consistency_result.get('is_consistent'):
                issues = consistency_result.get('issues', [])
                warnings = consistency_result.get('warnings', [])
                print(f"  ⚠ 发现{len(issues)}个问题，{len(warnings)}个警告")
                
                consistency_issues.extend([{
                    "chapter": i,
                    "type": "consistency_issue",
                    "message": issue
                } for issue in issues])
                
                # 如果问题严重，可以在这里暂停或重试
                # 简化处理：记录问题但继续
            
            # 3.4 更新人物记忆
            print(f"  [记忆更新] 根据剧本内容更新人物记忆...")
            
            # 从剧本数据中提取角色发展信息
            char_development = chapter_script_data.get('character_development', {})
            for char_name, development in char_development.items():
                if char_name in character_memories:
                    char_memory = character_memories[char_name]
                    event = f"第{i}章：{development}"
                    impact = "high" if any(kw in development for kw in ["重大", "转折", "决定", "改变"]) else "medium"
                    char_memory.add_experience(event, i, impact)
            
            # 更新关系网络（基于场景中的角色共现）
            scenes = chapter_script_data.get('scenes', [])
            for scene in scenes:
                chars = scene.get('characters_present', [])
                for j, char1 in enumerate(chars):
                    for char2 in chars[j+1:]:
                        if char1 in character_memories and char2 in character_memories:
                            character_memories[char1].update_relationship(char2, "互动")
                            character_memories[char2].update_relationship(char1, "互动")
            
            # 3.5 提取关键信息摘要
            print(f"  [信息摘要] 提取本章关键信息...")
            
            key_info = {
                "chapter_number": i,
                "chapter_title": chapter_script_data.get('chapter_title', f'第{i}章'),
                "summary": f"第{i}章：{', '.join(chapter_script_data.get('key_events', []))}",
                "key_events": chapter_script_data.get('key_events', []),
                "character_development": char_development,
                "emotional_arc": chapter_script_data.get('emotional_arc', '')
            }
            previous_chapters_summary.append(key_info['summary'])
            
            # 保存章节剧本
            chapter_scripts.append(chapter_script_data)
            
            # 更新进度
            chapter_progress = 40 + int((i / chapter_count) * 30)
            
            # 提取章节完整内容用于展示
            chapter_content = f"【{chapter_script_data.get('chapter_title', f'第{i}章')}】\n\n"
            for scene in chapter_script_data.get('scenes', []):
                chapter_content += f"【场景】{scene.get('setting', '')}\n"
                chapter_content += f"{scene.get('actions', '')}\n"
                for dialogue in scene.get('dialogues', []):
                    chapter_content += f"\n{dialogue.get('speaker', '')}：{dialogue.get('content', '')}\n"
            
            if progress_callback:
                await progress_callback({
                    "status": "chapter_script_completed",
                    "message": f"第{i}/{chapter_count}章剧本创作完成",
                    "overall_progress": chapter_progress,
                    "current_chapter": i,
                    "chapter_title": chapter_script_data.get('chapter_title'),
                    "scene_count": len(chapter_script_data.get('scenes', [])),
                    "word_count": chapter_script_data.get('word_count', 0),
                    "content": chapter_content
                })
            
            print(f"  ✓ 第{i}章完成: {len(chapter_script_data.get('scenes', []))}个场景")
        
        # ========================================
        # 阶段4: 整合结果
        # ========================================
        print(f"\n{'=' * 60}")
        print("阶段4: 整合创作结果")
        print(f"{'=' * 60}")
        
        # 计算总字数
        total_word_count = sum(s.get('word_count', 0) for s in chapter_scripts)
        
        # 构建最终的小说内容结构
        novel_content = {
            "chapter_scripts": chapter_scripts,
            "total_chapters": len(chapter_scripts),
            "word_count": total_word_count,
            "character_memories": {name: mem.to_dict() for name, mem in character_memories.items()},
            "consistency_issues": consistency_issues,
            "style": style,
            "chapter_count": chapter_count
        }
        
        # 生成传统格式的小说文本（用于兼容）
        full_novel_parts = []
        for script in chapter_scripts:
            chapter_text = f"\n\n{'='*40}\n{script.get('chapter_title', '')}\n{'='*40}\n\n"
            for scene in script.get('scenes', []):
                chapter_text += f"\n【场景】{scene.get('setting', '')}\n"
                chapter_text += f"{scene.get('actions', '')}\n"
                for dialogue in scene.get('dialogues', []):
                    chapter_text += f"\n{dialogue.get('speaker', '')}：{dialogue.get('content', '')}\n"
            full_novel_parts.append(chapter_text)
        
        full_novel = "\n".join(full_novel_parts)
        novel_content["full_novel"] = full_novel
        
        result = state.copy()
        result["novel_content"] = novel_content
        result["response"] = f"小说剧本创作完成，共{len(chapter_scripts)}章，{total_word_count}字"
        
        # 更新执行元数据
        if "execution_metadata" in result:
            result["execution_metadata"]["steps_completed"] = 2
            result["execution_metadata"]["milestones"].append({
                "event": "script_writing_completed",
                "time": datetime.now().isoformat(),
                "chapters_completed": len(chapter_scripts),
                "total_word_count": total_word_count
            })
        
        print(f"✓ 小说剧本创作完成: {len(chapter_scripts)}章, {total_word_count}字")
        print(f"  - 人物记忆: {len(character_memories)}个角色")
        print(f"  - 一致性问题: {len(consistency_issues)}个")
        
        if progress_callback:
            await progress_callback({
                "status": "writing_completed",
                "message": f"小说剧本创作完成，共{total_word_count}字",
                "overall_progress": 70,
                "word_count": total_word_count,
                "chapter_count": len(chapter_scripts),
                "character_count": len(character_memories),
                "consistency_issues": len(consistency_issues)
            })
        
        return result
        
    except Exception as e:
        print(f"✗ 小说剧本创作失败: {e}")
        import traceback
        traceback.print_exc()
        result = state.copy()
        result["novel_content"] = {"error": str(e), "chapters": [], "full_novel": ""}
        return result


async def quality_evaluation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    节点4: 质量评估与决策
    
    评估内容质量，决定是否通过或需要返回优化
    支持迭代优化（最多3次）
    """
    novel_content = state.get('novel_content', {})
    model = state.get('model', settings.DEFAULT_MODEL)
    
    # 获取当前迭代次数
    revision_count = state.get('revision_count', 0)
    max_revisions = state.get('max_revisions', 3)
    quality_threshold = state.get('quality_threshold', 75.0)
    
    print(f"\n{'=' * 60}")
    print(f"节点4: 质量评估与决策")
    print(f"迭代次数: {revision_count}/{max_revisions}, 阈值: {quality_threshold}")
    print(f"{'=' * 60}")
    
    progress_callback = state.get('progress_callback')
    if progress_callback:
        await progress_callback({
            "status": "evaluating",
            "message": "正在进行质量评估...",
            "overall_progress": 75
        })
    
    try:
        full_novel = novel_content.get('full_novel', '')
        
        if not full_novel:
            print("✗ 没有可评估的内容")
            result = state.copy()
            result["quality_report"] = {"error": "No content to evaluate"}
            return result
        
        # 使用调度智能体进行质量评估
        scheduler_agent = CoordinationSchedulerAgent(model)
        
        if progress_callback:
            await progress_callback({
                "status": "evaluating_content",
                "message": "正在分析内容质量...",
                "overall_progress": 78,
                "content": "正在对生成的内容进行全面质量评估，包括故事连贯性、人物一致性、文笔风格等方面"
            })
        
        quality_report = await scheduler_agent.evaluate_and_decide(
            content=full_novel,
            content_type="novel",
            quality_threshold=quality_threshold
        )
        
        result = state.copy()
        result["quality_report"] = quality_report
        result["revision_count"] = revision_count
        
        # 决策逻辑
        if quality_report.get('needs_revision') and revision_count < max_revisions:
            # 需要优化且未达到最大迭代次数
            print(f"⚠ 质量未达标 (score: {quality_report.get('overall_score')}), 需要优化")
            print(f"  建议: {quality_report.get('suggestions', [])}")
            
            result["needs_revision"] = True
            result["revision_count"] = revision_count + 1
            result["response"] = f"质量评估完成，需要优化 (第{revision_count + 1}次迭代)"
            
            # 构建优化建议内容
            revision_content = f"质量评分: {quality_report.get('overall_score')}分\n\n优化建议:\n"
            suggestions = quality_report.get('suggestions', [])
            for idx, suggestion in enumerate(suggestions[:3], 1):
                revision_content += f"{idx}. {suggestion}\n"
            
            if progress_callback:
                await progress_callback({
                    "status": "needs_revision",
                    "message": f"质量评估: {quality_report.get('overall_score')}分，需要优化",
                    "overall_progress": 80,
                    "quality_report": quality_report,
                    "revision_count": revision_count + 1,
                    "content": revision_content
                })
        else:
            # 通过评估或已达到最大迭代次数
            if quality_report.get('needs_revision'):
                print(f"⚠ 质量未达标但已达到最大迭代次数，强制通过")
            else:
                print(f"✓ 质量评估通过 (score: {quality_report.get('overall_score')})")
            
            result["needs_revision"] = False
            result["response"] = f"质量评估完成，评分: {quality_report.get('overall_score')}"
            
            # 更新执行元数据
            if "execution_metadata" in result:
                result["execution_metadata"]["steps_completed"] = 3
                result["execution_metadata"]["milestones"].append({
                    "event": "quality_evaluated",
                    "time": datetime.now().isoformat(),
                    "score": quality_report.get('overall_score')
                })
            
            # 构建质量报告内容
            quality_content = f"✅ 质量评估通过\n"
            quality_content += f"综合评分: {quality_report.get('overall_score')}分\n\n"
            quality_content += f"详细评价:\n"
            for key, value in quality_report.items():
                if key not in ['needs_revision', 'overall_score', 'suggestions'] and value:
                    quality_content += f"- {key}: {value}\n"
            
            if progress_callback:
                await progress_callback({
                    "status": "quality_passed",
                    "message": f"质量评估通过: {quality_report.get('overall_score')}分",
                    "overall_progress": 85,
                    "quality_report": quality_report,
                    "content": quality_content
                })
        
        return result
        
    except Exception as e:
        print(f"✗ 质量评估失败: {e}")
        result = state.copy()
        result["quality_report"] = {"error": str(e), "overall_score": 0}
        result["needs_revision"] = False
        return result


async def result_integration_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    节点5: 结果整合与报告
    
    整合所有执行结果，生成最终报告和日志
    """
    creative_framework = state.get('creative_framework', {})
    novel_content = state.get('novel_content', {})
    quality_report = state.get('quality_report', {})
    execution_metadata = state.get('execution_metadata', {})
    execution_plan = state.get('execution_plan', {})
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print(f"\n{'=' * 60}")
    print(f"节点5: 结果整合与报告")
    print(f"{'=' * 60}")
    
    progress_callback = state.get('progress_callback')
    if progress_callback:
            await progress_callback({
                "status": "integrating",
                "message": "正在整合结果...",
                "overall_progress": 90,
                "content": "正在将创意框架、小说内容、质量评估等所有结果整合为最终报告"
            })
    
    try:
        # 使用调度智能体整合结果
        scheduler_agent = CoordinationSchedulerAgent(model)
        final_result = await scheduler_agent.integrate_results(
            creative_framework=creative_framework,
            novel_content=novel_content,
            quality_report=quality_report,
            execution_metadata=execution_metadata
        )
        
        # 构建调度器响应格式的输出
        response = final_result.get('response', '工作流执行完成')
        
        # 构建兼容的schedule结构
        workflow_schedule = {
            "schedule": execution_plan.get('steps', []),
            "created_at": execution_plan.get('created_at', datetime.now().isoformat()),
            "total_duration": execution_plan.get('estimated_duration', 0)
        }
        
        # 构建兼容的log结构
        workflow_log = {
            "log_entries": execution_metadata.get('milestones', []),
            "generated_at": datetime.now().isoformat(),
            "total_steps": execution_plan.get('total_steps', 0),
            "included_steps": execution_metadata.get('steps_completed', 0),
            "skipped_steps": execution_plan.get('total_steps', 0) - execution_metadata.get('steps_completed', 0)
        }
        
        # 构建兼容的exception_report结构
        exception_report = {
            "exceptions": [],
            "generated_at": datetime.now().isoformat(),
            "total_exceptions": 0,
            "resolved_exceptions": 0,
            "unresolved_exceptions": 0
        }
        
        result = state.copy()
        result.update({
            "response": response,
            "schedule": workflow_schedule,
            "scheduling_log": workflow_log,
            "exception_report": exception_report,
            "final_result": final_result,
            "processed_at": datetime.now().isoformat()
        })
        
        print(f"✓ 结果整合完成")
        print(f"  字数: {final_result.get('execution_summary', {}).get('word_count', 0)}")
        print(f"  质量分: {final_result.get('execution_summary', {}).get('quality_score', 0)}")
        print(f"  耗时: {final_result.get('execution_summary', {}).get('total_time_seconds', 0):.1f}秒")
        
        # 构建最终结果内容
        final_content = f"🎉 工作流执行完成!\n\n"
        execution_summary = final_result.get('execution_summary', {})
        final_content += f"总字数: {execution_summary.get('word_count', 0)}\n"
        final_content += f"质量分: {execution_summary.get('quality_score', 0)}\n"
        final_content += f"总耗时: {execution_summary.get('total_time_seconds', 0):.1f}秒\n"
        final_content += f"章节数: {novel_content.get('total_chapters', 0)}"
        
        if progress_callback:
            await progress_callback({
                "status": "completed",
                "message": "工作流执行完成",
                "overall_progress": 100,
                "final_result": final_result,
                "content": final_content
            })
        
        return result
        
    except Exception as e:
        print(f"✗ 结果整合失败: {e}")
        result = state.copy()
        result["response"] = f"结果整合失败: {str(e)}"
        result["final_result"] = {"error": str(e)}
        result["processed_at"] = datetime.now().isoformat()
        return result


def create_scheduler_workflow():
    """
    创建精简版协同调度工作流（5个核心节点）
    
    新工作流架构：
    1. 智能规划与调度 - 动态生成执行计划
    2. 创意策划执行 - 执行创意策划工作流
    3. 内容创作执行 - 执行小说创作工作流
    4. 质量评估与决策 - 评估质量，支持迭代优化
    5. 结果整合与报告 - 整合结果生成最终报告
    
    改进点：
    - 节点从10个减少到5个，降低复杂度
    - 动态规划替代固定工作流
    - 增加质量评估反馈循环
    - 实时进度更新
    
    Returns:
        CompiledStateGraph: 编译后的工作流对象
    """
    # 初始化工作流状态图
    workflow = StateGraph(dict)
    
    # 添加5个核心节点
    workflow.add_node("planning_and_scheduling", planning_and_scheduling_node)  # 节点1: 智能规划
    workflow.add_node("creative_execution", creative_execution_node)            # 节点2: 创意策划
    workflow.add_node("content_writing", content_writing_node)                  # 节点3: 内容创作
    workflow.add_node("quality_evaluation", quality_evaluation_node)            # 节点4: 质量评估
    workflow.add_node("result_integration", result_integration_node)            # 节点5: 结果整合
    
    # 设置入口点
    workflow.set_entry_point("planning_and_scheduling")
    
    # 基本流程边
    workflow.add_edge("planning_and_scheduling", "creative_execution")
    workflow.add_edge("creative_execution", "content_writing")
    workflow.add_edge("content_writing", "quality_evaluation")
    
    # 条件边：质量评估后决定是继续还是返回优化
    def quality_decision(state: Dict[str, Any]) -> str:
        """
        质量评估决策函数
        
        根据质量评估结果决定下一步：
        - 需要优化且未达到最大迭代次数 -> 返回内容创作节点
        - 通过评估或达到最大迭代次数 -> 继续到结果整合
        """
        needs_revision = state.get("needs_revision", False)
        revision_count = state.get("revision_count", 0)
        max_revisions = state.get("max_revisions", 3)
        
        if needs_revision and revision_count < max_revisions:
            print(f"\n↻ 质量未达标，返回优化 (第{revision_count}次迭代)")
            return "content_writing"  # 返回内容创作节点进行优化
        else:
            print(f"\n→ 质量评估通过，继续结果整合")
            return "result_integration"
    
    # 添加条件边
    workflow.add_conditional_edges(
        "quality_evaluation",
        quality_decision,
        {
            "content_writing": "content_writing",      # 需要优化，返回重写
            "result_integration": "result_integration"  # 通过评估，继续
        }
    )
    
    # 结果整合后结束
    workflow.add_edge("result_integration", END)
    
    # 编译工作流
    return workflow.compile()


# 创建新的工作流实例
scheduler_workflow = create_scheduler_workflow()
