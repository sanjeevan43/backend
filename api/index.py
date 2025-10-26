from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return jsonify({
        "message": "LeetCode AI Solver", 
        "endpoint": "/solve"
    })



@app.route("/solve", methods=["POST"])
def solve_leetcode():
    data = request.get_json()
    if not data or "problem" not in data:
        return jsonify({"error": "Problem field required"}), 400
    
    problem_text = data['problem'].strip()
    if len(problem_text) < 10:
        return jsonify({"error": "Please provide a more detailed problem description."}), 400
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    
    language = data.get('language', 'python')
    
    prompt = f"""You are an expert LeetCode problem solver. Provide a COMPLETE, WORKING {language} solution for this problem.

{problem_text}

REQUIREMENTS:
1. Provide COMPLETE, EXECUTABLE code that passes ALL test cases
2. Use proper LeetCode class format with correct method names
3. Handle ALL edge cases
4. Use optimal algorithms
5. Write production-ready code

Response format:
```{language}
class Solution:
    def methodName(self, params):
        # Complete working implementation
        return result
```

Time Complexity: O(...)
Space Complexity: O(...)

Explanation: [Step-by-step explanation]"""
    
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": API_KEY,
            },
            json={
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "maxOutputTokens": 2000,
                    "temperature": 0.1,
                    "topP": 0.8
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({
                "solution": ai_response,
                "problem": data['problem'],
                "status": "success"
            })
        else:
            return jsonify({"error": f"API Error: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500