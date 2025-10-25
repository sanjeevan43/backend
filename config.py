"""
Configuration settings for the LeetCode Solver API
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_API_ENDPOINT = os.getenv('GEMINI_API_ENDPOINT', 
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent')
    
    # Request Configuration
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
    MAX_OUTPUT_TOKENS = int(os.getenv('MAX_OUTPUT_TOKENS', '1500'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.1'))
    TOP_P = float(os.getenv('TOP_P', '0.8'))
    
    # Flask Configuration
    PORT = int(os.getenv('PORT', '5000'))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Problem Validation
    LEETCODE_KEYWORDS = os.getenv('LEETCODE_KEYWORDS', 
        'array,string,linked list,tree,graph,dynamic programming,binary search,sorting,hash table,stack,queue,heap,two pointers,sliding window,backtracking,greedy,dfs,bfs,leetcode,given,return,constraints,example,input,output,nums,target,solution,algorithm,complexity'
    ).split(',')
    
    # Language Formats
    PYTHON_FORMAT = os.getenv('PYTHON_FORMAT', 
        'class Solution:\n    def methodName(self, params):\n        # implementation\n        return result')
    JS_FORMAT = os.getenv('JS_FORMAT', 
        'function methodName(params) {\n    // implementation\n    return result;\n}')
    JAVA_FORMAT = os.getenv('JAVA_FORMAT', 
        'class Solution {\n    public returnType methodName(params) {\n        // implementation\n        return result;\n    }\n}')
    CPP_FORMAT = os.getenv('CPP_FORMAT', 
        'class Solution {\npublic:\n    returnType methodName(params) {\n        // implementation\n        return result;\n    }\n};')