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
    
    language = data.get('language', 'python')
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    
    prompt = f"""Provide ONLY the {language} code that can be directly copied to LeetCode:

{problem_text}

RULES:
- Return ONLY the code without markdown, explanations, or formatting
- Use exact LeetCode function signature
- Ready to copy-paste into LeetCode editor

Provide ONLY the code:"""
    
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
                    "maxOutputTokens": 1000,
                    "temperature": 0.1,
                    "topP": 0.8
                }
            },
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
            # Clean up the response to remove markdown if present
            clean_code = ai_response.replace('```python', '').replace('```javascript', '').replace('```java', '').replace('```cpp', '').replace('```', '').strip()
            return jsonify({
                "solution": clean_code,
                "status": "success"
            })
        else:
            return jsonify({"error": f"API Error: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500