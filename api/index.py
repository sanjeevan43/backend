from flask import Flask, request, jsonify, render_template_string
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
        "usage": "Send LeetCode problems only. Other queries will be rejected.",
        "docs": "/docs"
    })

@app.route("/docs")
def swagger_ui():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>LeetCode Solver API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; }
        .endpoint { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .method { background: #007bff; color: white; padding: 5px 10px; border-radius: 3px; }
        .post { background: #28a745; }
        pre { background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        textarea { width: 100%; height: 100px; margin: 10px 0; }
        #result { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 LeetCode Solver API Documentation</h1>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> /</h3>
            <p>Get API information</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /solve</h3>
            <p>Solve LeetCode problems with complete Python solutions</p>
            
            <h4>Request Body:</h4>
            <pre>{
  "problem": "Your LeetCode problem description here"
}</pre>
            
            <h4>Try it out:</h4>
            <textarea id="problemInput" placeholder="Enter your LeetCode problem here...">Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.</textarea>
            <br>
            <button onclick="solveProblem()">Solve Problem</button>
            
            <div id="result"></div>
        </div>
    </div>
    
    <script>
        async function solveProblem() {
            const problem = document.getElementById('problemInput').value;
            const resultDiv = document.getElementById('result');
            
            if (!problem.trim()) {
                resultDiv.innerHTML = '<p style="color: red;">Please enter a problem description</p>';
                return;
            }
            
            resultDiv.innerHTML = '<p>Solving...</p>';
            
            try {
                const response = await fetch('/solve', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ problem: problem })
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    resultDiv.innerHTML = `<h4>Solution:</h4><pre>${data.solution}</pre>`;
                } else {
                    resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            }
        }
    </script>
</body>
</html>
    ''')

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

