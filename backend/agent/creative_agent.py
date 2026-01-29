from utils.async_llm import llm_manager
from core.config import settings
from core.agent_config import AgentType
from core.model_version import model_version_manager
from core.monitoring_decorator import monitor_execution_time
from core.error_handling_decorator import retry, ErrorHandler, ErrorContext, ModelError, NetworkError, TimeoutError
from core.redis import redis_manager
from typing import Dict, List, Any, Optional
import asyncio
import hashlib
import json


class CreativePlanningAgent:
    def __init__(self, model: str = None):
        self.model = model or model_version_manager.get_model_name("creative")
        self.llm = llm_manager.get_llm(self.model)
    
    @monitor_execution_time("creative")
    @retry(max_retries=3, agent_type="creative")
    async def analyze_hotspots(self, hotspots: List[str]) -> Dict[str, Any]:
        """
        分析市场热点元素
        
        Args:
            hotspots: 市场热点元素列表
            
        Returns:
            分析结果，包含热点元素的解读和应用建议
        """
        prompt = f"""
        作为专业的创意策划师，请分析以下市场热点元素，
        并提供这些元素在故事创作中的应用建议：
        
        热点元素：
        {', '.join(hotspots)}
        
        请从以下角度进行分析：
        1. 每个热点元素的核心含义和情感共鸣点
        2. 这些热点元素在故事创作中的潜在价值
        3. 如何将这些热点元素有机结合到故事中
        4. 可能的故事类型和风格建议
        """
        
        try:
            analysis = await self.llm.generate(prompt)
            return {
                "hotspots": hotspots,
                "analysis": analysis
            }
        except Exception as e:
            raise ModelError(f"分析热点元素失败: {e}")
    
    @monitor_execution_time("creative")
    @retry(max_retries=3, agent_type="creative")
    async def build_story_framework(self, hotspots_analysis: Dict[str, Any], story_type: str) -> Dict[str, Any]:
        """
        构建故事框架
        
        Args:
            hotspots_analysis: 热点元素分析结果
            story_type: 故事类型
            
        Returns:
            故事框架，包含人物设定、核心冲突和剧情脉络
        """
        prompt = f"""
        基于以下热点元素分析，为{story_type}类型的故事构建完整的故事框架：
        
        热点元素分析：
        {hotspots_analysis['analysis']}
        
        请构建以下内容：
        1. 人物设定：主要角色的背景、性格、目标和动机
        2. 核心冲突：故事的主要矛盾和冲突点
        3. 剧情脉络：故事的基本发展路径和关键节点
        4. 主题思想：故事想要表达的核心主题
        """
        
        try:
            framework = await self.llm.generate(prompt)
            return {
                "story_type": story_type,
                "framework": framework
            }
        except Exception as e:
            raise ModelError(f"构建故事框架失败: {e}")
    
    @monitor_execution_time("creative")
    @retry(max_retries=3, agent_type="creative")
    async def adapt_to_media(self, story_framework: Dict[str, Any]) -> Dict[str, Any]:
        """
        适配短剧和小说媒介
        
        Args:
            story_framework: 故事框架
            
        Returns:
            适配结果，包含短剧和小说的适配方案
        """
        prompt = f"""
        请将以下故事框架分别适配为短剧和小说两种媒介形式：
        
        故事框架：
        {story_framework['framework']}
        
        短剧适配要求：
        1. 设计符合短剧叙事规律的分镜逻辑
        2. 严格遵循每30秒设置1个小冲突
        3. 每3-5分钟设置1个大反转
        4. 控制剧集长度和节奏
        
        小说适配要求：
        1. 预留充足的小说拓展空间
        2. 包括细节描写、人物心理刻画、世界观构建等内容模块
        3. 设计适合小说阅读的章节结构
        4. 提供可以深入挖掘的情节线索
        """
        
        try:
            adaptation = await self.llm.generate(prompt)
            return {
                "story_type": story_framework['story_type'],
                "adaptation": adaptation
            }
        except Exception as e:
            raise ModelError(f"适配媒介失败: {e}")
    
    @monitor_execution_time("creative")
    @retry(max_retries=3, agent_type="creative")
    async def generate_creative_document(self, hotspots_analysis: Dict[str, Any], 
                                        story_framework: Dict[str, Any], 
                                        media_adaptation: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成标准化的《故事创意框架》文档
        
        Args:
            hotspots_analysis: 热点元素分析结果
            story_framework: 故事框架
            media_adaptation: 媒介适配结果
            
        Returns:
            标准化的《故事创意框架》文档
        """
        # 提取分析结果，确保即使结构不完整也能正常工作
        hotspots_analysis_content = hotspots_analysis.get('analysis', '暂无热点元素分析')
        story_framework_content = story_framework.get('framework', '暂无故事框架')
        media_adaptation_content = media_adaptation.get('adaptation', '暂无媒介适配方案')
        
        prompt = f"""
        请基于以下内容，生成一份标准化的《故事创意框架》文档：
        
        1. 热点元素分析：
        {hotspots_analysis_content}
        
        2. 故事框架：
        {story_framework_content}
        
        3. 媒介适配：
        {media_adaptation_content}
        
        《故事创意框架》文档必须包含以下核心内容：
        
        a) 人物小传：
        - 主要角色的背景故事
        - 性格特征
        - 目标动机
        - 人物弧光
        
        b) 剧情大纲：
        - 小说章回结构
        - 短剧集数结构
        
        c) 核心反转节点：
        - 明确标注所有关键转折点的位置
        - 内容
        - 情感冲击力评估
        
        文档格式要求：
        - 结构清晰，层次分明
        - 内容详细，逻辑严密
        - 符合商业可行性、情感共鸣力和跨媒介改编潜力的要求
        """
        
        try:
            document = await self.llm.generate(prompt)
            return {
                "document_type": "故事创意框架",
                "document": document
            }
        except Exception as e:
            raise ModelError(f"生成创意文档失败: {e}")
    
    def _generate_request_hash(self, hotspots: List[str], story_type: str) -> str:
        """
        生成请求哈希值
        
        Args:
            hotspots: 市场热点元素列表
            story_type: 故事类型
            
        Returns:
            请求哈希值
        """
        request_data = {
            "hotspots": sorted(hotspots),
            "story_type": story_type
        }
        return hashlib.md5(json.dumps(request_data, sort_keys=True).encode()).hexdigest()
    
    @monitor_execution_time("creative")
    async def process_creative_request(self, hotspots: List[str], story_type: str) -> Dict[str, Any]:
        """
        处理完整的创意策划请求
        
        Args:
            hotspots: 市场热点元素列表
            story_type: 故事类型
            
        Returns:
            完整的创意策划结果，包含《故事创意框架》文档
        """
        # 生成请求哈希
        request_hash = self._generate_request_hash(hotspots, story_type)
        
        # 检查缓存
        cached_response = await redis_manager.get_agent_response("creative", request_hash)
        if cached_response:
            return cached_response
        
        async with ErrorContext(agent_type="creative", operation="process_creative_request"):
            # 1. 分析热点元素
            hotspots_analysis = await self.analyze_hotspots(hotspots)
            
            # 2. 构建故事框架
            story_framework = await self.build_story_framework(hotspots_analysis, story_type)
            
            # 3. 适配短剧和小说媒介
            media_adaptation = await self.adapt_to_media(story_framework)
            
            # 4. 生成标准化的《故事创意框架》文档
            creative_document = await self.generate_creative_document(
                hotspots_analysis, story_framework, media_adaptation
            )
            
            result = {
                "hotspots_analysis": hotspots_analysis,
                "story_framework": story_framework,
                "media_adaptation": media_adaptation,
                "creative_document": creative_document
            }
            
            # 存储到缓存
            await redis_manager.store_agent_response("creative", request_hash, result)
            
            return result
