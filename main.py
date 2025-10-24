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

class MessageRequest(BaseModel):
    message: str
    session_id: str = "default"





API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

sessions = {}

@app.get("/")
async def root():
    return {"message": "LeetCode Solving AI is running", "endpoints": ["/chat", "/chat/{session_id}"]}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(request: MessageRequest):
    if request.session_id not in sessions:
        sessions[request.session_id] = []
    
    sessions[request.session_id].append({"role": "user", "message": request.message})
    
    try:
        response = requests.post(
            API_URL,
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": API_KEY,
            },
            json={
                "contents": [{
                    "parts": [{"text": f"You are a LeetCode problem-solving AI assistant. Help users solve coding problems by providing clear explanations, optimal solutions, and step-by-step approaches. Focus on algorithms, data structures, and coding best practices. If the question is not coding-related, respond with 'I can only help with coding and algorithm problems.' Previous conversation: {sessions[request.session_id][-10:] if len(sessions[request.session_id]) > 1 else []}. Current question: {request.message}"}]
                }],
                "generationConfig": {"maxOutputTokens": 100}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data["candidates"][0]["content"]["parts"][0]["text"]
            sessions[request.session_id].append({"role": "assistant", "message": ai_response})
            return {"response": ai_response.strip().replace("**", "").replace("*", "")}
        else:
            return {"error": f"API Error: {response.status_code}"}
            
    except Exception as e:
        return {"error": str(e)}

@app.get("/chat/{session_id}")
async def get_chat_history(session_id: str):
    if session_id in sessions:
        return {"session_id": session_id, "history": sessions[session_id]}
    return {"session_id": session_id, "history": []}

# Vercel will handle the server startup