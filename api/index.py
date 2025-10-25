from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return jsonify({
        "message": "LeetCode Problems Only - Coding Challenge Solver API", 
        "endpoint": "/solve",
        "usage": "Send LeetCode problems only. Other queries will be rejected."
    })

@app.route("/solve", methods=["POST"])
def solve_leetcode():
    data = request.get_json()
    if not data or "problem" not in data:
        return jsonify({"error": "Problem field required"}), 400
    
    # Validate it's a LeetCode problem
    problem_text = data['problem'].lower()
    leetcode_keywords = ['array', 'string', 'linked list', 'tree', 'graph', 'dynamic programming', 
                        'binary search', 'sorting', 'hash table', 'stack', 'queue', 'heap', 
                        'two pointers', 'sliding window', 'backtracking', 'greedy', 'dfs', 'bfs',
                        'leetcode', 'given', 'return', 'constraints', 'example', 'input', 'output']
    
    if not any(keyword in problem_text for keyword in leetcode_keywords):
        return jsonify({"error": "This API only solves LeetCode coding problems. Please provide a valid LeetCode problem."}), 400
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    
    prompt = f"""You are a LeetCode expert. Solve ONLY this specific LeetCode problem with complete working code:

{data['problem']}

RULES:
- ONLY solve LeetCode algorithmic problems
- Provide complete working Python solution
- Use proper LeetCode class Solution format
- No templates or placeholders

Format:
Time: O(...)
Space: O(...)

```python
class Solution:
    def methodName(self, params):
        # Complete working implementation
        return result
```

Explanation: [brief algorithm description]"""
    
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
                    "maxOutputTokens": 1500,
                    "temperature": 0.1,
                    "topP": 0.9
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

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})