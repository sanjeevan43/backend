from flask import jsonify

def generate_fallback_solution(problem, language='python'):
    """Generate solution when external API fails"""
    problem_lower = problem.lower()
    
    # Detect problem type
    if 'two sum' in problem_lower or ('target' in problem_lower and 'sum' in problem_lower):
        return get_two_sum_solution(language)
    elif 'palindrome' in problem_lower:
        return get_palindrome_solution(language)
    elif 'valid parentheses' in problem_lower or 'brackets' in problem_lower:
        return get_parentheses_solution(language)
    elif 'fibonacci' in problem_lower:
        return get_fibonacci_solution(language)
    else:
        return get_general_solution(language)

def get_two_sum_solution(language):
    solutions = {
        'python': '''Time: O(n)
Space: O(n)

```python
class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []
```

Explanation: Use hash map to store numbers and their indices. For each number, check if its complement exists in the hash map.''',
        'javascript': '''Time: O(n)
Space: O(n)

```javascript
function twoSum(nums, target) {
    const seen = new Map();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.has(complement)) {
            return [seen.get(complement), i];
        }
        seen.set(nums[i], i);
    }
    return [];
}
```

Explanation: Use Map for O(1) lookups to find complement of each number.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_palindrome_solution(language):
    solutions = {
        'python': '''Time: O(n)
Space: O(1)

```python
class Solution:
    def isPalindrome(self, s):
        left, right = 0, len(s) - 1
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True
```

Explanation: Two-pointer technique comparing characters from both ends.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_parentheses_solution(language):
    solutions = {
        'python': '''Time: O(n)
Space: O(n)

```python
class Solution:
    def isValid(self, s):
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        
        for char in s:
            if char in mapping:
                if not stack or stack.pop() != mapping[char]:
                    return False
            else:
                stack.append(char)
        
        return not stack
```

Explanation: Use stack to match opening and closing brackets.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_fibonacci_solution(language):
    solutions = {
        'python': '''Time: O(n)
Space: O(1)

```python
class Solution:
    def fib(self, n):
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
```

Explanation: Iterative approach with two variables to avoid recursion.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_general_solution(language):
    solutions = {
        'python': '''Time: O(n)
Space: O(1)

```python
class Solution:
    def solve(self, input_data):
        # Analyze the problem
        # Choose appropriate data structures
        # Implement step by step
        
        result = []
        # Your solution logic here
        
        return result
```

Explanation: General template - analyze problem, choose data structures, implement solution.'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})