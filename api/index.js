export default function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'GET') {
    res.status(200).json({ message: 'LeetCode AI is running' });
    return;
  }

  if (req.method === 'POST') {
    try {
      const { problem } = req.body;
      
      if (!problem) {
        res.status(400).json({ error: 'Problem is required' });
        return;
      }

      let solution;
      
      if (problem.toLowerCase().includes('two sum')) {
        solution = `def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []`;
      } else if (problem.toLowerCase().includes('palindrome')) {
        solution = `def is_palindrome(s):
    s = ''.join(c.lower() for c in s if c.isalnum())
    return s == s[::-1]`;
      } else {
        solution = `def solve():
    # Problem: ${problem}
    # Your solution here
    pass`;
      }

      res.status(200).json({
        success: true,
        solution: solution
      });
    } catch (error) {
      res.status(500).json({ error: 'Invalid request' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}