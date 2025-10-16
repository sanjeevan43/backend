from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set your OpenAI API key
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

@app.route('/solve', methods=['POST'])
def solve_leetcode():
    """
    Main endpoint to solve LeetCode problems
    
    Request JSON:
    {
        "problem": "Two Sum problem description here...",
        "language": "python"
    }
    """
    try:
        data = request.json
        problem = data.get('problem', '')
        language = data.get('language', 'python')
        
        if not problem:
            return jsonify({'error': 'Problem description required'}), 400
        
        # Create prompt for OpenAI
        prompt = f"""Solve this LeetCode problem in {language}:

{problem}

Provide:
1. Explanation of approach
2. Time & Space complexity
3. Complete working code
4. Test cases"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert LeetCode problem solver."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        solution = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'solution': solution,
            'tokens': response.usage.total_tokens
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/optimize', methods=['POST'])
def optimize_code():
    """
    Optimize existing code
    
    Request JSON:
    {
        "code": "your code here",
        "language": "python"
    }
    """
    try:
        data = request.json
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'Code required'}), 400
        
        prompt = f"""Optimize this {language} code:

{code}

Provide:
1. Optimized version
2. What was improved
3. Complexity analysis"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a code optimization expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500
        )
        
        return jsonify({
            'success': True,
            'optimized': response.choices[0].message.content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/explain', methods=['POST'])
def explain_code():
    """
    Explain code solution
    
    Request JSON:
    {
        "code": "code to explain"
    }
    """
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code:
            return jsonify({'error': 'Code required'}), 400
        
        prompt = f"""Explain this code step by step:

{code}

Include time and space complexity."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a code explanation expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        return jsonify({
            'success': True,
            'explanation': response.choices[0].message.content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/debug', methods=['POST'])
def debug_code():
    """
    Debug code and find errors
    
    Request JSON:
    {
        "code": "buggy code",
        "error": "error message (optional)"
    }
    """
    try:
        data = request.json
        code = data.get('code', '')
        error_msg = data.get('error', 'No error message provided')
        
        if not code:
            return jsonify({'error': 'Code required'}), 400
        
        prompt = f"""Debug this code:

Code:
{code}

Error: {error_msg}

Provide:
1. What's wrong
2. Fixed code
3. Explanation"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a debugging expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        return jsonify({
            'success': True,
            'debug_info': response.choices[0].message.content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    return jsonify({'status': 'API is running!', 'version': '1.0'})


if __name__ == '__main__':
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  WARNING: Set OPENAI_API_KEY environment variable!")
        print("Example: export OPENAI_API_KEY='your-key-here'")
    
    print("🚀 LeetCode Solver API starting on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)