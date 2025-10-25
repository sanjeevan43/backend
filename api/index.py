from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import os
import logging
from dotenv import load_dotenv
from fallback import generate_fallback_solution

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
MAX_OUTPUT_TOKENS = int(os.getenv('MAX_OUTPUT_TOKENS', '1500'))
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.1'))
TOP_P = float(os.getenv('TOP_P', '0.9'))

@app.route("/")
def root():
    return jsonify({
        "message": "LeetCode Problems Only - Coding Challenge Solver API", 
        "endpoint": "/solve",
        "usage": "Send LeetCode problems only. Other queries will be rejected.",
        "docs": "/docs",
        "health": "/health"
    })

@app.route("/health")
def health_check():
    """Health check endpoint"""
    api_key = os.getenv("GEMINI_API_KEY")
    return jsonify({
        "status": "healthy",
        "api_configured": bool(api_key and api_key != "your_api_key_here"),
        "fallback_available": True
    })

@app.route("/docs")
def swagger_ui():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>LeetCode Solver API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; }
        .endpoint { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .method { background: #007bff; color: white; padding: 5px 10px; border-radius: 3px; }
        .post { background: #28a745; }
        pre { background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        textarea { width: 100%; height: 100px; margin: 10px 0; }
        #result { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 LeetCode Solver API Documentation</h1>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> /</h3>
            <p>Get API information</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method post">POST</span> /solve</h3>
            <p>Solve LeetCode problems with complete Python solutions</p>
            
            <h4>Request Body:</h4>
            <pre>{
  "problem": "Your LeetCode problem description here"
}</pre>
            
            <h4>Try it out:</h4>
            <textarea id="problemInput" placeholder="Enter your LeetCode problem here...">Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.</textarea>
            <br>
            <button onclick="solveProblem()">Solve Problem</button>
            
            <div id="result"></div>
        </div>
    </div>
    
    <script>
        async function solveProblem() {
            const problem = document.getElementById('problemInput').value;
            const resultDiv = document.getElementById('result');
            
            if (!problem.trim()) {
                resultDiv.innerHTML = '<p style="color: red;">Please enter a problem description</p>';
                return;
            }
            
            resultDiv.innerHTML = '<p>Solving...</p>';
            
            try {
                const response = await fetch('/solve', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ problem: problem })
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    resultDiv.innerHTML = `<h4>Solution:</h4><pre>${data.solution}</pre>`;
                } else {
                    resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            }
        }
    </script>
</body>
</html>
    ''')

@app.route("/solve", methods=["POST"])
def solve_leetcode():
    try:
        data = request.get_json()
        if not data or "problem" not in data:
            return jsonify({"error": "Problem field required"}), 400
        
        if not data['problem'].strip():
            return jsonify({"error": "Problem description cannot be empty"}), 400
    except Exception as e:
        logger.error(f"Error parsing request: {str(e)}")
        return jsonify({"error": "Invalid JSON format"}), 400
    
    # Get language preference (default to python)
    language = data.get('language', 'python')
    
    # Validate it's a LeetCode problem
    problem_text = data['problem'].lower()
    leetcode_keywords = os.getenv('LEETCODE_KEYWORDS', 
        'array,string,linked list,tree,graph,dynamic programming,binary search,sorting,hash table,stack,queue,heap,two pointers,sliding window,backtracking,greedy,dfs,bfs,leetcode,given,return,constraints,example,input,output,nums,target,solution,algorithm,complexity'
    ).split(',')
    
    if not any(keyword.strip() in problem_text for keyword in leetcode_keywords):
        return jsonify({"error": "This API only solves LeetCode coding problems. Please provide a valid LeetCode problem."}), 400
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        logger.warning("GEMINI_API_KEY not found, using fallback solution")
        return generate_fallback_solution(data['problem'], language)
    
    # Language-specific formats from environment or defaults
    lang_formats = {
        'python': os.getenv('PYTHON_FORMAT', 'class Solution:\n    def methodName(self, params):\n        # implementation\n        return result'),
        'javascript': os.getenv('JS_FORMAT', 'function methodName(params) {\n    // implementation\n    return result;\n}'),
        'java': os.getenv('JAVA_FORMAT', 'class Solution {\n    public returnType methodName(params) {\n        // implementation\n        return result;\n    }\n}'),
        'cpp': os.getenv('CPP_FORMAT', 'class Solution {\npublic:\n    returnType methodName(params) {\n        // implementation\n        return result;\n    }\n};')
    }
    
    format_example = lang_formats.get(language, lang_formats['python'])
    
    base_prompt = os.getenv('BASE_PROMPT', 'You are a LeetCode expert. Solve this specific problem with complete working {language} code:')
    
    prompt = f"""{base_prompt.format(language=language)}

{data['problem']}

RULES:
- Provide complete working {language} solution
- Use proper LeetCode format for {language}
- Include time/space complexity
- Add brief explanation

Format:
Time: O(...)
Space: O(...)

```{language}
{format_example}
```

Explanation: [brief algorithm description]"""
    
    # Get API endpoint from environment
    api_endpoint = os.getenv('GEMINI_API_ENDPOINT', 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent')
    
    try:
        logger.info(f"Making API request to solve {language} problem")
        response = requests.post(
            api_endpoint,
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": API_KEY,
            },
            json={
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "maxOutputTokens": MAX_OUTPUT_TOKENS,
                    "temperature": TEMPERATURE,
                    "topP": TOP_P
                }
            },
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
                logger.info("Successfully generated solution via API")
                return jsonify({
                    "solution": ai_response,
                    "problem": data['problem'],
                    "status": "success"
                })
            else:
                logger.error("Invalid API response structure")
                return generate_fallback_solution(data['problem'], language)
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return generate_fallback_solution(data['problem'], language)
            
    except requests.exceptions.Timeout:
        logger.error("API request timed out")
        return generate_fallback_solution(data['problem'], language)
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to API")
        return generate_fallback_solution(data['problem'], language)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return generate_fallback_solution(data['problem'], language)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)