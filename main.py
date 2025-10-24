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
    session_id: str = "default"





API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

sessions = {}

@app.get("/")
async def root():
    return {"message": "LeetCode Solver API", "endpoints": ["/solve", "/history/{session_id}"]}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/solve")
async def solve_leetcode(request: LeetCodeRequest):
    if request.session_id not in sessions:
        sessions[request.session_id] = []
    
    sessions[request.session_id].append({"role": "user", "problem": request.problem})
    
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
            sessions[request.session_id].append({"role": "assistant", "solution": ai_response})
            return {"response": ai_response.strip().replace("**", "").replace("*", "")}
        else:
            return {"error": f"API Error: {response.status_code}"}
            
    except Exception as e:
        return {"error": str(e)}

@app.get("/history/{session_id}")
async def get_solution_history(session_id: str):
    if session_id in sessions:
        return {"session_id": session_id, "history": sessions[session_id]}
    return {"session_id": session_id, "history": []}

# Vercel will handle the server startup