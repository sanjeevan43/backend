export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'POST') {
    const { code, error } = req.body;
    
    if (!code) {
      res.status(400).json({ error: 'Code is required' });
      return;
    }

    let debug_info;
    
    if (error && error.includes('IndexError')) {
      debug_info = `## Debug Analysis

**Error**: IndexError - list index out of range

**Common Causes**:
1. Accessing array beyond its length
2. Empty array access
3. Off-by-one errors in loops

**Fixed Code**:
\`\`\`python
# Add bounds checking
if i < len(array) and array[i]:
    # Safe to access array[i]
    pass
\`\`\`

**Prevention**:
- Always check array bounds
- Use len() function
- Handle empty arrays`;
    } else if (error && error.includes('KeyError')) {
      debug_info = `## Debug Analysis

**Error**: KeyError - key not found in dictionary

**Common Causes**:
1. Accessing non-existent dictionary key
2. Typo in key name
3. Key not initialized

**Fixed Code**:
\`\`\`python
# Use get() method with default
value = dict.get(key, default_value)

# Or check if key exists
if key in dict:
    value = dict[key]
\`\`\`

**Prevention**:
- Use dict.get() method
- Check key existence first
- Initialize all required keys`;
    } else {
      debug_info = `## Debug Analysis

**Code Review**:
Your code structure looks good. Here are common debugging tips:

1. **Add print statements** to trace execution
2. **Check variable types** using type()
3. **Validate inputs** before processing
4. **Handle edge cases** (empty inputs, None values)
5. **Use try-catch** for error handling

**General Debugging Steps**:
- Identify the exact line causing issues
- Check variable values at each step
- Test with simple inputs first
- Add proper error handling`;
    }

    res.status(200).json({ success: true, debug_info });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}