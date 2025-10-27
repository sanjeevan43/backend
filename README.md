# LeetCode Solver Backend API

Minimal Python Flask API for solving LeetCode problems with AI assistance.

## Structure

```
backend/
├── api/
│   └── index.py           # Main Flask application
├── .env                   # Environment configuration
├── requirements.txt       # Python dependencies
├── run_server.py         # Server runner
├── start_backend.bat     # Windows startup script
└── vercel.json           # Vercel deployment config
```

## Quick Start

```bash
start_backend.bat
```

Or manually:
```bash
pip install -r requirements.txt
python run_server.py
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /solve` - Solve LeetCode problems

## Configuration

Edit `.env` file:
- `GEMINI_API_KEY` - Your Gemini API key
- `PORT` - Server port (default: 5000)

## Usage

POST to `/solve` with:
```json
{
  "problem": "Your LeetCode problem description",
  "language": "python"
}
```

## Features

- AI-powered code solutions
- Multiple programming languages
- Clean, copy-paste ready code
- Error handling