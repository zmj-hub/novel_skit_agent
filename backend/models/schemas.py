from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import datetime


class ChatRequest(BaseModel):
    message: str = Field(..., description="用户消息", example="什么是 RAG 技术？")
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    use_knowledge: bool = Field(default=True, description="是否使用知识库", example=True)
    model: str = Field(default="deepseek-chat", description="使用的模型", example="deepseek-chat")


class ChatResponse(BaseModel):
    response: str = Field(..., description="AI 响应", example="RAG (Retrieval-Augmented Generation) 是一种结合了检索和生成的 AI 技术...")
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    sources: Optional[List[Dict[str, Any]]] = Field(default=None, description="引用的知识源", example=[])


class Message(BaseModel):
    role: str = Field(..., description="角色: user 或 assistant", example="user")
    content: str = Field(..., description="消息内容", example="你好，能帮我解释一下什么是 AI Agent 吗？")


class FileUploadResponse(BaseModel):
    filename: str = Field(..., description="上传的文件名", example="example.pdf")
    chunks_count: int = Field(..., description="处理后的文本块数量", example=10)
    status: str = Field(..., description="处理状态", example="success")


class KnowledgeBaseStatus(BaseModel):
    document_count: int = Field(..., description="知识库中的文档数量", example=5)
    vector_store_type: str = Field(..., description="向量存储类型", example="chromadb")
    status: str = Field(..., description="知识库状态", example="active")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="错误信息", example="内部服务器错误")
    code: int = Field(..., description="错误代码", example=500)


class ClearKnowledgeBaseResponse(BaseModel):
    status: str = Field(..., description="操作状态", example="success")
    message: str = Field(..., description="操作消息", example="Knowledge base cleared")


class CreativePlanningRequest(BaseModel):
    """
    创意策划请求模型
    """
    hotspots: List[str] = Field(..., description="市场热点元素列表", 
                               example=["人工智能", "职场压力", "都市情感"])
    story_type: str = Field(default="都市情感", description="故事类型", 
                           example="都市情感")
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    model: str = Field(default="deepseek-chat", description="使用的模型", 
                      example="deepseek-chat")


class CharacterBiography(BaseModel):
    """
    人物小传模型
    """
    name: str = Field(..., description="人物姓名", example="林雨晴")
    background: str = Field(..., description="背景故事", example="30岁，AI公司产品经理")
    personality: str = Field(..., description="性格特征", example="独立坚强，内心敏感")
    motivation: str = Field(..., description="目标动机", example="追求职业成功，寻找真爱")
    character_arc: str = Field(..., description="人物弧光", example="从自我封闭到敞开心扉")


class PlotOutline(BaseModel):
    """
    剧情大纲模型
    """
    novel_chapters: List[str] = Field(..., description="小说章回结构", 
                                    example=["第一章：职场危机", "第二章：意外相遇", "第三章：情感纠葛"])
    skit_episodes: List[str] = Field(..., description="短剧集数结构", 
                                   example=["第一集：职场挑战", "第二集：偶遇旧爱", "第三集：抉择时刻"])


class PlotTwist(BaseModel):
    """
    核心反转节点模型
    """
    position: str = Field(..., description="转折点位置", example="第二集结尾")
    content: str = Field(..., description="转折点内容", example="女主角发现男主角是竞争对手公司的卧底")
    emotional_impact: str = Field(..., description="情感冲击力评估", example="高")


class StoryCreativeFramework(BaseModel):
    """
    故事创意框架模型
    """
    title: str = Field(..., description="故事标题", example="AI时代的情感抉择")
    characters: List[CharacterBiography] = Field(..., description="人物小传列表")
    plot_outline: PlotOutline = Field(..., description="剧情大纲")
    plot_twists: List[PlotTwist] = Field(..., description="核心反转节点列表")
    theme: str = Field(..., description="故事主题", example="在科技发展中寻找人性的温度")
    commercial_feasibility: str = Field(..., description="商业可行性评估", example="高")
    emotional_resonance: str = Field(..., description="情感共鸣力评估", example="高")
    cross_media_potential: str = Field(..., description="跨媒介改编潜力评估", example="高")


