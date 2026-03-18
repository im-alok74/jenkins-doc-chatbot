from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ChatContext(BaseModel):
    job_name: Optional[str] = None
    build_id: Optional[str] = None
    console_log: Optional[str] = None
    build_status: Optional[str] = None

class ConversationTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    query: str
    context: Optional[ChatContext] = None
    conversation_history: List[ConversationTurn]

class ChatResponse(BaseModel):
    response: str
    sources: List[str]
    confidence: float

class LogAnalysisRequest(BaseModel):
    console_log: str
    job_name: Optional[str] = None

class LogAnalysisResponse(BaseModel):
    error_type: str
    summary: str
    root_cause: str
    fix_suggestions: List[str]
    relevant_stage: str

class PluginRecommendation(BaseModel):
    name: str
    description: str
    install_command: str
    jenkinsfile_snippet: str

class PluginRecommendationResponse(BaseModel):
    plugins: List[PluginRecommendation]

class DocSearchResult(BaseModel):
    content: str
    source: str
    relevance_score: float

class DocSearchResponse(BaseModel):
    results: List[DocSearchResult]

class HealthResponse(BaseModel):
    status: str
    version: str
