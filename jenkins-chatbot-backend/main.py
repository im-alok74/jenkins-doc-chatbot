from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jenkins_chatbot_backend.routers import chat, logs, plugins, docs
from jenkins_chatbot_backend.services.rag_service import RAGService
from jenkins_chatbot_backend.models.schemas import HealthResponse
import logging

app = FastAPI(title="Jenkins AI Chatbot Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response

app.include_router(chat.router)
app.include_router(logs.router)
app.include_router(plugins.router)
app.include_router(docs.router)

@app.get("/api/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", version="1.0.0")

@app.on_event("startup")
def startup_event():
    rag_service = RAGService()
    if not rag_service.index or not rag_service.documents:
        logging.info("FAISS index missing, please run scripts/index_docs.py to create index.")
