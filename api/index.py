from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

def get_openai_client():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY environment variable not set')
    return openai.OpenAI(api_key=api_key)

@app.route('/solve', methods=['POST'])
def solve_leetcode():
    try:
        data = request.json
        problem = data.get('problem', '')
        language = data.get('language', 'python')
        
        if not problem:
            return jsonify({'error': 'Problem description required'}), 400
        
        prompt = f"""Solve this LeetCode problem in {language}:

{problem}

Provide:
1. Explanation of approach
2. Time & Space complexity
3. Complete working code
4. Test cases"""

        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert LeetCode problem solver."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return jsonify({
            'success': True,
            'solution': response.choices[0].message.content,
            'tokens': response.usage.total_tokens
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/optimize', methods=['POST'])
def optimize_code():
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

        client = get_openai_client()
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
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code:
            return jsonify({'error': 'Code required'}), 400
        
        prompt = f"""Explain this code step by step:

{code}

Include time and space complexity."""

        client = get_openai_client()
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

        client = get_openai_client()
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
@app.route('/', methods=['GET'])
def test():
    return jsonify({'status': 'API is running!', 'version': '1.0'})

# Vercel handler
def handler(request):
    return app(request.environ, lambda status, headers: None)