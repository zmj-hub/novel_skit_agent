from rag.processor import processor
from typing import List, Dict, Any


class KnowledgeBaseRetriever:
    def __init__(self):
        try:
            self.vector_store = processor.get_vector_store()
        except ValueError:
            # 允许在没有 API Key 的情况下初始化，只是在使用时会报错
            print("Warning: Vector store not initialized. Knowledge base features will be unavailable until OPENAI_API_KEY is configured.")
            self.vector_store = None
    
    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Please configure OPENAI_API_KEY in .env file.")
        
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        retrieved_docs = []
        for doc, score in results:
            retrieved_docs.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            })
        
        return retrieved_docs
    
    def build_context(self, query: str, k: int = 5) -> str:
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Please configure OPENAI_API_KEY in .env file.")
        
        retrieved_docs = self.retrieve(query, k=k)
        
        context_parts = []
        for i, doc in enumerate(retrieved_docs):
            context_parts.append(f"Document {i+1}:\n{doc['content']}\n")
        
        context = "\n".join(context_parts)
        return context
    
    def get_document_count(self) -> int:
        if not self.vector_store:
            return 0
        
        if hasattr(self.vector_store, "get_collection"):
            collection = self.vector_store.get_collection()
            return collection.count()
        elif hasattr(self.vector_store, "index"):
            return len(self.vector_store.index)
        else:
            return 0
    
    def clear_knowledge_base(self):
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Please configure OPENAI_API_KEY in .env file.")
        
        processor.clear_vector_store()
        self.vector_store = processor.get_vector_store()


retriever = KnowledgeBaseRetriever()
