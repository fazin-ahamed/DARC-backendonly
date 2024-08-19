from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .ai_analysis import analyze_code, analyze_code_complexity, generate_review_comments, optimize_code, profile_code_performance
from typing import Dict, List

routers = APIRouter()

class CodeRequest(BaseModel):
    code: str
    language: str

@routers.post("/api/analyze")
async def analyze_code_endpoint(request: CodeRequest):
    try:
        analysis_result = analyze_code(request.code, request.language)
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routers.post("/api/complexity")
async def analyze_code_complexity_endpoint(request: CodeRequest):
    try:
        complexity_result = analyze_code_complexity(request.code)
        return complexity_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routers.post("/api/review")
async def review_code_endpoint(request: CodeRequest):
    try:
        comments = generate_review_comments(request.code)
        return {"comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routers.post("/api/profile")
async def profile_code_endpoint(request: CodeRequest):
    try:
        profiling_result = profile_code_performance(request.code)
        return profiling_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routers.post("/api/optimize")
async def optimize_code_endpoint(request: CodeRequest):
    try:
        optimized_code = optimize_code(request.code, request.language)
        return {"optimized_code": optimized_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))