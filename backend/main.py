from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 导入API路由
from api.monitoring import router as monitoring_router
from api.chat import router as chat_router
from api.collaboration import router as collaboration_router
from api.creative import router as creative_router
from api.example import router as example_router
from api.knowledge import router as knowledge_router
from api.novel import router as novel_router
from api.scheduler import router as scheduler_router
from api.upload import router as upload_router

# 创建FastAPI应用实例
app = FastAPI(
    title="Novel Skit Agent API",
    description="智能小说创作多智能体系统API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(monitoring_router, prefix="/api/monitoring", tags=["monitoring"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(collaboration_router, prefix="/api/collaboration", tags=["collaboration"])
app.include_router(creative_router, prefix="/api/creative", tags=["creative"])
app.include_router(example_router, prefix="/api/example", tags=["example"])
app.include_router(knowledge_router, prefix="/api/knowledge", tags=["knowledge"])
app.include_router(novel_router, prefix="/api/novel", tags=["novel"])
app.include_router(scheduler_router, prefix="/api", tags=["scheduler"])
app.include_router(upload_router, prefix="/api/upload", tags=["upload"])

# 根路径
@app.get("/")
def read_root():
    return {
        "message": "Novel Skit Agent API",
        "version": "1.0.0",
        "status": "running"
    }

# 健康检查端点
@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
