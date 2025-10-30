from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return jsonify({
        "message": "LeetCode Solver API", 
        "endpoint": "/solve",
        "docs": "/docs"
    })

@app.route("/docs")
def swagger_ui():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>LeetCode Solver</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; }
        .endpoint { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        textarea { width: 100%; height: 100px; margin: 10px 0; }
        #result { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 LeetCode Solver</h1>
        
        <div class="endpoint">
            <h3>Solve LeetCode Problem</h3>
            <textarea id="problemInput" placeholder="Enter LeetCode problem description...">Two Sum: Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.</textarea>
            <br>
            <button onclick="solveProblem()">Get Solution</button>
            <div id="result"></div>
        </div>
    </div>
    
    <script>
        async function solveProblem() {
            const problem = document.getElementById('problemInput').value;
            const resultDiv = document.getElementById('result');
            
            if (!problem.trim()) {
                resultDiv.innerHTML = '<p style="color: red;">Please enter a problem</p>';
                return;
            }
            
            resultDiv.innerHTML = '<p>Solving...</p>';
            
            try {
                const response = await fetch('/solve', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ problem: problem })
                });
                
                const data = await response.json();
                
                if (data.solution) {
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
        return jsonify({"error": "Problem required"}), 400
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        return jsonify({"error": "API not configured"}), 500
    
    prompt = f"""Solve this LeetCode problem. Give me ONLY working Python code that I can copy-paste into LeetCode.

PROBLEM: {data['problem']}

RULES:
- Give me ONLY the class Solution with working code
- Use correct method names (twoSum, maxSubArray, etc.)
- Make sure code actually works
- NO explanations, NO complexity analysis, NO examples
- Just clean working code

Format:
```python
class Solution:
    def correctMethodName(self, params):
        # working code
        return result
```"""
    
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": API_KEY,
            },
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "maxOutputTokens": 500,
                    "temperature": 0,
                    "topP": 0.9
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
            
            # Clean the response - remove markdown and extra text
            import re
            code_match = re.search(r'```python\n(.*?)\n```', ai_response, re.DOTALL)
            if code_match:
                clean_code = code_match.group(1)
            else:
                # If no code block found, try to extract class Solution
                lines = ai_response.split('\n')
                code_lines = []
                in_class = False
                for line in lines:
                    if 'class Solution' in line:
                        in_class = True
                    if in_class:
                        code_lines.append(line)
                clean_code = '\n'.join(code_lines) if code_lines else ai_response
            
            return jsonify({"solution": clean_code})
        else:
            return jsonify({"error": f"API Error: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500