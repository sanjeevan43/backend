export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'POST') {
    const { code } = req.body;
    
    if (!code) {
      res.status(400).json({ error: 'Code is required' });
      return;
    }

    let explanation;
    
    if (code.includes('two_sum')) {
      explanation = `## Code Explanation

This is a Two Sum solution using hash map approach:

1. **Initialize hash map**: Store numbers we've seen
2. **Calculate complement**: For each number, find what we need to reach target
3. **Check if complement exists**: If yes, return indices
4. **Store current number**: Add to hash map for future lookups

## Time Complexity: O(n)
## Space Complexity: O(n)

The hash map provides O(1) lookup time, making this efficient.`;
    } else if (code.includes('palindrome')) {
      explanation = `## Code Explanation

This checks if a string is a palindrome:

1. **Clean the string**: Remove non-alphanumeric characters
2. **Convert to lowercase**: For case-insensitive comparison
3. **Compare with reverse**: Check if string equals its reverse

## Time Complexity: O(n)
## Space Complexity: O(n) for the cleaned string

Alternative: Use two pointers for O(1) space complexity.`;
    } else {
      explanation = `## Code Explanation

Your code structure:

1. **Function definition**: Defines the main logic
2. **Input processing**: Handles the input parameters
3. **Core algorithm**: Implements the solution logic
4. **Return result**: Outputs the final answer

## Analysis:
- Review the algorithm complexity
- Consider edge cases
- Add input validation if needed`;
    }

    res.status(200).json({ success: true, explanation });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}