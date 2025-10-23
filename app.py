from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "LeetCode Solving AI is running"})

@app.route('/solve', methods=['POST', 'OPTIONS'])
def solve():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    try:
        data = request.get_json()
        problem = data.get('problem', '')
        languages = data.get('languages', ['python'])
        
        if not problem:
            return jsonify({"error": "Problem is required"}), 400
        
        def solve_coding_problem(problem_text, languages):
            problem_lower = problem_text.lower()
            
            if 'two sum' in problem_lower or 'target sum' in problem_lower:
                return generate_two_sum_solution(languages)
            elif 'palindrome' in problem_lower:
                return generate_palindrome_solution(languages)
            elif 'reverse' in problem_lower and ('string' in problem_lower or 'array' in problem_lower):
                return generate_reverse_solution(languages)
            elif 'fibonacci' in problem_lower:
                return generate_fibonacci_solution(languages)
            elif 'factorial' in problem_lower:
                return generate_factorial_solution(languages)
            elif 'prime' in problem_lower:
                return generate_prime_solution(languages)
            elif 'binary search' in problem_lower:
                return generate_binary_search_solution(languages)
            elif 'maximum subarray' in problem_lower or 'kadane' in problem_lower:
                return generate_max_subarray_solution(languages)
            elif 'valid parentheses' in problem_lower or 'balanced parentheses' in problem_lower:
                return generate_valid_parentheses_solution(languages)
            elif 'merge' in problem_lower and 'sorted' in problem_lower:
                return generate_merge_arrays_solution(languages)
            else:
                return generate_general_solution(problem_text, languages)
        
        def generate_two_sum_solution(languages):
            solutions = {
                'python': '''def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []''',
                'javascript': '''function twoSum(nums, target) {
    const seen = new Map();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.has(complement)) {
            return [seen.get(complement), i];
        }
        seen.set(nums[i], i);
    }
    return [];
}''',
                'java': '''public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (seen.containsKey(complement)) {
            return new int[]{seen.get(complement), i};
        }
        seen.put(nums[i], i);
    }
    return new int[]{};
}'''
            }
            return {
                'approach': 'Hash Map - Store complements for O(1) lookup',
                'complexity': 'Time: O(n), Space: O(n)',
                'solutions': solutions
            }
        
        def generate_palindrome_solution(languages):
            solutions = {
                'python': '''def is_palindrome(s):
    s = ''.join(c.lower() for c in s if c.isalnum())
    return s == s[::-1]

# Two pointer approach
def is_palindrome_two_pointer(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True''',
                'javascript': '''function isPalindrome(s) {
    const cleaned = s.toLowerCase().replace(/[^a-z0-9]/g, '');
    return cleaned === cleaned.split('').reverse().join('');
}

// Two pointer approach
function isPalindromeTwoPointer(s) {
    let left = 0, right = s.length - 1;
    while (left < right) {
        if (s[left].toLowerCase() !== s[right].toLowerCase()) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}''',
                'java': '''public boolean isPalindrome(String s) {
    String cleaned = s.toLowerCase().replaceAll("[^a-z0-9]", "");
    return cleaned.equals(new StringBuilder(cleaned).reverse().toString());
}

// Two pointer approach
public boolean isPalindromeTwoPointer(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}'''
            }
            return {
                'approach': 'Two Pointer - Compare characters from both ends',
                'complexity': 'Time: O(n), Space: O(1)',
                'solutions': solutions
            }
        
        def generate_reverse_solution(languages):
            solutions = {
                'python': '''def reverse_string(s):
    return s[::-1]

# In-place for list
def reverse_list_inplace(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr''',
                'javascript': '''function reverseString(s) {
    return s.split('').reverse().join('');
}

// In-place for array
function reverseArrayInPlace(arr) {
    let left = 0, right = arr.length - 1;
    while (left < right) {
        [arr[left], arr[right]] = [arr[right], arr[left]];
        left++;
        right--;
    }
    return arr;
}''',
                'java': '''public String reverseString(String s) {
    return new StringBuilder(s).reverse().toString();
}

// In-place for array
public void reverseArray(int[] arr) {
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int temp = arr[left];
        arr[left] = arr[right];
        arr[right] = temp;
        left++;
        right--;
    }
}'''
            }
            return {
                'approach': 'Two Pointer - Swap elements from both ends',
                'complexity': 'Time: O(n), Space: O(1)',
                'solutions': solutions
            }
        
        def generate_fibonacci_solution(languages):
            solutions = {
                'python': '''def fibonacci(n):
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Recursive with memoization
def fibonacci_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    return memo[n]''',
                'javascript': '''function fibonacci(n) {
    if (n <= 1) return n;
    
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
        [a, b] = [b, a + b];
    }
    return b;
}

// Recursive with memoization
function fibonacciMemo(n, memo = {}) {
    if (n in memo) return memo[n];
    if (n <= 1) return n;
    memo[n] = fibonacciMemo(n-1, memo) + fibonacciMemo(n-2, memo);
    return memo[n];
}''',
                'java': '''public int fibonacci(int n) {
    if (n <= 1) return n;
    
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// Dynamic Programming
public int fibonacciDP(int n) {
    if (n <= 1) return n;
    
    int[] dp = new int[n + 1];
    dp[0] = 0;
    dp[1] = 1;
    
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i-1] + dp[i-2];
    }
    return dp[n];
}'''
            }
            return {
                'approach': 'Iterative - Build up from base cases',
                'complexity': 'Time: O(n), Space: O(1)',
                'solutions': solutions
            }
        
        def generate_factorial_solution(languages):
            solutions = {
                'python': '''def factorial(n):
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Recursive
def factorial_recursive(n):
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)''',
                'javascript': '''function factorial(n) {
    if (n <= 1) return 1;
    let result = 1;
    for (let i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// Recursive
function factorialRecursive(n) {
    if (n <= 1) return 1;
    return n * factorialRecursive(n - 1);
}''',
                'java': '''public long factorial(int n) {
    if (n <= 1) return 1;
    long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// Recursive
public long factorialRecursive(int n) {
    if (n <= 1) return 1;
    return n * factorialRecursive(n - 1);
}'''
            }
            return {
                'approach': 'Iterative multiplication from 1 to n',
                'complexity': 'Time: O(n), Space: O(1)',
                'solutions': solutions
            }
        
        def generate_prime_solution(languages):
            solutions = {
                'python': '''def is_prime(n):
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

def sieve_of_eratosthenes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    
    return [i for i in range(2, limit + 1) if sieve[i]]''',
                'javascript': '''function isPrime(n) {
    if (n < 2) return false;
    if (n === 2) return true;
    if (n % 2 === 0) return false;
    
    for (let i = 3; i <= Math.sqrt(n); i += 2) {
        if (n % i === 0) return false;
    }
    return true;
}

function sieveOfEratosthenes(limit) {
    const sieve = new Array(limit + 1).fill(true);
    sieve[0] = sieve[1] = false;
    
    for (let i = 2; i <= Math.sqrt(limit); i++) {
        if (sieve[i]) {
            for (let j = i * i; j <= limit; j += i) {
                sieve[j] = false;
            }
        }
    }
    
    return sieve.map((isPrime, num) => isPrime ? num : null)
                .filter(num => num !== null);
}''',
                'java': '''public boolean isPrime(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    
    for (int i = 3; i <= Math.sqrt(n); i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

public List<Integer> sieveOfEratosthenes(int limit) {
    boolean[] sieve = new boolean[limit + 1];
    Arrays.fill(sieve, true);
    sieve[0] = sieve[1] = false;
    
    for (int i = 2; i <= Math.sqrt(limit); i++) {
        if (sieve[i]) {
            for (int j = i * i; j <= limit; j += i) {
                sieve[j] = false;
            }
        }
    }
    
    List<Integer> primes = new ArrayList<>();
    for (int i = 2; i <= limit; i++) {
        if (sieve[i]) primes.add(i);
    }
    return primes;
}'''
            }
            return {
                'approach': 'Trial division up to sqrt(n) for efficiency',
                'complexity': 'Time: O(√n), Space: O(1)',
                'solutions': solutions
            }
        
        def generate_binary_search_solution(languages):
            solutions = {
                'python': '''def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1''',
                'javascript': '''function binarySearch(nums, target) {
    let left = 0, right = nums.length - 1;
    
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        if (nums[mid] === target) {
            return mid;
        } else if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1;
}''',
                'java': '''public int binarySearch(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) {
            return mid;
        } else if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1;
}'''
            }
            return {
                'approach': 'Divide and conquer - eliminate half each iteration',
                'complexity': 'Time: O(log n), Space: O(1)',
                'solutions': solutions
            }
        
        def generate_max_subarray_solution(languages):
            solutions = {
                'python': '''def max_subarray(nums):
    max_sum = current_sum = nums[0]
    
    for i in range(1, len(nums)):
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum''',
                'javascript': '''function maxSubarray(nums) {
    let maxSum = nums[0];
    let currentSum = nums[0];
    
    for (let i = 1; i < nums.length; i++) {
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        maxSum = Math.max(maxSum, currentSum);
    }
    
    return maxSum;
}''',
                'java': '''public int maxSubarray(int[] nums) {
    int maxSum = nums[0];
    int currentSum = nums[0];
    
    for (int i = 1; i < nums.length; i++) {
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        maxSum = Math.max(maxSum, currentSum);
    }
    
    return maxSum;
}'''
            }
            return {
                'approach': "Kadane's Algorithm - Dynamic Programming",
                'complexity': 'Time: O(n), Space: O(1)',
                'solutions': solutions
            }
        
        def generate_valid_parentheses_solution(languages):
            solutions = {
                'python': '''def is_valid_parentheses(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return not stack''',
                'javascript': '''function isValidParentheses(s) {
    const stack = [];
    const mapping = {')': '(', '}': '{', ']': '['};
    
    for (const char of s) {
        if (char in mapping) {
            if (!stack.length || stack.pop() !== mapping[char]) {
                return false;
            }
        } else {
            stack.push(char);
        }
    }
    
    return stack.length === 0;
}''',
                'java': '''public boolean isValidParentheses(String s) {
    Stack<Character> stack = new Stack<>();
    Map<Character, Character> mapping = new HashMap<>();
    mapping.put(')', '(');
    mapping.put('}', '{');
    mapping.put(']', '[');
    
    for (char c : s.toCharArray()) {
        if (mapping.containsKey(c)) {
            if (stack.isEmpty() || stack.pop() != mapping.get(c)) {
                return false;
            }
        } else {
            stack.push(c);
        }
    }
    
    return stack.isEmpty();
}'''
            }
            return {
                'approach': 'Stack - LIFO for matching pairs',
                'complexity': 'Time: O(n), Space: O(n)',
                'solutions': solutions
            }
        
        def generate_merge_arrays_solution(languages):
            solutions = {
                'python': '''def merge_sorted_arrays(arr1, arr2):
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
    return result''',
                'javascript': '''function mergeSortedArrays(arr1, arr2) {
    const result = [];
    let i = 0, j = 0;
    
    while (i < arr1.length && j < arr2.length) {
        if (arr1[i] <= arr2[j]) {
            result.push(arr1[i]);
            i++;
        } else {
            result.push(arr2[j]);
            j++;
        }
    }
    
    return result.concat(arr1.slice(i)).concat(arr2.slice(j));
}''',
                'java': '''public int[] mergeSortedArrays(int[] arr1, int[] arr2) {
    int[] result = new int[arr1.length + arr2.length];
    int i = 0, j = 0, k = 0;
    
    while (i < arr1.length && j < arr2.length) {
        if (arr1[i] <= arr2[j]) {
            result[k++] = arr1[i++];
        } else {
            result[k++] = arr2[j++];
        }
    }
    
    while (i < arr1.length) result[k++] = arr1[i++];
    while (j < arr2.length) result[k++] = arr2[j++];
    
    return result;
}'''
            }
            return {
                'approach': 'Two Pointer - Compare and merge in order',
                'complexity': 'Time: O(m+n), Space: O(m+n)',
                'solutions': solutions
            }
        
        def generate_general_solution(problem_text, languages):
            solutions = {}
            for lang in languages:
                if lang == 'python':
                    solutions[lang] = f'''def solve():
    """
    Problem: {problem_text}
    
    Steps to solve:
    1. Understand input/output format
    2. Identify constraints and edge cases
    3. Choose appropriate algorithm/data structure
    4. Implement and test
    """
    # Your implementation here
    pass'''
                elif lang == 'javascript':
                    solutions[lang] = f'''function solve() {{
    /*
    Problem: {problem_text}
    
    Steps to solve:
    1. Understand input/output format
    2. Identify constraints and edge cases
    3. Choose appropriate algorithm/data structure
    4. Implement and test
    */
    // Your implementation here
}}'''
                elif lang == 'java':
                    solutions[lang] = f'''public class Solution {{
    /*
    Problem: {problem_text}
    
    Steps to solve:
    1. Understand input/output format
    2. Identify constraints and edge cases
    3. Choose appropriate algorithm/data structure
    4. Implement and test
    */
    public void solve() {{
        // Your implementation here
    }}
}}'''
            
            return {
                'approach': 'Analyze the problem requirements and constraints',
                'complexity': 'Depends on chosen algorithm',
                'solutions': solutions
            }
        
        # Generate the actual solution
        result = solve_coding_problem(problem, languages)
        
        # Format the response
        solution = f"## Problem Analysis\n{result['approach']}\n\n"
        
        for lang in languages:
            if lang in result['solutions']:
                solution += f"### {lang.title()}\n```{lang}\n{result['solutions'][lang]}\n```\n\n"
        
        solution += f"## Complexity Analysis\n{result['complexity']}\n\n"
        solution += "## Key Implementation Notes\n"
        solution += "• Handle edge cases (empty input, single element)\n"
        solution += "• Consider integer overflow for large numbers\n"
        solution += "• Test with various input sizes\n"
        solution += "• Optimize for the given constraints"
        
        return jsonify({
            "success": True,
            "solution": solution
        })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)