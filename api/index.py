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
    
    enhanced_prompt = f"""You are an expert competitive programmer and LeetCode Grandmaster (rating 3000+). 
You ALWAYS write fully working, efficient, and clean code solutions.

Your job is to solve ANY LeetCode problem in Python. 
Follow these rules strictly:

1️⃣ Do NOT return template or placeholder code.  
   ❌ Never say things like:
      - "Analyze the problem requirements"
      - "Choose appropriate data structures"
      - "Your solution logic here"
      - "Implement step by step"
      - return []

2️⃣ Always provide the **real, complete solution** that compiles and passes all LeetCode test cases.

3️⃣ Follow this exact structure (no deviation):

---
Time complexity: O(...)
Space complexity: O(...)

```python
# Final working solution only
# Include all necessary imports/headers
class Solution:
    def methodName(self, params):
        # Complete working implementation
        pass
```

Explanation:
<Brief 2-3 sentence algorithm explanation>

Test cases:
- Input: [...] → Output: [...]
- Input: [...] → Output: [...]
---

4️⃣ Use the most optimal algorithm with lowest time complexity.

5️⃣ Code must be submission-ready for LeetCode.

SOLVE THIS PROBLEM:
{data['problem']}"""
    
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
                    "maxOutputTokens": 1500,
                    "temperature": 0,
                    "topP": 0.95,
                    "topK": 1
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