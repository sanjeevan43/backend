import requests
import os

API_KEY = "AIzaSyBd2jvMtrY4izfOfXD3NZReZtPUtyGQzU4"

def test_gemini():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Write a simple Python function to add two numbers"}]
        }]
    }
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_gemini()