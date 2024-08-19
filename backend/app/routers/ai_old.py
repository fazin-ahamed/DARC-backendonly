from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re
from typing import Dict, List
import cProfile
import pstats
import io
import os

# Load the Hugging Face API token
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

# Load pre-trained Codestral-22B model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('codellama/CodeLlama-7b-hf')
model = AutoModelForCausalLM.from_pretrained('codellama/CodeLlama-7b-hf')

def preprocess_code(code: str) -> str:
    code = re.sub(r'#.*', '', code)  # Remove single-line comments
    code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)  # Remove multi-line comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Remove multi-line comments for languages like Java and C++
    code = re.sub(r'\s+', ' ', code)  # Replace multiple whitespace with a single space
    code = code.strip()
    return code

def analyze_code(code: str, language: str) -> Dict:
    code = preprocess_code(code)
    inputs = tokenizer(code, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=100)
    
    suggestions = interpret_predictions(outputs, language)
    return {"suggestions": suggestions}

def interpret_predictions(predictions, language):
    suggestion_map = {
        "python": {
            0: "Consider refactoring this function to reduce its complexity.",
            1: "Optimize this loop for better performance.",
            2: "Use list comprehensions for better readability.",
            3: "Avoid excessive nesting of control structures.",
            4: "Use f-strings for string formatting.",
            5: "Ensure proper use of exception handling.",
            6: "Refactor long functions into smaller units.",
            7: "Use built-in functions and libraries where possible.",
            8: "Avoid global variables.",
            9: "Use type hints for better code clarity.",
            10: "Check for redundant code or logic."
        },
        "java": {
            0: "Use StringBuilder instead of String for concatenation in loops.",
            1: "Avoid using raw types in collections.",
            2: "Use try-with-resources for better resource management.",
            3: "Consider using lambda expressions for anonymous classes.",
            4: "Use the diamond operator to simplify generics.",
            5: "Avoid using null values in collections.",
            6: "Use enums instead of constant variables.",
            7: "Prefer interfaces over abstract classes.",
            8: "Use Optional to avoid null checks.",
            9: "Avoid using synchronized blocks for performance."
        },
        "javascript": {
            0: "Use strict mode for better error checking.",
            1: "Use let/const instead of var for block-scoped variables.",
            2: "Avoid callback hell by using Promises or async/await.",
            3: "Use template literals for string concatenation.",
            4: "Prefer arrow functions for callbacks.",
            5: "Use the spread operator for array manipulation.",
            6: "Avoid global variables for better modularity.",
            7: "Use destructuring for cleaner code.",
            8: "Avoid using eval() for security reasons.",
            9: "Use default parameters to handle missing arguments."
        },
        "go": {
            0: "Use goroutines for concurrent tasks.",
            1: "Avoid using global variables for better concurrency.",
            2: "Use defer for resource cleanup.",
            3: "Check for errors immediately after function calls.",
            4: "Use channels for communication between goroutines.",
            5: "Prefer composition over inheritance.",
            6: "Use slices instead of arrays for dynamic data.",
            7: "Avoid using panic for error handling.",
            8: "Use the blank identifier to ignore return values.",
            9: "Ensure proper use of mutexes for shared resources."
        },
        "ruby": {
            0: "Use symbols instead of strings for keys in hashes.",
            1: "Avoid using global variables.",
            2: "Use blocks for resource management.",
            3: "Prefer single quotes for strings unless interpolation is needed.",
            4: "Use Enumerable methods for iterating over collections.",
            5: "Avoid using eval() for security reasons.",
            6: "Use rescue to handle exceptions properly.",
            7: "Use modules to organize related methods.",
            8: "Prefer using map over each for transformations.",
            9: "Use memoization for expensive computations."
        },
        "php": {
            0: "Use PDO for database interactions to prevent SQL injection.",
            1: "Avoid using short tags for better portability.",
            2: "Use strict comparisons to avoid type juggling issues.",
            3: "Prefer echo over print for better performance.",
            4: "Use namespaces to avoid class name conflicts.",
            5: "Avoid using the global keyword inside functions.",
            6: "Use prepared statements for database queries.",
            7: "Ensure proper error handling with try-catch blocks.",
            8: "Use the array functions for cleaner code.",
            9: "Avoid using extract() for better security."
        },
        "csharp": {
            0: "Use var for implicit typing where applicable.",
            1: "Avoid using dynamic unless necessary.",
            2: "Use LINQ for collection manipulation.",
            3: "Prefer async/await over Task.Result for asynchronous code.",
            4: "Use using statements for resource management.",
            5: "Avoid locking on publicly accessible objects.",
            6: "Use StringBuilder for string concatenation in loops.",
            7: "Prefer properties over public fields.",
            8: "Use null-coalescing operators for null checks.",
            9: "Avoid using exceptions for control flow."
        },
        "cpp": {
            0: "Prefer smart pointers over raw pointers.",
            1: "Use RAII for resource management.",
            2: "Avoid using macros where inline functions can be used.",
            3: "Use range-based for loops for better readability.",
            4: "Avoid using namespace std; in headers.",
            5: "Use const and constexpr where applicable.",
            6: "Ensure proper memory management to avoid leaks.",
            7: "Use the standard library containers over raw arrays.",
            8: "Avoid using C-style casts.",
            9: "Use the appropriate STL algorithm instead of manual loops."
        },
        "kotlin": {
            0: "Use val instead of var for immutable variables.",
            1: "Avoid using !! for null safety.",
            2: "Use data classes for models.",
            3: "Prefer sealed classes for restricted class hierarchies.",
            4: "Use extension functions for utility methods.",
            5: "Prefer nullable types over null checks.",
            6: "Use lambdas for higher-order functions.",
            7: "Use the Elvis operator for default values.",
            8: "Prefer using let for null-safe calls.",
            9: "Use coroutines for asynchronous tasks."
        },
        "swift": {
            0: "Use optionals instead of force unwrapping.",
            1: "Prefer structs over classes where possible.",
            2: "Use guard statements for early exits.",
            3: "Use extensions to organize related methods.",
            4: "Prefer using map over for loops for transformations.",
            5: "Use lazy properties for expensive initializations.",
            6: "Avoid using the force try! for error handling.",
            7: "Use protocols to define interfaces.",
            8: "Prefer immutable collections over mutable ones.",
            9: "Use defer to handle resource cleanup."
        },
        "typescript": {
            0: "Use interfaces to define object shapes.",
            1: "Prefer const over let for constant values.",
            2: "Avoid using the any type.",
            3: "Use async/await for handling promises.",
            4: "Ensure proper type checking with union types.",
            5: "Use readonly for immutable properties.",
            6: "Prefer type aliases for complex types.",
            7: "Use generics for reusable components.",
            8: "Avoid using the global scope.",
            9: "Use enum for related constants."
        }
    }
    
    language_suggestions = suggestion_map.get(language, {})
    suggestions = [language_suggestions.get(int(pred), "General advice") for pred in predictions]
    return suggestions

def analyze_code_complexity(code: str) -> Dict:
    complexity_score = len(re.findall(r'if|for|while|case|catch|try', code))  # Example complexity metric
    return {"complexity_score": complexity_score}

def generate_review_comments(code: str) -> List[str]:
    # Generate comments based on the model's output
    inputs = tokenizer(code, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_length=150
        )
    
    # Decode and split the generated text into lines
    comments = tokenizer.decode(outputs[0], skip_special_tokens=True).split('\n')
    return comments


def profile_code_performance(code: str) -> Dict:
    profile = cProfile.Profile()
    profile.enable()
    
    # Execute the code
    exec_globals = {}
    exec_locals = {}
    try:
        exec(code, exec_globals, exec_locals)
    except Exception as e:
        profile.disable()
        return {"error": str(e)}
    
    profile.disable()
    
    # Create a stream to hold profiling data
    stream = io.StringIO()
    stats = pstats.Stats(profile, stream=stream).sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    
    # Return the profiling data
    profiling_data = stream.getvalue()
    return {"profiling_data": profiling_data}

def optimize_code(code: str, language: str) -> str:
    # Use model to generate optimized code
    inputs = tokenizer(f"Optimize this code for {language}:\n{code}", return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=300)
    
    optimized_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return optimized_code
