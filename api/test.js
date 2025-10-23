export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'GET') {
    res.status(200).json({ 
      status: 'API is running!', 
      version: '1.0',
      endpoints: [
        'GET /api/test - Test endpoint',
        'POST /api/solve - Solve problems',
        'POST /api/optimize - Optimize code',
        'POST /api/explain - Explain code',
        'POST /api/debug - Debug code'
      ]
    });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}