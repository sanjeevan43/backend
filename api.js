const API_BASE_URLS = [
  'http://localhost:5000',
  'https://backend-fl5mva3dw-sanjeevans-projects-45db636c.vercel.app'
];

export const api = {
  async explainCode(problem, code, language) {
    for (const url of API_BASE_URLS) {
      try {
        const response = await fetch(`${url}/api/explain`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ problem, code, language }),
        });
        
        if (response.ok) {
          const data = await response.json();
          return data.explanation || data.result;
        }
      } catch (error) {
        console.error(`Explain API failed for ${url}:`, error.message);
      }
    }
    return 'Unable to explain code at this time.';
  },

  async optimizeCode(problem, code, language) {
    for (const url of API_BASE_URLS) {
      try {
        const response = await fetch(`${url}/api/optimize`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ problem, code, language }),
        });
        
        if (response.ok) {
          const data = await response.json();
          return data.optimized || data.result;
        }
      } catch (error) {
        console.error(`Optimize API failed for ${url}:`, error.message);
      }
    }
    return 'Unable to optimize code at this time.';
  },

  async generateTests(problem, constraints = '') {
    for (const url of API_BASE_URLS) {
      try {
        const response = await fetch(`${url}/api/test`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ problem, constraints }),
        });
        
        if (response.ok) {
          const data = await response.json();
          return data.tests || data.result;
        }
      } catch (error) {
        console.error(`Test generation API failed for ${url}:`, error.message);
      }
    }
    return 'Unable to generate test cases at this time.';
  },
  async checkStatus() {
    for (const url of API_BASE_URLS) {
      try {
        const response = await fetch(`${url}/`, {
          method: 'GET',
          headers: { 'Accept': 'application/json' },
        });
        if (response.ok) {
          return true;
        }
      } catch (error) {
        console.error(`Health check failed for ${url}:`, error.message);
      }
    }
    return false;
  },

  async solveProblem(problem, selectedLanguages = ['python']) {
    const language = selectedLanguages[0] || 'python';
    
    for (const url of API_BASE_URLS) {
      try {
        const response = await fetch(`${url}/solve`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ 
            problem: problem.trim(), 
            language: language 
          }),
          timeout: 15000
        });
        
        if (response.ok) {
          const data = await response.json();
          if (data.status === 'success' && data.solution) {
            return data.solution;
          }
        }
      } catch (error) {
        console.error(`API failed:`, error.message);
      }
    }
    
    return this.generateMockSolution(problem, selectedLanguages);
  },



  generateMockSolution(problem, selectedLanguages) {
    console.log('Generating mock solution for problem type detection...');
    
    // More comprehensive problem analysis
    const problemLower = problem.toLowerCase();
    let problemType = 'general';
    let algorithmType = 'iterative';
    
    // Enhanced problem detection
    if (problemLower.includes('two sum') || (problemLower.includes('target') && problemLower.includes('sum'))) {
      problemType = 'two_sum';
      algorithmType = 'hash_map';
    } else if (problemLower.includes('palindrome')) {
      problemType = 'palindrome';
      algorithmType = 'two_pointer';
    } else if (problemLower.includes('reverse')) {
      problemType = 'reverse';
      algorithmType = 'two_pointer';
    } else if (problemLower.includes('fibonacci') || problemLower.includes('fib')) {
      problemType = 'fibonacci';
      algorithmType = 'dynamic_programming';
    } else if (problemLower.includes('binary search') || (problemLower.includes('search') && problemLower.includes('sorted'))) {
      problemType = 'binary_search';
      algorithmType = 'divide_conquer';
    } else if (problemLower.includes('linked list') || problemLower.includes('listnode')) {
      problemType = 'linked_list';
      algorithmType = 'pointer_manipulation';
    } else if (problemLower.includes('binary tree') || problemLower.includes('treenode')) {
      problemType = 'binary_tree';
      algorithmType = 'recursion';
    } else if (problemLower.includes('valid parentheses') || problemLower.includes('brackets')) {
      problemType = 'stack';
      algorithmType = 'stack';
    } else if (problemLower.includes('longest') || problemLower.includes('maximum') || problemLower.includes('minimum')) {
      problemType = 'optimization';
      algorithmType = 'dynamic_programming';
    } else if (problemLower.includes('merge') || problemLower.includes('sort')) {
      problemType = 'sorting';
      algorithmType = 'merge_sort';
    } else if (problemLower.includes('duplicate') || problemLower.includes('unique')) {
      problemType = 'hash_set';
      algorithmType = 'hash_set';
    }
    
    console.log(`Detected problem type: ${problemType}, algorithm: ${algorithmType}`);
    
    const solutions = this.getSolutionTemplates(problemType, algorithmType);
    
    const solutionData = {
      python: {
        code: solutions.python,
        explanation: this.getExplanation('python', problemType, algorithmType)
      },
      javascript: {
        code: solutions.javascript,
        explanation: this.getExplanation('javascript', problemType, algorithmType)
      },
      java: {
        code: solutions.java,
        explanation: this.getExplanation('java', problemType, algorithmType)
      },
      cpp: {
        code: solutions.cpp,
        explanation: this.getExplanation('cpp', problemType, algorithmType)
      },
      csharp: {
        code: solutions.csharp,
        explanation: this.getExplanation('csharp', problemType, algorithmType)
      },
      go: {
        code: solutions.go,
        explanation: this.getExplanation('go', problemType, algorithmType)
      },
      rust: {
        code: solutions.rust,
        explanation: this.getExplanation('rust', problemType, algorithmType)
      },
      typescript: {
        code: solutions.typescript,
        explanation: this.getExplanation('typescript', problemType, algorithmType)
      }
    };
    
    const algorithmInfo = this.getAlgorithmInfo(problemType, algorithmType);
    
    let response = `## 🎯 Problem Analysis
**Problem**: ${problem.substring(0, 150)}${problem.length > 150 ? '...' : ''}
**Problem Type**: ${algorithmInfo.type}
**Algorithm**: ${algorithmInfo.algorithm}
**Time Complexity**: ${algorithmInfo.timeComplexity}
**Space Complexity**: ${algorithmInfo.spaceComplexity}

## 🧠 Learning Approach
**Core Concept**: ${algorithmInfo.concept}

**The "Aha!" Moment**: ${algorithmInfo.insight}

`;
    
    selectedLanguages.forEach(lang => {
      if (solutionData[lang]) {
        const langNames = {
          python: '🐍 Python',
          javascript: '🟨 JavaScript', 
          java: '☕ Java',
          cpp: '⚡ C++',
          csharp: '🔷 C#',
          go: '🐹 Go',
          rust: '🦀 Rust',
          typescript: '🔷 TypeScript'
        };
        response += `## ${langNames[lang]} Solution

${lang}
${solutionData[lang].code}

### 📚 ${langNames[lang]} Teaching Notes
${solutionData[lang].explanation}

`;
      }
    });
    
    response += `## 🎓 Key Learning Points
${algorithmInfo.keyPoints}

## 🚀 Next Steps
${algorithmInfo.nextSteps}`;
    
    return response;
  },

  getSolutionTemplates(problemType, algorithmType) {
    const templates = {
      two_sum: {
        python: `def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []`,
        javascript: `function twoSum(nums, target) {
    const seen = new Map();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.has(complement)) {
            return [seen.get(complement), i];
        }
        seen.set(nums[i], i);
    }
    return [];
}`,
        java: `public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (seen.containsKey(complement)) {
            return new int[]{seen.get(complement), i};
        }
        seen.put(nums[i], i);
    }
    return new int[]{};
}`,
        cpp: `vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if (seen.find(complement) != seen.end()) {
            return {seen[complement], i};
        }
        seen[nums[i]] = i;
    }
    return {};
}`,
        csharp: `public int[] TwoSum(int[] nums, int target) {
    var seen = new Dictionary<int, int>();
    for (int i = 0; i < nums.Length; i++) {
        int complement = target - nums[i];
        if (seen.ContainsKey(complement)) {
            return new int[] { seen[complement], i };
        }
        seen[nums[i]] = i;
    }
    return new int[] { };
}`,
        go: `func twoSum(nums []int, target int) []int {
    seen := make(map[int]int)
    for i, num := range nums {
        complement := target - num
        if idx, exists := seen[complement]; exists {
            return []int{idx, i}
        }
        seen[num] = i
    }
    return []int{}
}`,
        rust: `pub fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
    let mut seen = HashMap::new();
    for (i, &num) in nums.iter().enumerate() {
        let complement = target - num;
        if let Some(&idx) = seen.get(&complement) {
            return vec![idx as i32, i as i32];
        }
        seen.insert(num, i);
    }
    vec![]
}`,
        typescript: `function twoSum(nums: number[], target: number): number[] {
    const seen = new Map<number, number>();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.has(complement)) {
            return [seen.get(complement)!, i];
        }
        seen.set(nums[i], i);
    }
    return [];
}`
      },
      palindrome: {
        python: `def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True`,
        javascript: `function isPalindrome(s) {
    let left = 0, right = s.length - 1;
    while (left < right) {
        if (s[left] !== s[right]) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}`,
        java: `public boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}`,
        cpp: `bool isPalindrome(string s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        if (s[left] != s[right]) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}`,
        csharp: `public bool IsPalindrome(string s) {
    int left = 0, right = s.Length - 1;
    while (left < right) {
        if (s[left] != s[right]) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}`,
        go: `func isPalindrome(s string) bool {
    left, right := 0, len(s)-1
    for left < right {
        if s[left] != s[right] {
            return false
        }
        left++
        right--
    }
    return true
}`,
        rust: `pub fn is_palindrome(s: String) -> bool {
    let chars: Vec<char> = s.chars().collect();
    let mut left = 0;
    let mut right = chars.len() - 1;
    while left < right {
        if chars[left] != chars[right] {
            return false;
        }
        left += 1;
        right -= 1;
    }
    true
}`,
        typescript: `function isPalindrome(s: string): boolean {
    let left = 0, right = s.length - 1;
    while (left < right) {
        if (s[left] !== s[right]) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}`
      },
      stack: {
        python: `def is_valid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return not stack`,
        javascript: `function isValid(s) {
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
}`,
        java: `public boolean isValid(String s) {
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
}`,
        cpp: `bool isValid(string s) {
    stack<char> st;
    unordered_map<char, char> mapping = {{')', '('}, {'}', '{'}, {']', '['}};
    
    for (char c : s) {
        if (mapping.find(c) != mapping.end()) {
            if (st.empty() || st.top() != mapping[c]) {
                return false;
            }
            st.pop();
        } else {
            st.push(c);
        }
    }
    
    return st.empty();
}`,
        csharp: `public bool IsValid(string s) {
    var stack = new Stack<char>();
    var mapping = new Dictionary<char, char> {{')', '('}, {'}', '{'}, {']', '['}};
    
    foreach (char c in s) {
        if (mapping.ContainsKey(c)) {
            if (stack.Count == 0 || stack.Pop() != mapping[c]) {
                return false;
            }
        } else {
            stack.Push(c);
        }
    }
    
    return stack.Count == 0;
}`,
        go: `func isValid(s string) bool {
    stack := []rune{}
    mapping := map[rune]rune{')': '(', '}': '{', ']': '['}
    
    for _, char := range s {
        if open, exists := mapping[char]; exists {
            if len(stack) == 0 || stack[len(stack)-1] != open {
                return false
            }
            stack = stack[:len(stack)-1]
        } else {
            stack = append(stack, char)
        }
    }
    
    return len(stack) == 0
}`,
        rust: `pub fn is_valid(s: String) -> bool {
    let mut stack = Vec::new();
    let mapping = [(')', '('), ('}', '{'), (']', '[')];
    
    for ch in s.chars() {
        if let Some((_, open)) = mapping.iter().find(|(close, _)| *close == ch) {
            if stack.is_empty() || stack.pop() != Some(*open) {
                return false;
            }
        } else {
            stack.push(ch);
        }
    }
    
    stack.is_empty()
}`,
        typescript: `function isValid(s: string): boolean {
    const stack: string[] = [];
    const mapping: {[key: string]: string} = {')': '(', '}': '{', ']': '['};
    
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
}`
      },
      fibonacci: {
        python: `def fibonacci(n):
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]`,
        javascript: `function fibonacci(n) {
    if (n <= 1) return n;
    
    const dp = new Array(n + 1);
    dp[0] = 0;
    dp[1] = 1;
    
    for (let i = 2; i <= n; i++) {
        dp[i] = dp[i-1] + dp[i-2];
    }
    
    return dp[n];
}`,
        java: `public int fibonacci(int n) {
    if (n <= 1) return n;
    
    int[] dp = new int[n + 1];
    dp[0] = 0;
    dp[1] = 1;
    
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i-1] + dp[i-2];
    }
    
    return dp[n];
}`,
        cpp: `int fibonacci(int n) {
    if (n <= 1) return n;
    
    vector<int> dp(n + 1);
    dp[0] = 0;
    dp[1] = 1;
    
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i-1] + dp[i-2];
    }
    
    return dp[n];
}`,
        csharp: `public int Fibonacci(int n) {
    if (n <= 1) return n;
    
    int[] dp = new int[n + 1];
    dp[0] = 0;
    dp[1] = 1;
    
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i-1] + dp[i-2];
    }
    
    return dp[n];
}`,
        go: `func fibonacci(n int) int {
    if n <= 1 {
        return n
    }
    
    dp := make([]int, n+1)
    dp[0] = 0
    dp[1] = 1
    
    for i := 2; i <= n; i++ {
        dp[i] = dp[i-1] + dp[i-2]
    }
    
    return dp[n]
}`,
        rust: `pub fn fibonacci(n: i32) -> i32 {
    if n <= 1 {
        return n;
    }
    
    let mut dp = vec![0; (n + 1) as usize];
    dp[1] = 1;
    
    for i in 2..=n as usize {
        dp[i] = dp[i-1] + dp[i-2];
    }
    
    dp[n as usize]
}`,
        typescript: `function fibonacci(n: number): number {
    if (n <= 1) return n;
    
    const dp: number[] = new Array(n + 1);
    dp[0] = 0;
    dp[1] = 1;
    
    for (let i = 2; i <= n; i++) {
        dp[i] = dp[i-1] + dp[i-2];
    }
    
    return dp[n];
}`
      },
      general: {
        python: `def solve_problem(input_data):
    # Analyze the problem requirements
    # Choose appropriate data structures
    # Implement step by step
    
    result = []
    # Your solution logic here
    
    return result`,
        javascript: `function solveProblem(inputData) {
    // Analyze the problem requirements
    // Choose appropriate data structures
    // Implement step by step
    
    let result = [];
    // Your solution logic here
    
    return result;
}`,
        java: `public class Solution {
    public int[] solveProblem(int[] inputData) {
        // Analyze the problem requirements
        // Choose appropriate data structures
        // Implement step by step
        
        List<Integer> result = new ArrayList<>();
        // Your solution logic here
        
        return result.stream().mapToInt(i -> i).toArray();
    }
}`,
        cpp: `vector<int> solveProblem(vector<int>& inputData) {
    // Analyze the problem requirements
    // Choose appropriate data structures
    // Implement step by step
    
    vector<int> result;
    // Your solution logic here
    
    return result;
}`,
        csharp: `public int[] SolveProblem(int[] inputData) {
    // Analyze the problem requirements
    // Choose appropriate data structures
    // Implement step by step
    
    var result = new List<int>();
    // Your solution logic here
    
    return result.ToArray();
}`,
        go: `func solveProblem(inputData []int) []int {
    // Analyze the problem requirements
    // Choose appropriate data structures
    // Implement step by step
    
    result := []int{}
    // Your solution logic here
    
    return result
}`,
        rust: `pub fn solve_problem(input_data: Vec<i32>) -> Vec<i32> {
    // Analyze the problem requirements
    // Choose appropriate data structures
    // Implement step by step
    
    let mut result = Vec::new();
    // Your solution logic here
    
    result
}`,
        typescript: `function solveProblem(inputData: number[]): number[] {
    // Analyze the problem requirements
    // Choose appropriate data structures
    // Implement step by step
    
    const result: number[] = [];
    // Your solution logic here
    
    return result;
}`
      }
    };
    
    return templates[problemType] || templates.general;
  },

  getExplanation(language, problemType, algorithmType) {
    const explanations = {
      two_sum: {
        python: "Hash map approach using dictionary for O(1) lookups. Enumerate gives both index and value.",
        javascript: "Map object provides clean API for key-value storage with has() and get() methods.",
        java: "HashMap with containsKey() for existence check and put() for storage.",
        cpp: "unordered_map for hash table implementation with find() method.",
        csharp: "Dictionary<TKey, TValue> with ContainsKey() method for type-safe operations.",
        go: "Built-in map with comma ok idiom for existence checking.",
        rust: "HashMap with pattern matching using if let Some() for safe access.",
        typescript: "Typed Map with generic parameters for compile-time safety."
      },
      palindrome: {
        python: "Two-pointer technique comparing characters from both ends.",
        javascript: "Two pointers moving inward with strict equality check.",
        java: "charAt() method for character access with two-pointer approach.",
        cpp: "Direct string indexing with two pointers for efficiency.",
        csharp: "String indexing with two-pointer technique.",
        go: "Slice indexing with two pointers moving toward center.",
        rust: "Convert to char vector for safe indexing with bounds checking.",
        typescript: "Type-safe string manipulation with two-pointer technique."
      },
      general: {
        python: "General problem-solving approach with clear structure and comments.",
        javascript: "Flexible solution template adaptable to various problem types.",
        java: "Object-oriented approach with proper data structure usage.",
        cpp: "Efficient C++ implementation with STL containers.",
        csharp: "Clean C# solution using LINQ and modern language features.",
        go: "Idiomatic Go code with simple and readable structure.",
        rust: "Memory-safe Rust implementation with ownership principles.",
        typescript: "Type-safe solution with clear interfaces and error handling."
      }
    };
    
    return explanations[problemType]?.[language] || explanations.general[language];
  },

  getAlgorithmInfo(problemType, algorithmType) {
    const info = {
      two_sum: {
        type: "Array, Hash Table",
        algorithm: "Hash Map Lookup",
        timeComplexity: "O(n)",
        spaceComplexity: "O(n)",
        concept: "Instead of checking every pair (O(n²)), store complements and check existence (O(n))",
        insight: "For each number, ask 'What number would complete this pair?' then check if we've seen it.",
        keyPoints: "1. **Hash Maps are your friend** - O(1) lookup beats O(n) searching\n2. **Think backwards** - 'What do I need?' instead of 'What do I have?'\n3. **Trade space for time** - Use extra memory for faster algorithms",
        nextSteps: "- Try with different inputs: [2,7,11,15], target=9\n- Handle edge cases: duplicates, no solution, negative numbers\n- Consider follow-up: what if array is sorted?"
      },
      palindrome: {
        type: "String, Two Pointers",
        algorithm: "Two Pointer Technique",
        timeComplexity: "O(n)",
        spaceComplexity: "O(1)",
        concept: "Compare characters from both ends moving inward until pointers meet",
        insight: "If it's a palindrome, characters at symmetric positions must match",
        keyPoints: "1. **Two pointers save space** - No need to reverse or copy\n2. **Early termination** - Stop as soon as mismatch found\n3. **Symmetric comparison** - Check from outside in",
        nextSteps: "- Handle case sensitivity and special characters\n- Try with different string lengths\n- Consider Unicode and multi-byte characters"
      },
      stack: {
        type: "Stack, String",
        algorithm: "Stack-based Matching",
        timeComplexity: "O(n)",
        spaceComplexity: "O(n)",
        concept: "Use stack to track opening brackets and match with closing ones",
        insight: "Stack naturally handles nested structures - last opened must be first closed",
        keyPoints: "1. **Stack for nesting** - Perfect for matching pairs\n2. **HashMap for mapping** - Quick lookup of bracket pairs\n3. **Early termination** - Return false immediately on mismatch",
        nextSteps: "- Handle different bracket types\n- Consider edge cases: empty string, unmatched brackets\n- Optimize space with counter approach"
      },
      fibonacci: {
        type: "Dynamic Programming, Math",
        algorithm: "Bottom-up DP",
        timeComplexity: "O(n)",
        spaceComplexity: "O(n)",
        concept: "Build solution from smaller subproblems using memoization",
        insight: "Each number is sum of previous two - avoid recalculation with DP",
        keyPoints: "1. **DP optimization** - O(n) instead of O(2^n) recursive\n2. **Space optimization** - Can reduce to O(1) with variables\n3. **Base cases** - Handle n=0 and n=1 separately",
        nextSteps: "- Optimize space to O(1) using two variables\n- Try matrix exponentiation for O(log n)\n- Handle large numbers with BigInt"
      },
      general: {
        type: "General Problem",
        algorithm: "Problem-Specific Approach",
        timeComplexity: "Depends on solution",
        spaceComplexity: "Depends on solution",
        concept: "Analyze the problem, choose appropriate data structures, implement step by step",
        insight: "Break down complex problems into smaller, manageable parts",
        keyPoints: "1. **Understand the problem** - Read carefully and identify patterns\n2. **Choose right tools** - Arrays, hashmaps, trees, etc.\n3. **Start simple** - Get working solution first, optimize later",
        nextSteps: "- Test with various inputs\n- Consider edge cases\n- Optimize time/space complexity if needed"
      }
    };
    
    return info[problemType] || info.general;
  }
};