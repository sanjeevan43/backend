from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {"message": "LeetCode Solving AI is running"}
        self.wfile.write(json.dumps(response).encode())
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            problem = data.get('problem', '')
            
            if not problem:
                self.send_error(400, "Problem is required")
                return
            
            # Simple problem detection and solution
            if 'two sum' in problem.lower():
                solution = """## Problem Analysis
Hash Map - Store complements for O(1) lookup

### Python
```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

## Complexity Analysis
Time: O(n), Space: O(n)"""
            elif 'palindrome' in problem.lower():
                solution = """## Problem Analysis
Two Pointer - Compare characters from both ends

### Python
```python
def is_palindrome(s):
    s = ''.join(c.lower() for c in s if c.isalnum())
    return s == s[::-1]
```

## Complexity Analysis
Time: O(n), Space: O(1)"""
            else:
                solution = f"""## Problem Analysis
Analyze the problem requirements

### Python
```python
def solve():
    # Problem: {problem}
    # Your implementation here
    pass
```

## Complexity Analysis
Depends on chosen algorithm"""
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"success": True, "solution": solution}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()