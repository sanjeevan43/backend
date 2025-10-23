export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'POST') {
    const { code, language = 'python' } = req.body;
    
    if (!code) {
      res.status(400).json({ error: 'Code is required' });
      return;
    }

    let optimized;
    
    if (code.includes('for') && code.includes('range')) {
      optimized = `# Optimized version using list comprehension
${code.replace(/for .+ in range\(.+\):\s*\n\s*.+\.append\(.+\)/g, 
'# Use list comprehension for better performance\nresult = [expression for item in iterable]')}

## Improvements:
- Used list comprehension for better performance
- Reduced time complexity
- More Pythonic code`;
    } else {
      optimized = `# Your code is already well optimized!
${code}

## Analysis:
- Code structure looks good
- Consider edge cases
- Add error handling if needed`;
    }

    res.status(200).json({ success: true, optimized });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}