export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { code } = req.body;
  
  if (!code) {
    res.status(400).json({ error: 'Code required' });
    return;
  }

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: 'gpt-4o-mini',
        messages: [
          { role: 'system', content: 'You are a code explanation expert.' },
          { role: 'user', content: `Explain this code step by step:\n\n${code}\n\nInclude algorithm, complexity, and key insights.` }
        ],
        max_tokens: 1200,
        temperature: 0.3
      })
    });

    const data = await response.json();
    
    res.status(200).json({
      success: true,
      explanation: data.choices[0].message.content
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}