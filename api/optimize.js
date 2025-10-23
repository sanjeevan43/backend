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
          { role: 'system', content: 'You are a code optimization expert.' },
          { role: 'user', content: `Optimize this code for better performance:\n\n${code}\n\nProvide optimized version with improvements explained.` }
        ],
        max_tokens: 1500,
        temperature: 0.2
      })
    });

    const data = await response.json();
    
    res.status(200).json({
      success: true,
      optimized: data.choices[0].message.content
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}