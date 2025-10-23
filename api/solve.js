export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-cache');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { problem, language = 'python' } = req.body;
  
  if (!problem) {
    res.status(400).json({ error: 'Problem required' });
    return;
  }

  try {
    const prompt = `You are an expert LeetCode problem solver. Solve this problem optimally:

${problem}

Provide:
1. Complete working ${language} solution
2. Time & Space complexity
3. Brief explanation
4. Handle edge cases

Format: Clean code with comments.`;

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: 'gpt-4o-mini',
        messages: [
          { role: 'system', content: 'You are a LeetCode expert who provides optimal solutions with clear explanations.' },
          { role: 'user', content: prompt }
        ],
        max_tokens: 2000,
        temperature: 0.3,
        stream: false
      })
    });

    if (!response.ok) {
      throw new Error(`OpenAI API error: ${response.status}`);
    }

    const data = await response.json();
    
    res.status(200).json({
      success: true,
      solution: data.choices[0].message.content,
      language,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('API Error:', error);
    res.status(500).json({ 
      error: 'Failed to solve problem',
      details: error.message 
    });
  }
}