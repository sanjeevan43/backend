from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/cpp", methods=["POST"])
def solve_cpp_leetcode():
    data = request.get_json()
    if not data or "problem" not in data:
        return jsonify({"error": "Problem field required"}), 400
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    
    cpp_prompt = f"""You are a C++ competitive programming expert and LeetCode Grandmaster (rating 3500+).
You ALWAYS write fully working, efficient C++ solutions.

Rules:
1️⃣ NO templates or placeholders - only complete working C++ code
2️⃣ Include ALL necessary headers (#include statements)
3️⃣ Use optimal STL containers and algorithms
4️⃣ Follow this EXACT structure:

---
Time complexity: O(...)
Space complexity: O(...)

```cpp
#include <vector>
#include <algorithm>
// Add other necessary includes

class Solution {{
public:
    returnType functionName(parameters) {{
        // Complete optimized implementation
        return result;
    }}
}};
```

Algorithm: <2-3 sentence explanation>

Test cases:
- Input: [...] → Output: [...]
- Input: [...] → Output: [...]
---

SOLVE THIS C++ LEETCODE PROBLEM:
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
                    "parts": [{"text": cpp_prompt}]
                }],
                "generationConfig": {
                    "maxOutputTokens": 1500,
                    "temperature": 0,
                    "topP": 0.8,
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
                "language": "cpp",
                "status": "success"
            })
        else:
            return jsonify({"error": f"API Error: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500