class CreativePlanningResponse(BaseModel):
    """
    创意策划响应模型
    """
    response: str = Field(..., description="创意策划响应", 
                        example="《故事创意框架》文档已生成")
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    creative_document: str = Field(..., description="《故事创意框架》文档内容")
    story_framework: Optional[StoryCreativeFramework] = Field(None, 
                                                           description="故事创意框架数据结构")
    sources: Optional[List[Dict[str, Any]]] = Field(default=None, 
                                                  description="引用的知识源", example=[])


class WritingStyle(BaseModel):
    """
    文风配置模型
    """
    style_type: str = Field(..., description="文风类型", 
                          example="sweet")
    style_name: str = Field(..., description="文风名称", 
                          example="甜宠风格")
    description: str = Field(..., description="文风描述", 
                           example="语言温馨浪漫，情感细腻，情节轻松愉快")


class NovelChapter(BaseModel):
    """
    小说章节模型
    """
    chapter_number: int = Field(..., description="章节编号", example=1)
    chapter_title: str = Field(..., description="章节标题", 
                             example="第一章：邂逅")
    chapter_content: str = Field(..., description="章节内容", 
                               example="林雨晴站在公司楼下，看着眼前熟悉的建筑，心中五味杂陈...")
    suspense_hook: str = Field(..., description="悬念钩子", 
                             example="就在她转身离开的瞬间，一个熟悉的声音从背后传来...")


class QualityEvaluation(BaseModel):
    """
    质量评估模型
    """
    read_rate_factors: List[str] = Field(..., description="完读率影响因素", 
                                       example=["情节吸引力强", "人物塑造立体", "冲突设计合理"])
    style_consistency: float = Field(..., description="文风一致性评分", 
                                   example=95.5)
    suspense_effectiveness: str = Field(..., description="悬念钩子有效性", 
                                      example="高")
    optimization_suggestions: List[str] = Field(..., description="优化建议", 
                                               example=["增加细节描写", "强化情感渲染"])
    overall_score: int = Field(..., description="整体评分", example=92)


class NovelWritingRequest(BaseModel):
    """
    小说创作请求模型
    """
    creative_framework: str = Field(..., description="创意框架文档", 
                                   example="# 《墟境疗心人》故事框架\n\n## 1. 人物设定...")
    style: str = Field(default="urban", description="文风类型", 
                      example="sweet")
    chapter_count: int = Field(default=5, description="章节数量", 
                              example=5)
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    model: str = Field(default="deepseek-chat", description="使用的模型", 
                      example="deepseek-chat")


class NovelWritingResponse(BaseModel):
    """
    小说创作响应模型
    """
    response: str = Field(..., description="小说创作响应", 
                        example="《爆款短篇小说》已生成")
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    novel_content: str = Field(..., description="小说内容")
    chapters: Optional[List[NovelChapter]] = Field(None, 
                                                 description="小说章节列表")
    quality_evaluation: Optional[QualityEvaluation] = Field(None, 
                                                         description="质量评估结果")
    word_count: int = Field(..., description="字数统计", example=8000)
    style_used: str = Field(..., description="使用的文风", example="sweet")


class SchedulerRequest(BaseModel):
    """
    调度请求模型
    """
    story_description: str = Field(..., description="故事详细描述文本", 
                                 example="一个关于人工智能与人类情感的科幻故事，讲述了一个AI助手与它的主人之间逐渐发展的情感纽带，以及他们共同面对的挑战")
    story_type: str = Field(..., description="故事类型", 
                          example="科幻")
    request_priority: int = Field(default=1, description="请求优先级（1-5，5最高）", 
                                example=3)
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    model: str = Field(default="modelscope", description="使用的模型", 
                      example="modelscope")


