from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Python LeetCode AI is running", "version": "1.0"})

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        problem = data.get('problem', '')
        language = data.get('language', 'python')
        
        if not problem:
            return jsonify({"error": "Problem is required"}), 400
        
        solution = generate_solution(problem, language)
        return jsonify({"success": True, "solution": solution})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_solution(problem, language):
    problem_lower = problem.lower()
    
    # Two Sum
    if 'two sum' in problem_lower:
        return f"""## Two Sum Solution

### Approach: Hash Map
Use a hash map to store complements for O(1) lookup.

### {language.title()} Code:
```{language}
def two_sum(nums, target):
    seen = {{}}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

### Complexity:
- Time: O(n)
- Space: O(n)"""

    # Palindrome
    elif 'palindrome' in problem_lower:
        return f"""## Palindrome Solution

### Approach: Two Pointer
Compare characters from both ends moving inward.

### {language.title()} Code:
```{language}
def is_palindrome(s):
    s = ''.join(c.lower() for c in s if c.isalnum())
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

### Complexity:
- Time: O(n)
- Space: O(1)"""

    # Fibonacci
    elif 'fibonacci' in problem_lower:
        return f"""## Fibonacci Solution

### Approach: Iterative DP
Build up from base cases to avoid recursion overhead.

### {language.title()} Code:
```{language}
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

### Complexity:
- Time: O(n)
- Space: O(1)"""

    # Binary Search
    elif 'binary search' in problem_lower:
        return f"""## Binary Search Solution

### Approach: Divide and Conquer
Eliminate half the search space each iteration.

### {language.title()} Code:
```{language}
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### Complexity:
- Time: O(log n)
- Space: O(1)"""

    # Maximum Subarray (Kadane's Algorithm)
    elif 'maximum subarray' in problem_lower or 'kadane' in problem_lower:
        return f"""## Maximum Subarray Solution

### Approach: Kadane's Algorithm
Dynamic programming to find maximum sum subarray.

### {language.title()} Code:
```{language}
def max_subarray(nums):
    max_sum = current_sum = nums[0]
    for i in range(1, len(nums)):
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    return max_sum
```

### Complexity:
- Time: O(n)
- Space: O(1)"""

    # Valid Parentheses
    elif 'valid parentheses' in problem_lower or 'balanced' in problem_lower:
        return f"""## Valid Parentheses Solution

### Approach: Stack
Use LIFO structure to match opening and closing brackets.

### {language.title()} Code:
```{language}
def is_valid(s):
    stack = []
    mapping = {{')': '(', '}}': '{{', ']': '['}}
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    return not stack
```

### Complexity:
- Time: O(n)
- Space: O(n)"""

    # Reverse String/Array
    elif 'reverse' in problem_lower:
        return f"""## Reverse Solution

### Approach: Two Pointer
Swap elements from both ends moving inward.

### {language.title()} Code:
```{language}
def reverse_string(s):
    s = list(s)
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    return ''.join(s)
```

### Complexity:
- Time: O(n)
- Space: O(1)"""

    # Merge Sorted Arrays
    elif 'merge' in problem_lower and 'sorted' in problem_lower:
        return f"""## Merge Sorted Arrays Solution

### Approach: Two Pointer
Compare elements and merge in sorted order.

### {language.title()} Code:
```{language}
def merge_sorted_arrays(arr1, arr2):
    result = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result
```

### Complexity:
- Time: O(m + n)
- Space: O(m + n)"""

    # Factorial
    elif 'factorial' in problem_lower:
        return f"""## Factorial Solution

### Approach: Iterative
Multiply numbers from 1 to n.

### {language.title()} Code:
```{language}
def factorial(n):
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

### Complexity:
- Time: O(n)
- Space: O(1)"""

    # Prime Numbers
    elif 'prime' in problem_lower:
        return f"""## Prime Number Solution

### Approach: Trial Division
Check divisibility up to sqrt(n) for efficiency.

### {language.title()} Code:
```{language}
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True
```

### Complexity:
- Time: O(√n)
- Space: O(1)"""

    # Linked List
    elif 'linked list' in problem_lower:
        return f"""## Linked List Solution

### Approach: Iterative Traversal
Process nodes one by one with proper pointer management.

### {language.title()} Code:
```{language}
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    prev = None
    current = head
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    return prev
```

### Complexity:
- Time: O(n)
- Space: O(1)"""

    # Binary Tree
    elif 'binary tree' in problem_lower or 'tree' in problem_lower:
        return f"""## Binary Tree Solution

### Approach: Tree Traversal
Use DFS or BFS to process tree nodes.

### {language.title()} Code:
```{language}
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root):
    result = []
    def dfs(node):
        if node:
            dfs(node.left)
            result.append(node.val)
            dfs(node.right)
    dfs(root)
    return result
```

### Complexity:
- Time: O(n)
- Space: O(h) where h is height"""

    # Default case
    else:
        return f"""## General Solution Template

### Problem Analysis:
{problem}

### {language.title()} Code:
```{language}
def solve():
    # Step 1: Understand the problem
    # Step 2: Identify input/output format
    # Step 3: Choose appropriate algorithm
    # Step 4: Handle edge cases
    
    # Your implementation here
    pass
```

### Approach:
1. Break down the problem into smaller parts
2. Choose the right data structure
3. Optimize for time/space complexity
4. Test with edge cases"""

