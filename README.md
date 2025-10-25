# LeetCode Solver Backend API

Complete Python Flask API for solving LeetCode problems with AI assistance.

## Structure

```
backend/
├── api/
│   ├── index.py           # Main Flask application
│   ├── fallback.py        # Fallback solutions for common problems
│   └── extended_fallback.py # Extended problem solutions
├── .env                   # Environment configuration
├── requirements.txt       # Python dependencies
├── run_server.py         # Server runner
├── start_backend.bat     # Windows startup script
├── test_api.py           # API testing script
└── test-api-direct.py    # Direct API testing
```

## Quick Start

### Option 1: Use batch file
```bash
start_backend.bat
```

### Option 2: Manual start
```bash
cd backend
pip install -r requirements.txt
python run_server.py
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Interactive documentation
- `POST /solve` - Solve LeetCode problems

## Configuration

Edit `.env` file to configure:
- `GEMINI_API_KEY` - Your Gemini API key
- `PORT` - Server port (default: 5000)
- `API_TIMEOUT` - Request timeout
- `MAX_OUTPUT_TOKENS` - AI response limit

## Testing

```bash
python test_api.py
```

## Supported Problems

The API can solve 15+ common LeetCode problem types including:
- Two Sum, Three Sum
- Maximum Subarray (Kadane's Algorithm)
- Binary Search, Merge Sorted Arrays
- Valid Parentheses, Palindrome Check
- Climbing Stairs, Stock Problems
- Container With Most Water
- And many more...

## Features

- Complete working code solutions
- Proper time/space complexity analysis
- Fallback solutions when API fails
- Multiple programming language support
- Production-ready error handling