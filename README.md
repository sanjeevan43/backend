# LeetCode AI Solver API

Fast and optimized API for solving LeetCode problems using OpenAI GPT-4.

## Endpoints

- `GET /api/` - API status and info
- `POST /api/solve` - Solve LeetCode problems
- `POST /api/optimize` - Optimize existing code
- `POST /api/explain` - Explain code solutions

## Usage

```javascript
// Solve a problem
fetch('/api/solve', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    problem: "Two Sum problem description...",
    language: "python"
  })
})

// Optimize code
fetch('/api/optimize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: "your code here"
  })
})
```

## Features

- ⚡ Fast response times with GPT-4o-mini
- 🔧 Code optimization suggestions
- 📚 Detailed explanations
- 🌐 CORS enabled
- 🚀 Vercel serverless deployment