import json

def handler(request):
    if request.method == 'GET':
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "LeetCode AI is running"})
        }
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            problem = data.get('problem', '')
            
            if 'two sum' in problem.lower():
                solution = "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []"
            else:
                solution = "def solve():\n    # Your solution here\n    pass"
            
            return {
                'statusCode': 200,
                'body': json.dumps({"success": True, "solution": solution})
            }
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": "Invalid request"})
            }