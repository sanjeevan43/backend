#!/usr/bin/env python3
import requests
import json

def test_backend():
    base_url = "http://localhost:5000"
    
    print("Testing LeetCode AI Solver Backend...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test root endpoint
    try:
        response = requests.get(base_url)
        print(f"Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Root endpoint failed: {e}")
    
    # Test solve endpoint
    try:
        test_problem = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
        payload = {
            "problem": test_problem,
            "language": "python"
        }
        
        response = requests.post(f"{base_url}/solve", 
                               headers={"Content-Type": "application/json"},
                               json=payload)
        
        print(f"Solve endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Solution preview: {data.get('solution', '')[:100]}...")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Solve endpoint failed: {e}")

if __name__ == "__main__":
    test_backend()