from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma, FAISS
from core.config import settings
from typing import List, Optional
import os


class DocumentProcessor:
    def __init__(self):
        try:
            self.embeddings = OpenAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
                api_key=settings.OPENAI_API_KEY
            )
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            self.vector_store = self._init_vector_store()
        except Exception as e:
            # 允许在没有 API Key 的情况下初始化，只是在使用时会报错
            print(f"Warning: Failed to initialize embeddings: {e}")
            print("Application will start, but LLM features will be unavailable until OPENAI_API_KEY is configured")
            self.embeddings = None
            self.text_splitter = None
            self.vector_store = None
    
    def _init_vector_store(self):
        if settings.VECTOR_STORE_TYPE == "chromadb":
            return Chroma(
                persist_directory=settings.VECTOR_STORE_PATH,
                embedding_function=self.embeddings
            )
        elif settings.VECTOR_STORE_TYPE == "faiss":
            return FAISS(
                embedding_function=self.embeddings
            )
        else:
            raise ValueError(f"Unsupported vector store type: {settings.VECTOR_STORE_TYPE}")
    
    def load_document(self, file_path: str) -> List:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext in [".txt", ".md"]:
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        documents = loader.load()
        return documents
    
    def process_document(self, file_path: str) -> int:
        if not self.embeddings or not self.text_splitter or not self.vector_store:
            raise ValueError("Embeddings not initialized. Please configure OPENAI_API_KEY in .env file.")
        
        documents = self.load_document(file_path)
        chunks = self.text_splitter.split_documents(documents)
        
        if settings.VECTOR_STORE_TYPE == "chromadb":
            self.vector_store.add_documents(chunks)
            self.vector_store.persist()
        elif settings.VECTOR_STORE_TYPE == "faiss":
            self.vector_store.add_documents(chunks)
            self.vector_store.save_local(settings.VECTOR_STORE_PATH)
        
        return len(chunks)
    
    def get_vector_store(self):
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Please configure OPENAI_API_KEY in .env file.")
        return self.vector_store
    
    def clear_vector_store(self):
        if not self.embeddings:
            raise ValueError("Embeddings not initialized. Please configure OPENAI_API_KEY in .env file.")
        
        if settings.VECTOR_STORE_TYPE == "chromadb":
            import shutil
            if os.path.exists(settings.VECTOR_STORE_PATH):
                shutil.rmtree(settings.VECTOR_STORE_PATH)
            os.makedirs(settings.VECTOR_STORE_PATH, exist_ok=True)
            self.vector_store = self._init_vector_store()
        elif settings.VECTOR_STORE_TYPE == "faiss":
            if os.path.exists(settings.VECTOR_STORE_PATH):
                import shutil
                shutil.rmtree(settings.VECTOR_STORE_PATH)
            self.vector_store = self._init_vector_store()


processor = DocumentProcessor()
