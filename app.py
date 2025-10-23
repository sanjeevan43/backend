from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return jsonify({"message": "LeetCode AI Solver"})

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    problem = data.get('problem', '')
    
    if not problem:
        return jsonify({"error": "Problem required"}), 400
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a LeetCode expert."},
                {"role": "user", "content": f"Solve: {problem}"}
            ],
            max_tokens=1500
        )
        
        return jsonify({
            "success": True,
            "solution": response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)