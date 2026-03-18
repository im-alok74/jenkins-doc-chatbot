from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from jenkins_chatbot_backend.models.schemas import DocSearchResponse
from jenkins_chatbot_backend.services.rag_service import RAGService
import logging

router = APIRouter()
rag_service = RAGService()

@router.get("/api/docs/search", response_model=DocSearchResponse)
async def docs_search(request: Request, query: str = Query(...)):
    try:
        results = rag_service.search(query, top_k=5)
        response = DocSearchResponse(results=results)
        logging.info(f"Docs search for '{query}': {len(results)} results")
        return response
    except Exception as e:
        logging.error(f"Docs search error: {str(e)}")
        return JSONResponse(status_code=500, content={"results": []})
