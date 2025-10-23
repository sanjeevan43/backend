export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'POST') {
    const { problem, languages = ['python'] } = req.body;
    
    if (!problem) {
      res.status(400).json({ error: 'Problem is required' });
      return;
    }

    let solution;
    let approach;
    let complexity;
    
    if (problem.toLowerCase().includes('two sum')) {
      solution = `def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []`;
      approach = 'Hash Map - Store complements for O(1) lookup';
      complexity = 'Time: O(n), Space: O(n)';
    } else if (problem.toLowerCase().includes('palindrome')) {
      solution = `def is_palindrome(s):
    s = ''.join(c.lower() for c in s if c.isalnum())
    return s == s[::-1]`;
      approach = 'Two Pointer - Compare characters from both ends';
      complexity = 'Time: O(n), Space: O(1)';
    } else if (problem.toLowerCase().includes('fibonacci')) {
      solution = `def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b`;
      approach = 'Iterative - Build up from base cases';
      complexity = 'Time: O(n), Space: O(1)';
    } else {
      solution = `def solve():
    # Problem: ${problem}
    # Your implementation here
    pass`;
      approach = 'Analyze the problem requirements';
      complexity = 'Depends on chosen algorithm';
    }

    const response = `## Problem Analysis
${approach}

### Python
\`\`\`python
${solution}
\`\`\`

## Complexity Analysis
${complexity}`;

    res.status(200).json({ success: true, solution: response });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}