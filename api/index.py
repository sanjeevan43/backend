from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return jsonify({"message": "LeetCode Solver API", "endpoint": "/solve"})

def is_leetcode_problem(problem):
    leetcode_keywords = ["leetcode", "two sum", "array", "string", "linked list", "tree", "graph", "dynamic programming", "binary search", "sorting", "hash table", "stack", "queue", "heap", "trie", "backtracking", "greedy", "sliding window", "dfs", "bfs"]
    return any(keyword in problem.lower() for keyword in leetcode_keywords)

@app.route("/solve", methods=["POST"])
def solve_leetcode():
    data = request.get_json()
    if not data or "problem" not in data:
        return jsonify({"error": "Problem field required"}), 400
    
    problem = data["problem"]
    
    if not is_leetcode_problem(problem):
        return jsonify({"error": "Only LeetCode problems are allowed"}), 400
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
                    "parts": [{"text": f"Solve this LeetCode problem: {problem}"}]
                }],
                "generationConfig": {"maxOutputTokens": 500}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"response": ai_response})
        else:
            return jsonify({"error": f"API Error: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500