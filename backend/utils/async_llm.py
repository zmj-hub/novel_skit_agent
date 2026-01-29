import asyncio
from concurrent.futures import ThreadPoolExecutor
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain_community.llms import Tongyi
from core.config import settings
from typing import Optional, Dict, Any, List
from openai import OpenAI


class BaseLLM:
    def __init__(self):
        self.llm = None
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def generate(self, prompt: str, **kwargs) -> str:
        if not self.llm:
            raise ValueError("LLM not initialized.")
        
        print(f"Generating response for prompt: {prompt[:100]}...")
        print(f"Using LLM: {type(self.llm).__name__}")
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            self._sync_generate,
            prompt,
            kwargs
        )
        
        print(f"Generated result: {result[:100]}..." if result else "Generated empty result")
        return result
    
    def _sync_generate(self, prompt: str, kwargs: Dict[str, Any]) -> str:
        try:
            print(f"Calling llm.invoke with prompt length: {len(prompt)}")
            response = self.llm.invoke(prompt, **kwargs)
            print(f"Got response: {type(response)}")
            if hasattr(response, 'content'):
                print(f"Response content length: {len(response.content)}")
                return response.content
            else:
                print(f"Response has no content attribute: {response}")
                return str(response)
        except Exception as e:
            print(f"Error in _sync_generate: {e}")
            import traceback
            traceback.print_exc()
            return f"Error: {e}"
    
    async def generate_with_context(self, query: str, context: str) -> str:
        if not self.llm:
            raise ValueError("LLM not initialized.")
        
        prompt = f"""
        You are a helpful assistant. Answer the user's question based on the provided context.
        
        Context:
        {context}
        
        Question:
        {query}
        
        Answer:
        """
        
        return await self.generate(prompt)
    
    async def generate_with_history(self, query: str, history: List[Dict[str, str]]) -> str:
        if not self.llm:
            raise ValueError("LLM not initialized.")
        
        messages = []
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": query})
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            self._sync_generate_with_messages,
            messages
        )
        return result
    
    def _sync_generate_with_messages(self, messages: List[Dict[str, str]]) -> str:
        response = self.llm.invoke(messages)
        return response.content
    
    def close(self):
        self.executor.shutdown(wait=True)


class OpenAILLM(BaseLLM):
    def __init__(self, model: str = "gpt-3.5-turbo"):
        super().__init__()
        try:
            self.llm = ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=model,
                temperature=0.7
            )
        except Exception as e:
            # 允许在没有 API Key 的情况下初始化，只是在使用时会报错
            print(f"Warning: Failed to initialize OpenAI LLM: {e}")
            print("Application will start, but OpenAI features will be unavailable until OPENAI_API_KEY is configured")
            self.llm = None


class DeepSeekLLM(BaseLLM):
    def __init__(self, model: str = "deepseek-chat"):
        super().__init__()
        print(f"Initializing DeepSeekLLM with model: {model}")
        print(f"Using DeepSeek API Key: {settings.DEEPSEEK_API_KEY[:10]}..." if settings.DEEPSEEK_API_KEY else "No DeepSeek API Key provided")
        try:
            self.llm = ChatDeepSeek(
                api_key=settings.DEEPSEEK_API_KEY,
                model=model,
                temperature=0.7
            )
            print(f"Successfully initialized DeepSeekLLM with model: {model}")
        except Exception as e:
            # 允许在没有 API Key 的情况下初始化，只是在使用时会报错
            print(f"Warning: Failed to initialize DeepSeek LLM: {e}")
            print("Application will start, but DeepSeek features will be unavailable until DEEPSEEK_API_KEY is configured")
            self.llm = None


class QwenLLM(BaseLLM):
    def __init__(self, model: str = "qwen-plus"):
        super().__init__()
        print(f"Initializing QwenLLM with model: {model}")
        print(f"Using DashScope API Key: {settings.DASHSCOPE_API_KEY[:10]}..." if settings.DASHSCOPE_API_KEY else "No DashScope API Key provided")
        try:
            import os
            os.environ["DASHSCOPE_API_KEY"] = settings.DASHSCOPE_API_KEY
            self.llm = Tongyi(
                model=model,
                temperature=0.7
            )
            print(f"Successfully initialized QwenLLM with model: {model}")
        except Exception as e:
            # 允许在没有 API Key 的情况下初始化，只是在使用时会报错
            print(f"Warning: Failed to initialize Qwen LLM: {e}")
            print("Application will start, but Qwen features will be unavailable until DASHSCOPE_API_KEY is configured")
            self.llm = None


