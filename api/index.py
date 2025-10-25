from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return jsonify({"message": "Advanced LeetCode Solver API", "endpoint": "/solve"})

@app.route("/solve", methods=["POST"])
def solve_leetcode():
    data = request.get_json()
    if not data or "problem" not in data:
        return jsonify({"error": "Problem field required"}), 400
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    
    enhanced_prompt = f"""You are a world-class competitive programmer and LeetCode expert. Solve this problem with the BEST possible approach:

PROBLEM: {data['problem']}

Provide a complete solution with:

1. PROBLEM ANALYSIS:
   - Understand the problem requirements
   - Identify key constraints and edge cases
   - Determine the optimal approach

2. ALGORITHM EXPLANATION:
   - Explain the chosen algorithm/data structure
   - Why this approach is optimal
   - Step-by-step logic

3. COMPLETE PYTHON CODE:
   - Proper function signature (class Solution with method)
   - Clean, optimized implementation
   - Handle all edge cases
   - Add comments for clarity

4. COMPLEXITY ANALYSIS:
   - Time complexity with explanation
   - Space complexity with explanation

5. TEST CASES:
   - Multiple test cases with expected outputs
   - Include edge cases

IMPORTANT: 
- Write ACTUAL working code, not templates
- Use the most efficient algorithm possible
- Code should be ready to submit on LeetCode
- Be specific to this exact problem
- Provide multiple approaches if applicable (brute force vs optimal)"""
    
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": API_KEY,
            },
            json={
                "contents": [{
                    "parts": [{"text": enhanced_prompt}]
                }],
                "generationConfig": {
                    "maxOutputTokens": 3000,
                    "temperature": 0.2,
                    "topP": 0.8,
                    "topK": 40
                }
            },
            timeout=45
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

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "LeetCode Solver API"})