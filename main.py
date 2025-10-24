from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LeetCode Solving AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class LeetCodeRequest(BaseModel):
    problem: str

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

@app.get("/")
async def root():
    api_key_status = "configured" if os.getenv("GEMINI_API_KEY") else "missing"
    return {"message": "LeetCode Solver API", "endpoint": "/solve", "api_key": api_key_status}

@app.post("/solve")
async def solve_leetcode(request: LeetCodeRequest):
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        return {"error": "API key not configured"}
    
    try:
        response = requests.post(
            API_URL,
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": API_KEY,
            },
            json={
                "contents": [{
                    "parts": [{"text": f"You are a LeetCode problem solver. ONLY solve LeetCode problems. Provide: 1) Problem analysis 2) Optimal solution with code 3) Time/Space complexity. If input is not a LeetCode problem, respond 'Please provide a valid LeetCode problem to solve.' Problem: {request.problem}"}]
                }],
                "generationConfig": {"maxOutputTokens": 500}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"response": ai_response.strip().replace("**", "").replace("*", "")}
        else:
            return {"error": f"API Error: {response.status_code}"}
            
    except Exception as e:
        return {"error": str(e)}



# Export app for Vercel
handler = app