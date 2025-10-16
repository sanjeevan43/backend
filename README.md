# LeetCode AI Backend

A Flask-based API that helps solve, optimize, explain, and debug LeetCode problems using OpenAI's GPT models.

## Features

- **Solve**: Get complete solutions for LeetCode problems
- **Optimize**: Improve existing code performance
- **Explain**: Get detailed explanations of code solutions
- **Debug**: Find and fix code errors

## Setup

1. Clone the repository:
```bash
git clone https://github.com/sanjeevan43/leetcode-AI-backend.git
cd leetcode-AI-backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. Run the application:
```bash
python app.py
```

## API Endpoints

### POST /solve
Solve a LeetCode problem
```json
{
  "problem": "Two Sum problem description...",
  "language": "python"
}
```

### POST /optimize
Optimize existing code
```json
{
  "code": "your code here",
  "language": "python"
}
```

### POST /explain
Explain code solution
```json
{
  "code": "code to explain"
}
```

### POST /debug
Debug code and find errors
```json
{
  "code": "buggy code",
  "error": "error message (optional)"
}
```

### GET /test
Test if API is running

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key

## Deployment

The app runs on `http://localhost:5000` by default and is configured for production deployment.