from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from models.schemas import LogAnalysisRequest, LogAnalysisResponse
from services.log_analyzer import LogAnalyzer
import logging

router = APIRouter()
log_analyzer = LogAnalyzer()

@router.post("/api/logs/analyze", response_model=LogAnalysisResponse)
async def analyze_logs(request: Request, log_req: LogAnalysisRequest):
    try:
        result = log_analyzer.analyze(log_req.console_log)
        response = LogAnalysisResponse(**result)
        logging.info(f"Log analysis: {response.summary}")
        return response
    except Exception as e:
        logging.error(f"Log analysis error: {str(e)}")
        return JSONResponse(status_code=500, content={"error_type": "Internal error", "summary": "Internal server error.", "root_cause": "", "fix_suggestions": [], "relevant_stage": ""})
