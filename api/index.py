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
        "languages": ["python", "javascript", "java", "cpp"]
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
        return None
    
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            headers={"Content-Type": "application/json", "X-goog-api-key": API_KEY},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": 2500, "temperature": 0.2}
            },
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        pass
    return None

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    
    if not data or "problem" not in data:
        return jsonify({"error": "Problem required"}), 400
    
    problem = data['problem'].strip()
    language = data.get('language', 'python')
    
    if len(problem) < 5:
        return jsonify({"error": "Problem too short"}), 400
    
    # Enhanced prompt for complete solution with explanation
    prompt = f"""
Solve this LeetCode problem in {language}. Provide:

1. APPROACH: Brief explanation of the solution strategy
2. ALGORITHM: Step-by-step algorithm 
3. CODE: Clean, optimized code
4. COMPLEXITY: Time and space complexity
5. EXAMPLE: Walk through with sample input

Problem:
{problem}

Format your response clearly with these 5 sections.
"""
    
    ai_response = call_gemini(prompt)
    if not ai_response:
        return jsonify({"error": "Service unavailable"}), 503
    
    # Parse the response into sections
    sections = {}
    current_section = None
    lines = ai_response.split('\n')
    
    for line in lines:
        line = line.strip()
        if any(keyword in line.upper() for keyword in ['APPROACH:', 'ALGORITHM:', 'CODE:', 'COMPLEXITY:', 'EXAMPLE:']):
            current_section = line.split(':')[0].upper()
            sections[current_section] = []
        elif current_section and line:
            sections[current_section].append(line)
    
    # Extract and clean code
    code_section = sections.get('CODE', [])
    code = '\n'.join(code_section)
    clean_solution = clean_code(code)
    
    return jsonify({
        "solution": clean_solution,
        "approach": '\n'.join(sections.get('APPROACH', [])),
        "algorithm": sections.get('ALGORITHM', []),
        "complexity": '\n'.join(sections.get('COMPLEXITY', [])),
        "example": '\n'.join(sections.get('EXAMPLE', [])),
        "language": language
    })

@app.route("/explain", methods=["POST"])
def explain():
    data = request.get_json()
    
    if not data or "problem" not in data:
        return jsonify({"error": "Problem required"}), 400
    
    problem = data['problem'].strip()
    
    prompt = f"""
Explain this LeetCode problem in detail:

1. PROBLEM BREAKDOWN: What the problem is asking
2. KEY INSIGHTS: Important observations to solve it
3. APPROACHES: Different ways to solve (brute force, optimal)
4. PATTERNS: What algorithmic patterns this uses
5. TIPS: How to approach similar problems

Problem:
{problem}

Make it educational and easy to understand.
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