@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code:
            return jsonify({"error": "Code is required"}), 400
        
        optimized = analyze_and_optimize(code)
        return jsonify({"success": True, "optimized": optimized})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def analyze_and_optimize(code):
    suggestions = []
    
    if 'for' in code and 'append' in code:
        suggestions.append("• Use list comprehension instead of for loop with append")
    
    if 'range(len(' in code:
        suggestions.append("• Use enumerate() instead of range(len())")
    
    if code.count('if') > 3:
        suggestions.append("• Consider using dictionary mapping for multiple conditions")
    
    optimizations = "\n".join(suggestions) if suggestions else "• Code looks well optimized!"
    
    return f"""## Code Optimization Analysis

### Current Code:
```python
{code}
```

### Optimization Suggestions:
{optimizations}

### General Tips:
• Use built-in functions when possible
• Avoid nested loops if not necessary
• Consider space-time tradeoffs
• Use appropriate data structures"""

@app.route('/explain', methods=['POST'])
def explain():
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code:
            return jsonify({"error": "Code is required"}), 400
        
        explanation = explain_code(code)
        return jsonify({"success": True, "explanation": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def explain_code(code):
    return f"""## Code Explanation

### Code Analysis:
```python
{code}
```

### Step-by-Step Breakdown:
1. **Function Definition**: The main logic is encapsulated in a function
2. **Input Processing**: Parameters are processed and validated
3. **Algorithm Implementation**: Core logic executes the solution
4. **Return Statement**: Final result is returned

### Key Concepts:
• **Data Structures**: Analyze which data structures are used
• **Algorithm Pattern**: Identify the algorithmic approach
• **Time Complexity**: Consider the efficiency of operations
• **Space Complexity**: Evaluate memory usage

### Best Practices:
• Add input validation
• Handle edge cases
• Use meaningful variable names
• Add comments for complex logic"""

@app.route('/debug', methods=['POST'])
def debug():
    try:
        data = request.get_json()
        code = data.get('code', '')
        error = data.get('error', '')
        
        if not code:
            return jsonify({"error": "Code is required"}), 400
        
        debug_info = debug_code(code, error)
        return jsonify({"success": True, "debug_info": debug_info})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def debug_code(code, error):
    common_fixes = []
    
    if 'IndexError' in error:
        common_fixes.append("• Check array bounds before accessing elements")
        common_fixes.append("• Use len() to verify array size")
    
    if 'KeyError' in error:
        common_fixes.append("• Use dict.get() method with default values")
        common_fixes.append("• Check if key exists before accessing")
    
    if 'TypeError' in error:
        common_fixes.append("• Verify variable types before operations")
        common_fixes.append("• Add type checking or conversion")
    
    fixes = "\n".join(common_fixes) if common_fixes else "• Add print statements to trace execution"
    
    return f"""## Debug Analysis

### Code Under Review:
```python
{code}
```

### Error Information:
{error if error else 'No specific error provided'}

### Common Fixes:
{fixes}

### Debugging Steps:
1. **Add Print Statements**: Trace variable values
2. **Check Edge Cases**: Test with empty/null inputs
3. **Verify Logic**: Ensure algorithm correctness
4. **Test Incrementally**: Start with simple cases

### Prevention Tips:
• Always validate inputs
• Handle edge cases explicitly
• Use try-catch for error handling
• Test with various input sizes"""

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        "status": "Python LeetCode AI is running!",
        "version": "1.0",
        "endpoints": {
            "POST /solve": "Solve coding problems",
            "POST /optimize": "Optimize existing code", 
            "POST /explain": "Explain code logic",
            "POST /debug": "Debug and fix code",
            "GET /test": "API status check"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)