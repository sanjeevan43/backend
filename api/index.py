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
    
    enhanced_prompt = f"""You are an expert competitive programmer and LeetCode problem solver. 
Your task is to solve ANY LeetCode problem completely and correctly in Python.

Follow these strict rules:

1. Always output a **complete, compiling, and correct solution** for the given function signature. 
   ❌ Never write placeholders like "Your solution logic here", "TODO", or "Implement step by step".

2. Structure your response EXACTLY as follows:
   ---
   Time complexity: O(...)
   Space complexity: O(...)

   ```python
   # Final working solution only
   # Include all required imports/headers
   class Solution:
       def methodName(self, params):
           # Complete implementation here
           return result
   ```

   Explanation:
   <Explain your algorithm in 2-6 clear sentences.>

   Testcases:
   1. input: <example input> -> expected: <expected output>
   2. input: <edge case> -> expected: <expected output>
   3. input: <large or boundary case> -> expected: <expected output>
   ---

3. Use **the most efficient algorithm** possible within given constraints.

4. If multiple solutions exist, choose the one with **lowest time complexity**.
   (If equal, prefer simpler code.)

5. Include necessary headers/imports and ensure the code **compiles and runs**.

6. Use **only standard libraries** unless otherwise allowed.

7. If the problem is ambiguous, state one clear assumption and continue.

8. No extra commentary, no markdown outside the shown structure, and no private reasoning steps.

Now, solve the following LeetCode problem in Python:
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
                    "maxOutputTokens": 2000,
                    "temperature": 0,
                    "topP": 1,
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