from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return jsonify({
        "message": "LeetCode AI Solver API",
        "status": "running",
        "endpoints": {
            "POST /solve": "Solve LeetCode problems",
            "POST /optimize": "Optimize code",
            "POST /explain": "Explain code"
        }
    })

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    problem = data.get('problem', '')
    
    if not problem:
        return jsonify({"error": "Problem required"}), 400
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a LeetCode expert."},
                {"role": "user", "content": f"Solve: {problem}"}
            ],
            "max_tokens": 1500
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                "success": True,
                "solution": result['choices'][0]['message']['content']
            })
        else:
            return jsonify({"error": "API error"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)