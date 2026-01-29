from utils.async_llm import llm_manager
from core.config import settings
from typing import Dict, List, Any, Optional
import asyncio


class NovelWritingAgent:
    def __init__(self, model: str = None):
        self.model = model or settings.DEFAULT_MODEL
        self.llm = llm_manager.get_llm(self.model)
        self.writing_styles = {
            "sweet": "甜宠风格：语言温馨浪漫，情感细腻，情节轻松愉快，注重角色间的甜蜜互动和浪漫氛围。",
            "suspense": "悬疑风格：语言紧凑有力，情节跌宕起伏，注重悬念设置和逻辑推理，氛围紧张刺激。",
            "counterattack": "逆袭风格：语言充满力量感，情节从低谷到高峰，注重主角的成长和反击，充满爽感。",
            "urban": "都市风格：语言贴近现实，情节真实细腻，注重职场和生活细节，反映当代社会。",
            "fantasy": "奇幻风格：语言富有想象力，情节奇幻多变，注重世界观构建和魔法元素，充满冒险感。"
        }
    
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
        
        请以清晰、结构化的方式输出解析结果。
        """
        
        analysis = await self.llm.generate(prompt)
        return {
            "creative_framework": creative_framework,
            "parsed_content": analysis
        }
    
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
        
        adapted_content = await self.llm.generate(prompt)
        return {
            "original_content": content,
            "style": style,
            "style_description": style_description,
            "adapted_content": adapted_content
        }
    
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
        """
        
        character_arc = await self.llm.generate(prompt)
        return {
            "character_info": character_info,
            "character_arc": character_arc
        }
    
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
        """
        
        conflicts = await self.llm.generate(prompt)
        return {
            "story_context": story_context,
            "conflicts": conflicts
        }
    
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
        
        chapter_content = await self.llm.generate(prompt)
        return {
            "chapter_outline": chapter_outline,
            "style": style,
            "chapter_number": chapter_number,
            "chapter_content": chapter_content
        }
    
    async def evaluate_content_quality(self, content: str) -> Dict[str, Any]:
        """
        评估内容质量
        
        Args:
            content: 需要评估的内容
            
        Returns:
            质量评估结果，包含完读率影响因素和优化建议
        """
        prompt = f"""
        请评估以下小说内容的质量：
        
        内容：
        {content}
        
        评估要求：
        1. 分析完读率影响因素：情节吸引力、人物塑造、冲突设计、节奏控制等
        2. 评估文风一致性：语言风格、叙事节奏和情感渲染的一致性
        3. 检查悬念钩子的有效性：结尾悬念是否足够吸引人
        4. 提供具体的优化建议：如何提升内容质量和读者体验
        5. 给出整体评分（0-100分）
        """
        
        evaluation = await self.llm.generate(prompt)
        return {
            "content": content,
            "evaluation": evaluation
        }
    
    async def process_novel_request(self, creative_framework: str, style: str, chapter_count: int = 5) -> Dict[str, Any]:
        """
        处理完整的小说创作请求
        
        Args:
            creative_framework: 创意框架文档
            style: 文风类型
            chapter_count: 章节数量
            
        Returns:
            完整的小说创作结果，包含小说内容和质量评估
        """
        # 1. 解析创意框架
        parsed_framework = await self.parse_creative_framework(creative_framework)
        
        # 2. 适配文风
        adapted_content = await self.adapt_writing_style(parsed_framework['parsed_content'], style)
        
        # 3. 构建人物弧光
        # 这里简化处理，实际应该从解析结果中提取人物信息
        character_arc = await self.create_character_arc(adapted_content['adapted_content'])
        
        # 4. 设计冲突
        conflicts = await self.design_conflicts(adapted_content['adapted_content'])
        
        # 5. 撰写章节
        chapters = []
        for i in range(1, chapter_count + 1):
            chapter_outline = f"第{i}章：基于创意框架的章节内容"
            chapter = await self.write_chapter(chapter_outline, style, i)
            chapters.append(chapter)
        
        # 6. 评估内容质量
        full_novel = "\n\n".join([chapter['chapter_content'] for chapter in chapters])
        quality_evaluation = await self.evaluate_content_quality(full_novel)
        
        return {
            "parsed_framework": parsed_framework,
            "adapted_content": adapted_content,
            "character_arc": character_arc,
            "conflicts": conflicts,
            "chapters": chapters,
            "full_novel": full_novel,
            "quality_evaluation": quality_evaluation
        }