class ModelScopeLLM(BaseLLM):
    def __init__(self, model: str = "Qwen/Qwen3-30B-A3B-Instruct-2507"):
        super().__init__()
        print(f"Initializing ModelScopeLLM with model: {model}")
        print(f"Using ModelScope API Key: {settings.MODELSCOPE_API_KEY[:10]}..." if settings.MODELSCOPE_API_KEY else "No ModelScope API Key provided")
        try:
            self.model = model
            self.api_key = settings.MODELSCOPE_API_KEY
            self.base_url = settings.MODELSCOPE_BASE_URL
            self.llm = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
            )
            print(f"Successfully initialized ModelScopeLLM with model: {model}")
        except Exception as e:
            # 允许在没有 API Key 的情况下初始化，只是在使用时会报错
            print(f"Warning: Failed to initialize ModelScope LLM: {e}")
            print("Application will start, but ModelScope features will be unavailable until MODELSCOPE_API_KEY is configured")
            self.llm = None
    
    def _sync_generate(self, prompt: str, kwargs: Dict[str, Any]) -> str:
        if not self.llm:
            return f"Error: ModelScope LLM not initialized."
        
        if not self.api_key:
            return f"Error: ModelScope API Key not configured."
        
        try:
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a helpful assistant.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                stream=False
            )
            
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return f"Error: Invalid response from ModelScope API"
        except Exception as e:
            print(f"Error in ModelScope _sync_generate: {e}")
            import traceback
            traceback.print_exc()
            return f"Error: {e}"
    
    def _sync_generate_with_messages(self, messages: List[Dict[str, str]]) -> str:
        if not self.llm:
            return f"Error: ModelScope LLM not initialized."
        
        if not self.api_key:
            return f"Error: ModelScope API Key not configured."
        
        try:
            # 确保消息格式正确
            formatted_messages = []
            # 添加系统消息（如果没有）
            has_system = any(msg.get('role') == 'system' for msg in messages)
            if not has_system:
                formatted_messages.append({
                    'role': 'system',
                    'content': 'You are a helpful assistant.'
                })
            
            # 添加所有消息
            for msg in messages:
                formatted_messages.append({
                    'role': msg.get('role', 'user'),
                    'content': msg.get('content', '')
                })
            
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                stream=False
            )
            
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return f"Error: Invalid response from ModelScope API"
        except Exception as e:
            print(f"Error in ModelScope _sync_generate_with_messages: {e}")
            import traceback
            traceback.print_exc()
            return f"Error: {e}"


# class QwenMultimodalLLM(BaseLLM):
#     def __init__(self, model: str = "qwen-vl-plus"):
#         super().__init__()
#         print(f"Initializing QwenMultimodalLLM with model: {model}")
#         print(f"Using DashScope API Key: {settings.DASHSCOPE_API_KEY[:10]}..." if settings.DASHSCOPE_API_KEY else "No DashScope API Key provided")
#         try:
#             import os
#             os.environ["DASHSCOPE_API_KEY"] = settings.DASHSCOPE_API_KEY
#             # 注意：Tongyi 可能不支持多模态，需要单独处理
#             self.llm = Tongyi(
#                 model=model,
#                 temperature=0.7
#             )
#             print(f"Successfully initialized QwenMultimodalLLM with model: {model}")
#         except Exception as e:
#             # 允许在没有 API Key 的情况下初始化，只是在使用时会报错
#             print(f"Warning: Failed to initialize Qwen Multimodal LLM: {e}")
#             print("Application will start, but Qwen Multimodal features will be unavailable until DASHSCOPE_API_KEY is configured")
#             self.llm = None
#     
#     async def generate_with_image(self, prompt: str, image_url: str) -> str:
#         if not self.llm:
#             raise ValueError("LLM not initialized.")
#         
#         messages = [
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": prompt},
#                     {"type": "image", "image": image_url}
#                 ]
#             }
#         ]
#         
#         loop = asyncio.get_event_loop()
#         result = await loop.run_in_executor(
#             self.executor,
#             self._sync_generate_with_messages,
#             messages
#         )
#         return result


class LLMManager:
    def __init__(self):
        self.llm_instances = {}
    
    def get_llm(self, model: str) -> BaseLLM:
        # 检查模型是否有效，如果无效则使用默认模型
        if model not in settings.MODEL_PROVIDERS:
            print(f"Warning: Invalid model id: {model}, using default model instead")
            model = settings.DEFAULT_MODEL
        
        if model not in self.llm_instances:
            provider = settings.MODEL_PROVIDERS.get(model, "modelscope")
            if provider == "openai":
                self.llm_instances[model] = OpenAILLM(model)
            elif provider == "deepseek":
                self.llm_instances[model] = DeepSeekLLM(model)
            elif provider == "qwen" or provider == "qwen-multimodal":
                self.llm_instances[model] = QwenLLM(model)
            elif provider == "modelscope":
                self.llm_instances[model] = ModelScopeLLM(model)
            else:
                raise ValueError(f"Unknown provider for model {model}")
        return self.llm_instances[model]
    
    def get_default_llm(self) -> BaseLLM:
        return self.get_llm(settings.DEFAULT_MODEL)
    
    def close(self):
        for llm in self.llm_instances.values():
            llm.close()


llm_manager = LLMManager()
