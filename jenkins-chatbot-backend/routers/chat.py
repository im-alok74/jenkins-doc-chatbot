from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from models.schemas import ChatRequest, ChatResponse
from services.llm_service import LLMService
from services.rag_service import RAGService
import logging

router = APIRouter()
llm_service = LLMService()
rag_service = RAGService()

@router.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: Request, chat_req: ChatRequest):
    try:
        context = chat_req.context.dict() if chat_req.context else {}
        history = [turn.dict() for turn in chat_req.conversation_history]
        rag_results = rag_service.search(chat_req.query, top_k=5)
        sources = [r["source"] for r in rag_results]
        llm_input_context = context.copy()
        if rag_results:
            llm_input_context["docs"] = "\n".join([r["content"] for r in rag_results])
        llm_resp = await llm_service.get_response(chat_req.query, llm_input_context, history)
        response = ChatResponse(
            response=llm_resp["response"],
            sources=sources,
            confidence=llm_resp["confidence"]
        )
        logging.info(f"Chat response: {response.response}")
        return response
    except Exception as e:
        logging.error(f"Chat endpoint error: {str(e)}")
        return JSONResponse(status_code=500, content={"response": "Internal server error.", "sources": [], "confidence": 0.0})