class WorkflowStep(BaseModel):
    """
    工作流步骤模型
    """
    step_id: str = Field(..., description="步骤ID", example="creative_generation")
    step_name: str = Field(..., description="步骤名称", example="创意生成")
    start_time: str = Field(..., description="开始时间", example="2024-01-26T10:00:00")
    estimated_end_time: str = Field(..., description="预计结束时间", example="2024-01-26T11:00:00")
    duration_minutes: int = Field(..., description="持续时间（分钟）", example=60)
    agent_available: bool = Field(..., description="智能体是否可用", example=True)
    priority: int = Field(..., description="优先级", example=3)
    dependencies: List[str] = Field(..., description="依赖关系", 
                                   example=["market_analysis"])


class WorkflowSchedule(BaseModel):
    """
    工作时序表模型
    """
    schedule: List[WorkflowStep] = Field(..., description="工作流步骤列表")
    created_at: str = Field(..., description="创建时间", example="2024-01-26T10:00:00")
    total_duration: float = Field(..., description="总持续时间（分钟）", example=525)


class WorkflowLogEntry(BaseModel):
    """
    工作流日志条目模型
    """
    step_id: str = Field(..., description="步骤ID", example="creative_generation")
    step_name: str = Field(..., description="步骤名称", example="创意生成")
    start_time: str = Field(..., description="开始时间", example="2024-01-26T10:00:00")
    estimated_end_time: str = Field(..., description="预计结束时间", example="2024-01-26T11:00:00")
    duration_minutes: int = Field(..., description="持续时间（分钟）", example=60)
    status: str = Field(..., description="状态", example="included")
    agent_available: bool = Field(..., description="智能体是否可用", example=True)
    cpu_allocation: str = Field(..., description="CPU分配", example="4 cores")
    memory_allocation: str = Field(..., description="内存分配", example="8 GB")
    priority: int = Field(..., description="优先级", example=3)
    dependencies: List[str] = Field(..., description="依赖关系", 
                                   example=["market_analysis"])
    log_time: str = Field(..., description="日志时间", example="2024-01-26T10:00:00")


class WorkflowLog(BaseModel):
    """
    工作流调度日志模型
    """
    log_entries: List[WorkflowLogEntry] = Field(..., description="日志条目列表")
    generated_at: str = Field(..., description="生成时间", example="2024-01-26T10:00:00")
    total_steps: int = Field(..., description="总步骤数", example=6)
    included_steps: int = Field(..., description="包含的步骤数", example=2)
    skipped_steps: int = Field(..., description="跳过的步骤数", example=4)


class ExceptionEntry(BaseModel):
    """
    异常条目模型
    """
    conflict_id: str = Field(..., description="冲突ID", example="agent_unavailable_market_analysis")
    conflict_type: str = Field(..., description="冲突类型", example="agent_unavailable")
    step_name: str = Field(..., description="步骤名称", example="市场分析")
    description: str = Field(..., description="描述", example="市场分析环节的智能体尚未部署")
    severity: str = Field(..., description="严重程度", example="medium")
    resolution: str = Field(..., description="解决方案", example="skip")
    resolution_description: str = Field(..., description="解决方案描述", example="跳过市场分析环节，因为相关智能体尚未部署")
    prevention: str = Field(..., description="预防措施", example="建议部署市场分析智能体以完善工作流程")
    status: str = Field(..., description="状态", example="resolved")


class ExceptionReport(BaseModel):
    """
    异常处理报告模型
    """
    exceptions: List[ExceptionEntry] = Field(..., description="异常条目列表")
    generated_at: str = Field(..., description="生成时间", example="2024-01-26T10:00:00")
    total_exceptions: int = Field(..., description="总异常数", example=4)
    resolved_exceptions: int = Field(..., description="已解决的异常数", example=4)
    unresolved_exceptions: int = Field(..., description="未解决的异常数", example=0)


