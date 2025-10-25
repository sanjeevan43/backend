from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Import C++ solver
from cpp import solve_cpp_leetcode
app.add_url_rule('/cpp', 'solve_cpp_leetcode', solve_cpp_leetcode, methods=['POST'])

@app.route("/")
def root():
    return jsonify({
        "message": "Advanced LeetCode Solver API", 
        "endpoints": {
            "/solve": "Multi-language solver (Python/C++/Java)",
            "/cpp": "Specialized C++ solver"
        }
    })

@app.route("/solve", methods=["POST"])
def solve_leetcode():
    data = request.get_json()
    if not data or "problem" not in data:
        return jsonify({"error": "Problem field required"}), 400
    
    language = data.get("language", "python").lower()
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    
    enhanced_prompt = f"""I am giving you a LeetCode problem. You MUST solve it completely with working code.

RULES:
❌ NO templates, NO placeholders, NO "TODO", NO "implement here"
✅ ONLY complete working solutions that pass all test cases
✅ Write the ACTUAL algorithm implementation
✅ Use optimal time/space complexity

FORMAT (follow exactly):

Time: O(...)
Space: O(...)

```python
class Solution:
    def functionName(self, params):
        # Write the complete working solution here
        # This must be the actual algorithm, not a template
        return actual_result
```

Algorithm: [Brief explanation]

EXAMPLE:
If problem is "Two Sum", you write:
```python
class Solution:
    def twoSum(self, nums, target):
        seen = {{}}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []
```

Now solve this problem with COMPLETE working code:

PROBLEM: {data['problem']}

Write the complete solution now (no explanations first, just solve it):"""
    
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
                    "maxOutputTokens": 2000,
                    "temperature": 0.1,
                    "topP": 0.9,
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
                "language": language,
                "status": "success"
            })
        else:
            return jsonify({"error": f"API Error: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "LeetCode Solver API"})