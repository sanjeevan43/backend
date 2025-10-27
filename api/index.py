from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"], supports_credentials=True)

@app.route("/")
def root():
    return jsonify({"message": "LeetCode AI Solver API", "status": "online"})

@app.route("/solve", methods=["POST"])
def solve_leetcode():
    try:
        data = request.get_json()
        if not data or "problem" not in data:
            return jsonify({"error": "Problem field required"}), 400
        
        problem_text = data['problem'].strip()
        if len(problem_text) < 3:
            return jsonify({"error": "Please provide a problem description."}), 400
        
        language = data.get('language', 'python')
        API_KEY = os.getenv("GEMINI_API_KEY")
        
        if not API_KEY:
            return jsonify({"error": "API key not configured"}), 500
        
        prompt = f"""Provide ONLY the {language} code for this LeetCode problem:

{problem_text}

Return ONLY the code without markdown formatting or explanations."""
        
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            headers={"Content-Type": "application/json", "X-goog-api-key": API_KEY},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": 1000, "temperature": 0.1}
            },
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
            clean_code = ai_response.replace('```python', '').replace('```javascript', '').replace('```java', '').replace('```cpp', '').replace('```', '').strip()
            return jsonify({"solution": clean_code, "status": "success"})
        else:
            return jsonify({"error": f"API Error: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)