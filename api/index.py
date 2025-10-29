from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import re

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return jsonify({
        "name": "LeetCode AI Solver with Explanations",
        "endpoints": {
            "/solve": "POST - Solve with code + explanation",
            "/explain": "POST - Get detailed explanation only"
        },
        "languages": ["python", "javascript", "java", "cpp", "c", "csharp", "go", "rust", "kotlin", "swift", "php", "ruby", "scala", "typescript", "dart", "r", "matlab", "perl", "lua", "haskell", "clojure", "elixir", "fsharp", "vb"]
    })

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

def clean_code(text):
    text = re.sub(r'```\w*\n?', '', text)
    text = re.sub(r'```', '', text)
    return text.strip()

def call_gemini(prompt):
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        print("No API key found")
        return None
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and result["candidates"]:
                return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"API Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")
    
    return None

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    
    if not data or "problem" not in data:
        return jsonify({"error": "Problem required"}), 400
    
    problem = data['problem'].strip()
    language = data.get('language', 'python')
    
    if len(problem) < 3:
        return jsonify({"error": "Problem name too short"}), 400
    
    prompt = f"""
Solve the LeetCode problem "{problem}" in {language}.

Provide your response in this exact format:

APPROACH:
[Brief explanation of the solution strategy]

ALGORITHM:
1. [Step 1]
2. [Step 2]
3. [Step 3]

CODE:
[Clean, working code]

COMPLEXITY:
Time: O(...)
Space: O(...)

EXAMPLE:
[Walk through with sample input/output]
"""
    
    ai_response = call_gemini(prompt)
    if not ai_response:
        return jsonify({"error": "AI service unavailable"}), 503
    
    # Parse sections
    sections = {}
    current_section = None
    lines = ai_response.split('\n')
    
    for line in lines:
        line = line.strip()
        if line.upper().startswith(('APPROACH:', 'ALGORITHM:', 'CODE:', 'COMPLEXITY:', 'EXAMPLE:')):
            current_section = line.split(':')[0].upper()
            sections[current_section] = []
        elif current_section and line:
            sections[current_section].append(line)
    
    # Extract code
    code_lines = sections.get('CODE', [])
    solution = clean_code('\n'.join(code_lines)) if code_lines else ai_response
    
    # Extract algorithm steps
    algorithm_lines = sections.get('ALGORITHM', [])
    algorithm_steps = [line.lstrip('0123456789. ') for line in algorithm_lines if line.strip()]
    
    return jsonify({
        "solution": solution,
        "approach": '\n'.join(sections.get('APPROACH', [])) or "Optimized solution approach",
        "algorithm": algorithm_steps or ["Implementation details in code"],
        "complexity": '\n'.join(sections.get('COMPLEXITY', [])) or "Time and space complexity analysis",
        "example": '\n'.join(sections.get('EXAMPLE', [])) or "Example walkthrough provided",
        "language": language
    })

@app.route("/explain", methods=["POST"])
def explain():
    data = request.get_json()
    
    if not data or "problem" not in data:
        return jsonify({"error": "Problem required"}), 400
    
    problem = data['problem'].strip()
    
    prompt = f"""
Explain the LeetCode problem "{problem}" in detail:

1. PROBLEM BREAKDOWN: What the problem is asking
2. KEY INSIGHTS: Important observations to solve it
3. APPROACHES: Different ways to solve (brute force, optimal)
4. PATTERNS: What algorithmic patterns this uses
5. TIPS: How to approach similar problems

Find the problem by name and explain it. Make it educational and easy to understand.
"""
    
    ai_response = call_gemini(prompt)
    if not ai_response:
        return jsonify({"error": "Service unavailable"}), 503
    
    # Parse explanation sections
    sections = {}
    current_section = None
    lines = ai_response.split('\n')
    
    for line in lines:
        line = line.strip()
        if any(keyword in line.upper() for keyword in ['BREAKDOWN:', 'INSIGHTS:', 'APPROACHES:', 'PATTERNS:', 'TIPS:']):
            current_section = line.split(':')[0].upper()
            sections[current_section] = []
        elif current_section and line:
            sections[current_section].append(line)
    
    return jsonify({
        "breakdown": '\n'.join(sections.get('PROBLEM BREAKDOWN', sections.get('BREAKDOWN', []))),
        "insights": sections.get('KEY INSIGHTS', sections.get('INSIGHTS', [])),
        "approaches": sections.get('APPROACHES', []),
        "patterns": sections.get('PATTERNS', []),
        "tips": sections.get('TIPS', [])
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))