class SchedulerResponse(BaseModel):
    """
    调度响应模型
    """
    response: str = Field(..., description="调度响应", 
                        example="工作流调度已完成")
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    schedule: Optional[WorkflowSchedule] = Field(None, 
                                              description="工作时序表")
    workflow_log: Optional[WorkflowLog] = Field(None, 
                                              description="工作流调度日志")
    exception_report: Optional[ExceptionReport] = Field(None, 
                                                     description="异常处理报告")
    processed_at: str = Field(..., description="处理时间", example="2024-01-26T10:00:00")


class CollaborationRequest(BaseModel):
    """
    协作请求模型
    """
    task_goal: str = Field(..., description="任务目标", 
                         example="生成一个关于人工智能的故事创意，并创作故事剧本")
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    model: Optional[str] = Field(default=None, description="默认使用的模型", 
                                example="qwen3-30b-a3b")
    timeout: Optional[int] = Field(default=300, description="超时时间（秒）", 
                                  example=300)
    priority: Optional[int] = Field(default=1, description="请求优先级（1-5，5最高）", 
                                   example=3)
    writing_style: Optional[str] = Field(default="urban", description="文风类型", 
                                        example="urban")
    medium_type: Optional[str] = Field(default="novel", description="媒介类型", 
                                      example="novel")
    chapter_count: Optional[int] = Field(default=5, description="章节/场景数量", 
                                        example=5)
    models: Optional[Dict[str, str]] = Field(default_factory=dict, description="智能体模型配置", 
                                           example={"coordination": "Qwen/Qwen3-235B-A22B-Instruct-2507", "creative": "deepseek-chat", "story_script": "Qwen/Qwen3-30B-A3B-Instruct-2507"})
    model_parameters: Optional[Dict[str, Dict[str, Any]]] = Field(default_factory=dict, description="智能体模型参数配置", 
                                                                 example={"coordination": {"temperature": 0.6, "top_p": 0.95}, "creative": {"temperature": 0.8}, "story_script": {"temperature": 0.7}})


class CollaborationResponse(BaseModel):
    """
    协作响应模型
    """
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    task_goal: str = Field(..., description="任务目标", 
                         example="生成一个关于人工智能的故事创意，并撰写短篇小说")
    workflow_state: str = Field(..., description="工作流状态", 
                               example="completed")
    result: Optional[Dict[str, Any]] = Field(None, description="执行结果", 
                                           example={"execution_history": [], "reflection_records": []})
    error: Optional[str] = Field(None, description="错误信息", 
                               example="执行超时")
    execution_history: Optional[List[Dict[str, Any]]] = Field(None, 
                                                          description="执行历史")
    reflection_records: Optional[List[Dict[str, Any]]] = Field(None, 
                                                            description="反思记录")
    created_at: Optional[str] = Field(default_factory=lambda: datetime.datetime.now().isoformat(), 
                                     description="创建时间")
    updated_at: Optional[str] = Field(default_factory=lambda: datetime.datetime.now().isoformat(), 
                                     description="更新时间")


class NovelChaptersResponse(BaseModel):
    """
    小说章节响应模型
    """
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    chapters: List[NovelChapter] = Field(default_factory=list, description="小说章节列表")
    message: str = Field(..., description="响应消息", example="章节获取功能待实现")


class NovelExportResponse(BaseModel):
    """
    小说导出响应模型
    """
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    format: str = Field(..., description="导出格式", example="txt")
    message: str = Field(..., description="响应消息", example="小说导出功能待实现")


class CollaborationStatusResponse(BaseModel):
    """
    协作状态响应模型
    """
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    status: str = Field(..., description="协作状态", example="completed")
    message: str = Field(..., description="响应消息", example="协作状态查询功能正在开发中")


class CollaborationCancelResponse(BaseModel):
    """
    协作取消响应模型
    """
    session_id: str = Field(..., description="对话会话 ID", example="user_123")
    status: str = Field(..., description="取消状态", example="cancelled")
    message: str = Field(..., description="响应消息", example="协作取消功能正在开发中")
