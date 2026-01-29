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


class StoryScriptAgent:
    def __init__(self, model: str = None):
        self.model = model or model_version_manager.get_model_name("story_script")
        self.llm = llm_manager.get_llm(self.model)
        self.writing_styles = {
            "sweet": "甜宠风格：语言温馨浪漫，情感细腻，情节轻松愉快，注重角色间的甜蜜互动和浪漫氛围。",
            "suspense": "悬疑风格：语言紧凑有力，情节跌宕起伏，注重悬念设置和逻辑推理，氛围紧张刺激。",
            "counterattack": "逆袭风格：语言充满力量感，情节从低谷到高峰，注重主角的成长和反击，充满爽感。",
            "urban": "都市风格：语言贴近现实，情节真实细腻，注重职场和生活细节，反映当代社会。",
            "fantasy": "奇幻风格：语言富有想象力，情节奇幻多变，注重世界观构建和魔法元素，充满冒险感。"
        }
        self.script_formats = {
            "screenplay": "电影剧本格式：包含场景标题、动作描述、对话和镜头指示。",
            "stage_play": "舞台剧剧本格式：包含场景设置、角色对话、舞台指示和灯光音效说明。",
            "short_play": "短剧剧本格式：节奏紧凑，每30秒设置1个小冲突，每3-5分钟设置1个大反转。"
        }
    
    @monitor_execution_time("story_script")
    @retry(max_retries=3, agent_type="story_script")
    async def parse_creative_framework(self, creative_framework: str) -> Dict[str, Any]:
        """
        解析创意策划智能体提供的创意框架
        
        Args:
            creative_framework: 创意框架文档
            
        Returns:
            解析结果，包含人物设定、剧情大纲和核心反转节点
        """
        prompt = f"""
        请解析以下创意框架文档，提取关键信息并整理为结构化数据：
        
        创意框架：
        {creative_framework}
        
        请提取以下内容：
        1. 人物小传：主要角色的背景故事、性格特征、目标动机和人物弧光
        2. 剧情大纲：小说章回结构和短剧集数结构
        3. 核心反转节点：关键转折点的位置、内容和情感冲击力评估
        4. 适合的媒介形式：小说、剧本、短剧等
        
        请以清晰、结构化的方式输出解析结果。
        """
        
        try:
            analysis = await self.llm.generate(prompt)
            return {
                "creative_framework": creative_framework,
                "parsed_content": analysis
            }
        except Exception as e:
            raise ModelError(f"解析创意框架失败: {e}")
    
    @monitor_execution_time("story_script")
    @retry(max_retries=3, agent_type="story_script")
    async def adapt_writing_style(self, content: str, style: str) -> Dict[str, Any]:
        """
        适配不同题材的文风
        
        Args:
            content: 需要适配的内容
            style: 文风类型（sweet, suspense, counterattack, urban, fantasy）
            
        Returns:
            适配结果，包含适配后的内容和文风说明
        """
        style_description = self.writing_styles.get(style, self.writing_styles["urban"])
        
        prompt = f"""
        请将以下内容适配为{style_description}：
        
        原始内容：
        {content}
        
        适配要求：
        1. 保持内容的核心信息不变
        2. 调整语言风格、叙事节奏和情感渲染方式
        3. 确保适配后的内容符合该风格的特点
        4. 保持内容的连贯性和逻辑性
        """
        
        try:
            adapted_content = await self.llm.generate(prompt)
            return {
                "original_content": content,
                "style": style,
                "style_description": style_description,
                "adapted_content": adapted_content
            }
        except Exception as e:
            raise ModelError(f"适配文风失败: {e}")
    
    @monitor_execution_time("story_script")
    @retry(max_retries=3, agent_type="story_script")
    async def create_character_arc(self, character_info: str) -> Dict[str, Any]:
        """
        构建人物弧光
        
        Args:
            character_info: 人物信息
            
        Returns:
            人物弧光，包含角色成长曲线和关键转折点
        """
        prompt = f"""
        请基于以下人物信息，构建完整的人物弧光：
        
        人物信息：
        {character_info}
        
        构建要求：
        1. 设计符合逻辑的角色成长曲线
        2. 明确人物的起点、发展和终点状态
        3. 识别关键转折点和成长机会
        4. 确保人物弧光与整体故事主题一致
        5. 提供具体的场景和事件来展现人物的成长
        6. 分析角色在剧本中的表现潜力
        """
        
        try:
            character_arc = await self.llm.generate(prompt)
            return {
                "character_info": character_info,
                "character_arc": character_arc
            }
        except Exception as e:
            raise ModelError(f"构建人物弧光失败: {e}")
    
    @monitor_execution_time("story_script")
    @retry(max_retries=3, agent_type="story_script")
    async def design_conflicts(self, story_context: str) -> Dict[str, Any]:
        """
        设计冲突细节
        
        Args:
            story_context: 故事背景
            
        Returns:
            冲突设计，包含外部冲突和内部冲突
        """
        prompt = f"""
        请基于以下故事背景，设计详细的冲突细节：
        
        故事背景：
        {story_context}
        
        设计要求：
        1. 设计外部冲突：角色与环境、其他角色的冲突
        2. 设计内部冲突：角色内心的挣扎和矛盾
        3. 确保冲突符合故事逻辑和人物性格
        4. 提供具体的冲突场景和解决方式
        5. 强化冲突的细节描写，提升读者沉浸感
        6. 分析冲突在剧本中的表现潜力
        """
        
        try:
            conflicts = await self.llm.generate(prompt)
            return {
                "story_context": story_context,
                "conflicts": conflicts
            }
        except Exception as e:
            raise ModelError(f"设计冲突失败: {e}")
    
    @monitor_execution_time("story_script")
    @retry(max_retries=3, agent_type="story_script")
    async def write_chapter(self, chapter_outline: str, style: str, chapter_number: int) -> Dict[str, Any]:
        """
        撰写小说章节
        
        Args:
            chapter_outline: 章节大纲
            style: 文风类型
            chapter_number: 章节编号
            
        Returns:
            章节内容，包含正文和悬念钩子
        """
        style_description = self.writing_styles.get(style, self.writing_styles["urban"])
        
        prompt = f"""
        请基于以下章节大纲，撰写一篇{style_description}的小说章节：
        
        章节大纲：
        {chapter_outline}
        
        章节编号：第{chapter_number}章
        
        撰写要求：
        1. 采用章回体结构，章节标题要吸引人
        2. 语言风格符合选定的文风
        3. 叙事节奏紧凑，情感渲染强烈
        4. 强化冲突细节描写，提升读者沉浸感
        5. 每章结尾必须包含悬念式钩子设计，激发读者持续阅读兴趣
        6. 章节字数控制在1000-2000字之间
        """
        
        try:
            chapter_content = await self.llm.generate(prompt)
            return {
                "chapter_outline": chapter_outline,
                "style": style,
                "chapter_number": chapter_number,
                "chapter_content": chapter_content
            }
        except Exception as e:
            raise ModelError(f"撰写章节失败: {e}")
    
    @monitor_execution_time("story_script")
    @retry(max_retries=3, agent_type="story_script")
    async def write_script_scene(self, scene_outline: str, script_format: str, style: str) -> Dict[str, Any]:
        """
        撰写剧本场景
        
        Args:
            scene_outline: 场景大纲
            script_format: 剧本格式
            style: 文风类型
            
        Returns:
            场景内容，包含剧本格式的场景描述和对话
        """
        format_description = self.script_formats.get(script_format, self.script_formats["screenplay"])
        style_description = self.writing_styles.get(style, self.writing_styles["urban"])
        
        prompt = f"""
        请基于以下场景大纲，撰写一个{format_description}的剧本场景：
        
        场景大纲：
        {scene_outline}
        
        文风要求：{style_description}
        
        撰写要求：
        1. 严格按照指定的剧本格式撰写
        2. 包含详细的场景描述、角色对话和舞台/镜头指示
        3. 语言风格符合选定的文风
        4. 对话自然流畅，符合角色性格
        5. 场景节奏紧凑，冲突明确
        6. 适合影视/舞台表现
        """
        
        try:
            scene_content = await self.llm.generate(prompt)
            return {
                "scene_outline": scene_outline,
                "script_format": script_format,
                "style": style,
                "scene_content": scene_content
            }
        except Exception as e:
            raise ModelError(f"撰写剧本场景失败: {e}")
    
    @monitor_execution_time("story_script")
    @retry(max_retries=3, agent_type="story_script")
    async def adapt_to_medium(self, content: str, medium_type: str) -> Dict[str, Any]:
        """
        适配不同媒介形式
        
        Args:
            content: 需要适配的内容
            medium_type: 媒介类型（novel, screenplay, stage_play, short_play）
            
        Returns:
            适配结果，包含适配后的内容和媒介说明
        """
        prompt = f"""
        请将以下内容适配为{medium_type}形式：
        
        原始内容：
        {content}
        
        适配要求：
        1. 保持内容的核心信息不变
        2. 调整格式以符合选定媒介的要求
        3. 小说：注重细节描写和心理刻画
        4. 剧本：添加场景描述、对话和镜头指示
        5. 短剧：节奏紧凑，增加冲突和反转
        6. 确保适配后的内容符合媒介的表现特点
        """
        
        try:
            adapted_content = await self.llm.generate(prompt)
            return {
                "original_content": content,
                "medium_type": medium_type,
                "adapted_content": adapted_content
            }
        except Exception as e:
            raise ModelError(f"适配媒介形式失败: {e}")
    
    @monitor_execution_time("story_script")
    @retry(max_retries=3, agent_type="story_script")
    async def evaluate_content_quality(self, content: str, medium_type: str = "novel") -> Dict[str, Any]:
        """
        评估内容质量
        
        Args:
            content: 需要评估的内容
            medium_type: 媒介类型
            
        Returns:
            质量评估结果，包含完读率影响因素和优化建议
        """
        prompt = f"""
        请评估以下{medium_type}内容的质量：
        
        内容：
        {content}
        
        评估要求：
        1. 分析完读率影响因素：情节吸引力、人物塑造、冲突设计、节奏控制等
        2. 评估文风一致性：语言风格、叙事节奏和情感渲染的一致性
        3. 检查悬念钩子的有效性：结尾悬念是否足够吸引人
        4. 提供具体的优化建议：如何提升内容质量和读者体验
        5. 给出整体评分（0-100分）
        6. 评估内容在选定媒介中的表现效果
        """
        
        try:
            evaluation = await self.llm.generate(prompt)
            return {
                "content": content,
                "medium_type": medium_type,
                "evaluation": evaluation
            }
        except Exception as e:
            raise ModelError(f"评估内容质量失败: {e}")
    
    def _generate_request_hash(self, creative_framework: str, style: str, medium_type: str, chapter_count: int) -> str:
        """
        生成请求哈希值
        
        Args:
            creative_framework: 创意框架文档
            style: 文风类型
            medium_type: 媒介类型
            chapter_count: 章节数量
            
        Returns:
            请求哈希值
        """
        # 使用创意框架的前1000个字符和其他参数生成哈希
        framework_snippet = creative_framework[:1000] if len(creative_framework) > 1000 else creative_framework
        request_data = {
            "framework_snippet": framework_snippet,
            "style": style,
            "medium_type": medium_type,
            "chapter_count": chapter_count
        }
        return hashlib.md5(json.dumps(request_data, sort_keys=True).encode()).hexdigest()
    
    @monitor_execution_time("story_script")
    async def process_story_request(self, creative_framework: str, style: str, medium_type: str = "novel", chapter_count: int = 5) -> Dict[str, Any]:
        """
        处理完整的故事创作请求
        
        Args:
            creative_framework: 创意框架文档
            style: 文风类型
            medium_type: 媒介类型
            chapter_count: 章节数量
            
        Returns:
            完整的故事创作结果，包含故事内容和质量评估
        """
        # 生成请求哈希
        request_hash = self._generate_request_hash(creative_framework, style, medium_type, chapter_count)
        
        # 检查缓存
        cached_response = await redis_manager.get_agent_response("story_script", request_hash)
        if cached_response:
            return cached_response
        
        async with ErrorContext(agent_type="story_script", operation="process_story_request"):
            # 1. 解析创意框架
            parsed_framework = await self.parse_creative_framework(creative_framework)
            
            # 2. 适配文风
            adapted_content = await self.adapt_writing_style(parsed_framework['parsed_content'], style)
            
            # 3. 构建人物弧光
            character_arc = await self.create_character_arc(adapted_content['adapted_content'])
            
            # 4. 设计冲突
            conflicts = await self.design_conflicts(adapted_content['adapted_content'])
            
            # 5. 根据媒介类型生成内容
            if medium_type == "novel":
                # 撰写小说章节
                chapters = []
                for i in range(1, chapter_count + 1):
                    chapter_outline = f"第{i}章：基于创意框架的章节内容"
                    chapter = await self.write_chapter(chapter_outline, style, i)
                    chapters.append(chapter)
                
                full_story = "\n\n".join([chapter['chapter_content'] for chapter in chapters])
            else:
                # 撰写剧本场景
                scenes = []
                for i in range(1, chapter_count + 1):
                    scene_outline = f"场景{i}：基于创意框架的场景内容"
                    scene = await self.write_script_scene(scene_outline, medium_type, style)
                    scenes.append(scene)
                
                full_story = "\n\n".join([scene['scene_content'] for scene in scenes])
            
            # 6. 评估内容质量
            quality_evaluation = await self.evaluate_content_quality(full_story, medium_type)
            
            result = {
                "parsed_framework": parsed_framework,
                "adapted_content": adapted_content,
                "character_arc": character_arc,
                "conflicts": conflicts,
                "chapters" if medium_type == "novel" else "scenes": chapters if medium_type == "novel" else scenes,
                "full_story": full_story,
                "medium_type": medium_type,
                "quality_evaluation": quality_evaluation
            }
            
            # 存储到缓存
            await redis_manager.store_agent_response("story_script", request_hash, result)
            
            return result
