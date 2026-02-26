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

    # ============================================
    # 小说剧本创作新方法
    # ============================================

    async def write_chapter_script(self, chapter_context) -> Dict[str, Any]:
        """
        创作章节剧本 - 基于完整上下文创作剧本格式的章节
        
        这是小说剧本创作智能体的核心方法，接收完整的创作上下文，
        输出包含场景、对话、动作指示的剧本格式内容。
        
        Args:
            chapter_context: ChapterContext 对象，包含：
                - chapter_overview: 当前章节概述
                - character_memories: 人物记忆（加权）
                - previous_chapters_summary: 前文摘要
                - style_guide: 风格指南
                
        Returns:
            ChapterScript 对象的字典表示
        """
        from .models import ChapterScript, Scene
        
        chapter_number = chapter_context.chapter_number
        chapter_overview = chapter_context.chapter_overview
        character_memories = chapter_context.character_memories
        previous_summary = chapter_context.previous_chapters_summary
        style_guide = chapter_context.style_guide
        
        print(f"  [剧本创作] 开始创作第{chapter_number}章剧本...")
        
        # 构建人物记忆提示
        character_prompts = []
        for char_name, char_memory in character_memories.items():
            weighted = char_memory.get_weighted_memories(chapter_number)
            char_prompt = f"""
角色：{char_name}
核心特质：{weighted['core_traits']}
近期经历：{', '.join([e['event'] for e in weighted['recent_experiences']])}
重要过往：{', '.join([e['event'] for e in weighted['important_past']])}
关系网络：{weighted['relationships']}
"""
            character_prompts.append(char_prompt)
        
        # 构建前文摘要提示
        previous_prompt = ""
        if previous_summary:
            previous_prompt = "前文关键信息：\n" + "\n".join([f"- {s}" for s in previous_summary[-3:]])  # 最近3章
        
        # 构建风格指南提示
        style = style_guide.get("style", "urban")
        style_description = self.writing_styles.get(style, self.writing_styles["urban"])
        tone = style_guide.get("emotional_tone", "根据情节自然发展")
        
        # 主提示词
        prompt = f"""你是一位专业的小说剧本创作专家。请基于以下信息创作第{chapter_number}章的完整剧本：

【章节概述】
{chapter_overview}

【人物记忆与状态】
{chr(10).join(character_prompts)}

{previous_prompt}

【风格要求】
文风：{style_description}
情感基调：{tone}

【剧本格式要求】
请按照以下JSON格式输出剧本内容：

{{
    "chapter_title": "章节标题",
    "scenes": [
        {{
            "scene_id": "scene_1",
            "setting": "场景描述：时间、地点、环境氛围",
            "characters_present": ["角色A", "角色B"],
            "dialogues": [
                {{"speaker": "角色A", "content": "对话内容", "emotion": "情感状态", "action": "伴随动作"}},
                {{"speaker": "角色B", "content": "对话内容", "emotion": "情感状态", "action": "伴随动作"}}
            ],
            "actions": "场景中的动作指示和描写",
            "emotional_tone": "本场景的情感基调",
            "plot_progression": "本场景推动的情节发展点"
        }}
    ],
    "key_events": ["关键事件1", "关键事件2"],
    "character_development": {{"角色A": "本章节该角色的成长或变化", "角色B": "本章节该角色的成长或变化"}},
    "emotional_arc": "本章节的情感弧线描述"
}}

【创作要求】
1. 场景划分清晰，每个场景有明确的目的和情节推进
2. 对话符合角色性格和当前记忆状态
3. 动作指示具体，便于可视化呈现
4. 情感描写细腻，体现人物内心变化
5. 确保与人物记忆和前文信息保持一致
6. 章节结尾设置悬念或过渡，为下一章铺垫
7. 字数控制在1500-2500字之间

请直接输出JSON格式的剧本内容，确保格式正确可解析。"""

        try:
            # 调用LLM生成剧本
            script_content = await self.llm.generate(prompt)
            
            print(f"  [剧本创作] 收到LLM响应，长度: {len(script_content)}")
            
            # 尝试提取JSON - 清理markdown标记等
            import json
            import re
            
            # 清理响应，提取JSON部分
            json_match = re.search(r'(\{[\s\S]*\})', script_content)
            if json_match:
                script_content = json_match.group(1)
            
            # 移除可能的markdown代码块标记
            script_content = script_content.replace('```json', '').replace('```', '').strip()
            
            # 解析JSON响应
            script_data = json.loads(script_content)
            
            # 创建ChapterScript对象
            chapter_script = ChapterScript(
                chapter_number=chapter_number,
                chapter_title=script_data.get("chapter_title", f"第{chapter_number}章"),
                overview=chapter_overview
            )
            
            # 添加场景
            for scene_data in script_data.get("scenes", []):
                scene = Scene(
                    scene_id=scene_data.get("scene_id", f"scene_{len(chapter_script.scenes)+1}"),
                    setting=scene_data.get("setting", ""),
                    characters_present=scene_data.get("characters_present", []),
                    dialogues=scene_data.get("dialogues", []),
                    actions=scene_data.get("actions", ""),
                    emotional_tone=scene_data.get("emotional_tone", ""),
                    plot_progression=scene_data.get("plot_progression", "")
                )
                chapter_script.add_scene(scene)
            
            # 设置其他属性
            chapter_script.key_events = script_data.get("key_events", [])
            chapter_script.character_development = script_data.get("character_development", {})
            chapter_script.emotional_arc = script_data.get("emotional_arc", "")
            
            print(f"  [剧本创作] 第{chapter_number}章完成，共{len(chapter_script.scenes)}个场景，{chapter_script.word_count}字")
            
            return {
                "success": True,
                "chapter_script": chapter_script.to_dict(),
                "chapter_number": chapter_number
            }
            
        except Exception as e:
            print(f"  [剧本创作] 第{chapter_number}章创作失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "chapter_number": chapter_number
            }

    async def extract_chapter_key_info(self, chapter_script) -> Dict[str, Any]:
        """
        提取章节关键信息摘要
        
        用于传递给后续章节作为上下文
        
        Args:
            chapter_script: ChapterScript 对象
            
        Returns:
            关键信息摘要
        """
        chapter_number = chapter_script.chapter_number
        chapter_title = chapter_script.chapter_title
        key_events = chapter_script.key_events
        character_development = chapter_script.character_development
        
        # 构建摘要
        summary = f"第{chapter_number}章《{chapter_title}》："
        summary += f"关键事件：{', '.join(key_events)}；"
        summary += f"角色发展：{', '.join([f'{k}({v})' for k, v in character_development.items()])}"
        
        return {
            "chapter_number": chapter_number,
            "chapter_title": chapter_title,
            "summary": summary,
            "key_events": key_events,
            "character_development": character_development,
            "emotional_arc": chapter_script.emotional_arc
        }

    async def check_script_consistency(self, chapter_script, character_memories, previous_summaries) -> Dict[str, Any]:
        """
        检查剧本一致性
        
        检查剧本内容是否与人物记忆和前文信息保持一致
        
        Args:
            chapter_script: ChapterScript 对象
            character_memories: 人物记忆字典
            previous_summaries: 前文摘要列表
            
        Returns:
            一致性检查结果
        """
        issues = []
        warnings = []
        
        # 1. 检查角色行为一致性
        for char_name, development in chapter_script.character_development.items():
            if char_name in character_memories:
                char_memory = character_memories[char_name]
                core_traits = char_memory.long_term_memory.get("core_traits", "")
                
                # 简单检查：如果角色发展描述与核心特质完全无关，发出警告
                # 实际实现中可以使用LLM进行更复杂的语义分析
                if core_traits and len(development) > 10:
                    # 这里简化处理，实际应该调用LLM判断
                    pass
        
        # 2. 检查情节连贯性
        if previous_summaries:
            last_summary = previous_summaries[-1]
            # 检查本章关键事件是否与前文逻辑连贯
            # 简化处理，实际应该调用LLM判断
            pass
        
        # 3. 检查场景完整性
        for i, scene in enumerate(chapter_script.scenes):
            if not scene.dialogues and not scene.actions:
                issues.append(f"场景{i+1}缺少对话和动作")
            if not scene.characters_present:
                warnings.append(f"场景{i+1}未指定在场角色")
        
        is_consistent = len(issues) == 0
        
        return {
            "is_consistent": is_consistent,
            "issues": issues,
            "warnings": warnings,
            "chapter_number": chapter_script.chapter_number
        }

    async def update_character_memories_from_script(self, chapter_script, character_memories) -> Dict[str, Any]:
        """
        根据剧本内容更新人物记忆
        
        Args:
            chapter_script: ChapterScript 对象
            character_memories: 当前人物记忆字典
            
        Returns:
            更新后的人物记忆字典
        """
        chapter_number = chapter_script.chapter_number
        
        # 为每个在本章有发展的角色添加经历
        for char_name, development in chapter_script.character_development.items():
            if char_name in character_memories:
                char_memory = character_memories[char_name]
                
                # 添加本章经历
                event_description = f"第{chapter_number}章：{development}"
                
                # 判断影响程度（简化逻辑：根据描述长度和关键词）
                impact = "high" if any(kw in development for kw in ["重大", "转折", "决定", "改变"]) else "medium"
                
                char_memory.add_experience(event_description, chapter_number, impact)
                
                print(f"  [记忆更新] {char_name}：添加经历（{impact}影响）")
        
        # 检查场景中的角色互动，更新关系
        for scene in chapter_script.scenes:
            chars = scene.characters_present
            if len(chars) >= 2:
                # 简化处理：如果两个角色同时出现在场景中，认为他们有互动
                for i, char1 in enumerate(chars):
                    for char2 in chars[i+1:]:
                        if char1 in character_memories and char2 in character_memories:
                            # 更新双向关系（简化处理）
                            character_memories[char1].update_relationship(char2, "互动")
                            character_memories[char2].update_relationship(char1, "互动")
        
        return character_memories
