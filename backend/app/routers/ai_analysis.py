import os
import requests
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import radon.complexity as radon_complexity
import cProfile
import io
import pstats



OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_TOKEN = os.getenv("OPENROUTER_API_TOKEN")

headers = {
    "Authorization": f"Bearer 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"
}

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str

def query_openrouter(payload):
    response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{response.status_code}: {response.json()}"
        )
    
    response_json = response.json()
    
    # Extract the suggestion from the API response
    try:
        suggestion_content = response_json["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing response: {str(e)}"
        )
    
    return suggestion_content

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
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",  
        "messages": [
            {
                "role": "system", 
                "content": "Analyze this code and give me suggestions only without any other introductions or any ending notes, not even here are the suggestions or even here are your comments. Make sure there are multiple suggestions"
            },
            { 
                "role": "user", 
                "content": request.code
            }
        ]
    }
    result = query_openrouter(payload)
    return {"suggestions": result}

async def analyze_code_complexity(request: CodeAnalysisRequest):
    if request.language in language_support_map:
        complexity_function = language_support_map[request.language]["complexity_function"]
        return {"complexity_score": complexity_function(request.code)}
    else:
        return {"complexity_score": "Complexity analysis not supported for this language"}

async def generate_review_comments(request: CodeAnalysisRequest):
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",  
        "messages": [
            {
                "role": "system", 
                "content": "Analyze this code and give me comments only without any other introductions or any ending notes, not even here are the suggestions or here are your comments. Make sure there are multiple comments"
            },
            { 
                "role": "user", 
                "content": request.code
            }
        ]
    }
    result = query_openrouter(payload)
    return {"comments": result}
    
async def optimize_code(request: CodeAnalysisRequest):
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",  
        "messages": [
            {
                "role": "system", 
                "content": "Optimize this code only without any other introductions or any ending notes, not even here are the suggestions or here is your code"
            },
            { 
                "role": "user", 
                "content": request.code
            }
        ]
    }
    result = query_openrouter(payload)
    return {"optimized_code": result}

async def profile_code_performance(request: CodeAnalysisRequest):
    if request.language in language_support_map:
        profile_function = language_support_map[request.language]["profile_function"]
        return {"performance": profile_function(request.code)}
    else:
        return {"performance": "Profiling not supported for this language"}
