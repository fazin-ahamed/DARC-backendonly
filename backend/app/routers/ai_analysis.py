import os
import requests
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import radon.complexity as radon_complexity
import cProfile
import io
import pstats

router = APIRouter()

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Codestral-22B-v0.1"
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str

def query_huggingface(payload):
    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while connecting to Hugging Face API"
        )
    return response.json()

def analyze_python_complexity(code):
    complexity = radon_complexity.cc_visit(code)
    complexity_score = sum([c.complexity for c in complexity])
    return complexity_score

def profile_python_code(code):
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        exec(code)
    except Exception as e:
        return f"Error executing code: {e}"
    finally:
        profiler.disable()
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats()
    return s.getvalue()

language_support_map = {
    "python": {
        "complexity_function": analyze_python_complexity,
        "profile_function": profile_python_code,
    },
    "java": {
        "complexity_function": lambda code: "Complexity analysis not yet implemented for Java",
        "profile_function": lambda code: "Profiling not yet implemented for Java",
    },
    "javascript": {
        "complexity_function": lambda code: "Complexity analysis not yet implemented for JavaScript",
        "profile_function": lambda code: "Profiling not yet implemented for JavaScript",
    },
    "go": {
        "complexity_function": lambda code: "Complexity analysis not yet implemented for Go",
        "profile_function": lambda code: "Profiling not yet implemented for Go",
    },
    "ruby": {
        "complexity_function": lambda code: "Complexity analysis not yet implemented for Ruby",
        "profile_function": lambda code: "Profiling not yet implemented for Ruby",
    },
    "php": {
        "complexity_function": lambda code: "Complexity analysis not yet implemented for PHP",
        "profile_function": lambda code: "Profiling not yet implemented for PHP",
    },
    "csharp": {
        "complexity_function": lambda code: "Complexity analysis not yet implemented for C#",
        "profile_function": lambda code: "Profiling not yet implemented for C#",
    },
    "c": {
        "complexity_function": lambda code: "Complexity analysis not yet implemented for C",
        "profile_function": lambda code: "Profiling not yet implemented for C",
    },
    "cpp": {
        "complexity_function": lambda code: "Complexity analysis not yet implemented for C++",
        "profile_function": lambda code: "Profiling not yet implemented for C++",
    },
    "typescript": {
        "complexity_function": lambda code: "Complexity analysis not yet implemented for TypeScript",
        "profile_function": lambda code: "Profiling not yet implemented for TypeScript",
    }
}

async def analyze_code(request: CodeAnalysisRequest):
    payload = {"inputs": request.code, "language": request.language}
    result = query_huggingface(payload)
    return {"suggestions": result}

async def analyze_code_complexity(request: CodeAnalysisRequest):
    if request.language in language_support_map:
        complexity_function = language_support_map[request.language]["complexity_function"]
        return {"complexity_score": complexity_function(request.code)}
    else:
        return {"complexity_score": "Complexity analysis not supported for this language"}

async def generate_review_comments(request: CodeAnalysisRequest):
    payload = {"inputs": request.code, "language": request.language}
    result = query_huggingface(payload)
    return {"comments": result.get("comments", [])}

async def optimize_code(request: CodeAnalysisRequest):
    payload = {"inputs": request.code, "language": request.language}
    result = query_huggingface(payload)
    return {"optimized_code": result.get("optimized_code", "")}

async def profile_code_performance(request: CodeAnalysisRequest):
    if request.language in language_support_map:
        profile_function = language_support_map[request.language]["profile_function"]
        return {"performance": profile_function(request.code)}
    else:
        return {"performance": "Profiling not supported for this language"}
