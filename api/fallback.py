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
    elif 'reverse' in problem_lower and ('string' in problem_lower or 'array' in problem_lower):
        return get_reverse_solution(language)
    elif 'maximum subarray' in problem_lower or 'kadane' in problem_lower:
        return get_max_subarray_solution(language)
    else:
        return get_general_solution(language)

def get_two_sum_solution(language):
    solutions = {
        'python': '''class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []''',
        'javascript': '''var twoSum = function(nums, target) {
    const seen = new Map();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.has(complement)) {
            return [seen.get(complement), i];
        }
        seen.set(nums[i], i);
    }
    return [];
};''',
        'java': '''class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (seen.containsKey(complement)) {
                return new int[]{seen.get(complement), i};
            }
            seen.put(nums[i], i);
        }
        return new int[]{};
    }
}''',
        'cpp': '''class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen;
        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums[i];
            if (seen.find(complement) != seen.end()) {
                return {seen[complement], i};
            }
            seen[nums[i]] = i;
        }
        return {};
    }
};'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_palindrome_solution(language):
    solutions = {
        'python': '''class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = ''.join(c.lower() for c in s if c.isalnum())
        left, right = 0, len(s) - 1
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True''',
        'javascript': '''var isPalindrome = function(s) {
    s = s.toLowerCase().replace(/[^a-z0-9]/g, '');
    let left = 0, right = s.length - 1;
    while (left < right) {
        if (s[left] !== s[right]) {
            return false;
        }
        left++;
        right--;
    }
    return true;
};'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_parentheses_solution(language):
    solutions = {
        'python': '''class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        
        for char in s:
            if char in mapping:
                if not stack or stack.pop() != mapping[char]:
                    return False
            else:
                stack.append(char)
        
        return not stack''',
        'javascript': '''var isValid = function(s) {
    const stack = [];
    const mapping = {')': '(', '}': '{', ']': '['};
    
    for (let char of s) {
        if (char in mapping) {
            if (!stack.length || stack.pop() !== mapping[char]) {
                return false;
            }
        } else {
            stack.push(char);
        }
    }
    
    return stack.length === 0;
};'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_fibonacci_solution(language):
    solutions = {
        'python': '''class Solution:
    def fib(self, n: int) -> int:
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b''',
        'javascript': '''var fib = function(n) {
    if (n <= 1) return n;
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
        [a, b] = [b, a + b];
    }
    return b;
};'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_reverse_solution(language):
    solutions = {
        'python': '''class Solution:
    def reverseString(self, s: List[str]) -> None:
        left, right = 0, len(s) - 1
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1''',
        'javascript': '''var reverseString = function(s) {
    let left = 0, right = s.length - 1;
    while (left < right) {
        [s[left], s[right]] = [s[right], s[left]];
        left++;
        right--;
    }
};'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_max_subarray_solution(language):
    solutions = {
        'python': '''class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = current_sum = nums[0]
        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        return max_sum''',
        'javascript': '''var maxSubArray = function(nums) {
    let maxSum = nums[0];
    let currentSum = nums[0];
    
    for (let i = 1; i < nums.length; i++) {
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        maxSum = Math.max(maxSum, currentSum);
    }
    
    return maxSum;
};'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})

def get_general_solution(language):
    solutions = {
        'python': '''class Solution:
    def solve(self, input_data):
        # Copy this code to LeetCode
        # Replace method name and parameters as needed
        
        result = []
        # Your solution logic here
        
        return result''',
        'javascript': '''var solve = function(inputData) {
    // Copy this code to LeetCode
    // Replace function name and parameters as needed
    
    let result = [];
    // Your solution logic here
    
    return result;
};'''
    }
    return jsonify({"solution": solutions.get(language, solutions['python']), "status": "success"})