def handler(request, response):
    response.status_code = 200
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    if request.method == 'GET':
        return '{"message": "LeetCode AI is running"}'
    
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            problem = data.get('problem', '')
            
            if 'two sum' in problem.lower():
                solution = "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []"
            else:
                solution = "def solve():\n    pass"
            
            return json.dumps({"success": True, "solution": solution})
        except:
            response.status_code = 500
            return '{"error": "Invalid request"}'
    
    return '{"error": "Method not allowed"}'