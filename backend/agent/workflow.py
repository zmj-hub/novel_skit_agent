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
        adapted_workflow = await agent.adapt_agent_workflow(schedule)
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


async def execute_workflow_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行工作流节点
    """
    adapted_workflow = state.get('adapted_workflow')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print("Executing workflow steps...")
    print(f"Adapted workflow: {adapted_workflow}")
    
    # 这里可以添加实际执行工作流的逻辑
    # 例如，调用创意生成和小说创作智能体
    
    # 返回包含原始状态的数据
    result = state.copy()
    result["response"] = "Workflow execution initiated"
    return result


async def generate_reports_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成报告节点
    """
    schedule = state.get('schedule')
    conflict_detection = state.get('conflict_detection')
    conflict_resolution = state.get('conflict_resolution')
    resource_allocations = state.get('resource_allocations')
    adapted_workflow = state.get('adapted_workflow')
    task_plan = state.get('task_plan')
    task_breakdown = state.get('task_breakdown')
    agent_allocation = state.get('agent_allocation')
    progress_tracking = state.get('progress_tracking')
    result_summary = state.get('result_summary')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print("Generating scheduling logs and exception reports...")
    
    try:
        agent = CoordinationSchedulerAgent(model)
        scheduling_log = await agent.generate_scheduling_log(schedule, resource_allocations, adapted_workflow)
        exception_report = await agent.generate_exception_report(conflict_detection, conflict_resolution)
        # 返回包含原始状态的数据
        result = state.copy()
        result["scheduling_log"] = scheduling_log
        result["exception_report"] = exception_report
        result["response"] = "Reports generated successfully"
        result["processed_at"] = datetime.datetime.now().isoformat()
        return result
    except Exception as e:
        print(f"Warning: Failed to generate reports: {e}")
        # 返回包含原始状态的数据
        result = state.copy()
        result["scheduling_log"] = {"log_entries": [], "generated_at": "Error", "total_steps": 0, "included_steps": 0, "skipped_steps": 0}
        result["exception_report"] = {"exceptions": [], "generated_at": "Error", "total_exceptions": 0, "resolved_exceptions": 0, "unresolved_exceptions": 0}
        result["response"] = "Error generating reports"
        result["processed_at"] = datetime.datetime.now().isoformat()
        return result


async def task_planning_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    任务规划节点
    """
    story_description = state.get('story_description', '')
    story_type = state.get('story_type', '')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print(f"Planning task for story: {story_type}")
    print(f"Story description: {story_description[:100]}...")
    
    try:
        agent = CoordinationSchedulerAgent(model)
        task_plan = await agent.plan_story_task(story_description, story_type)
        # 返回包含原始状态的数据
        result = state.copy()
        result["task_plan"] = task_plan
        return result
    except Exception as e:
        print(f"Warning: Failed to plan story task: {e}")
        # 返回包含原始状态的数据
        result = state.copy()
        result["task_plan"] = {"story_type": story_type, "plan": "Error", "estimated_duration": 0}
        return result


async def task_breakdown_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    任务拆解节点
    """
    task_plan = state.get('task_plan')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print("Breaking down task into subtasks...")
    
    try:
        agent = CoordinationSchedulerAgent(model)
        task_breakdown = await agent.breakdown_task(task_plan)
        # 返回包含原始状态的数据
        result = state.copy()
        result["task_breakdown"] = task_breakdown
        return result
    except Exception as e:
        print(f"Warning: Failed to breakdown task: {e}")
        # 返回包含原始状态的数据
        result = state.copy()
        result["task_breakdown"] = {"subtasks": [], "breakdown_at": "Error"}
        return result


async def agent_allocation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    智能体分配节点
    """
    task_breakdown = state.get('task_breakdown')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print("Allocating subtasks to agents...")
    
    try:
        agent = CoordinationSchedulerAgent(model)
        agent_allocation = await agent.allocate_tasks_to_agents(task_breakdown)
        # 返回包含原始状态的数据
        result = state.copy()
        result["agent_allocation"] = agent_allocation
        return result
    except Exception as e:
        print(f"Warning: Failed to allocate tasks to agents: {e}")
        # 返回包含原始状态的数据
        result = state.copy()
        result["agent_allocation"] = {"allocations": [], "allocated_at": "Error"}
        return result


async def progress_tracking_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    进度跟踪节点
    """
    agent_allocation = state.get('agent_allocation')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print("Tracking task progress...")
    
    try:
        agent = CoordinationSchedulerAgent(model)
        progress_tracking = await agent.track_task_progress(agent_allocation)
        # 返回包含原始状态的数据
        result = state.copy()
        result["progress_tracking"] = progress_tracking
        return result
    except Exception as e:
        print(f"Warning: Failed to track task progress: {e}")
        # 返回包含原始状态的数据
        result = state.copy()
        result["progress_tracking"] = {"progress": 0, "status": "Error", "tracking_at": "Error"}
        return result


async def result_summary_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    结果汇总节点
    """
    progress_tracking = state.get('progress_tracking')
    model = state.get('model', settings.DEFAULT_MODEL)
    
    print("Summarizing task results...")
    
    try:
        agent = CoordinationSchedulerAgent(model)
        result_summary = await agent.summarize_task_results(progress_tracking)
        # 返回包含原始状态的数据
        result = state.copy()
        result["result_summary"] = result_summary
        result["response"] = "Task completed successfully"
        return result
    except Exception as e:
        print(f"Warning: Failed to summarize task results: {e}")
        # 返回包含原始状态的数据
        result = state.copy()
        result["result_summary"] = {"summary": "Error", "completed_at": "Error"}
        result["response"] = "Error summarizing task results"
        return result


def create_scheduler_workflow():
    """
    创建协同调度工作流
    """
    workflow = StateGraph(dict)
    
    # 原有节点
    workflow.add_node("create_schedule", create_schedule_node)
    workflow.add_node("detect_conflicts", detect_conflicts_node)
    workflow.add_node("allocate_resources", allocate_resources_node)
    
    # 新增节点
    workflow.add_node("task_planning", task_planning_node)
    workflow.add_node("task_breakdown", task_breakdown_node)
    workflow.add_node("agent_allocation", agent_allocation_node)
    workflow.add_node("progress_tracking", progress_tracking_node)
    workflow.add_node("result_summary", result_summary_node)
    
    # 原有节点
    workflow.add_node("execute_workflow", execute_workflow_node)
    workflow.add_node("generate_reports", generate_reports_node)
    
    # 设置工作流流程
    workflow.set_entry_point("task_planning")
    workflow.add_edge("task_planning", "task_breakdown")
    workflow.add_edge("task_breakdown", "agent_allocation")
    workflow.add_edge("agent_allocation", "create_schedule")
    workflow.add_edge("create_schedule", "detect_conflicts")
    workflow.add_edge("detect_conflicts", "allocate_resources")
    workflow.add_edge("allocate_resources", "execute_workflow")
    workflow.add_edge("execute_workflow", "progress_tracking")
    workflow.add_edge("progress_tracking", "result_summary")
    workflow.add_edge("result_summary", "generate_reports")
    workflow.add_edge("generate_reports", END)
    
    return workflow.compile()


scheduler_workflow = create_scheduler_workflow()
