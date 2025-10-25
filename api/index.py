from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return jsonify({"message": "LeetCode Solver API", "endpoint": "/solve"})

@app.route("/solve", methods=["POST"])
def solve_leetcode():
    data = request.get_json()
    if not data or "problem" not in data:
        return jsonify({"error": "Problem field required"}), 400
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": API_KEY,
            },
            json={
                "contents": [{
                    "parts": [{"text": f"You are an expert LeetCode problem solver. For the given problem, provide a complete working solution with:

1. Problem understanding and approach
2. Complete Python code solution (not template)
3. Time and space complexity analysis
4. Example walkthrough

IMPORTANT: Provide actual working code, not templates or placeholders. Solve the specific problem completely.

Problem: {data['problem']}"}]
                }],
                "generationConfig": {"maxOutputTokens": 2000, "temperature": 0.1}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"response": ai_response})
        else:
            return jsonify({"error": f"API Error: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500