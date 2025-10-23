export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  if (req.method === 'GET') {
    res.status(200).json({ 
      message: 'LeetCode AI Solver API',
      status: 'running'
    });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}