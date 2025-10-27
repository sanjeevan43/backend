import requests
import json

def test_api():
    base_url = "http://localhost:5000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test solve endpoint
    test_problem = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
    
    payload = {
        "problem": test_problem,
        "language": "python"
    }
    
    try:
        response = requests.post(f"{base_url}/solve", json=payload)
        print(f"Solve API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Solution:", data.get('solution', 'No solution')[:100] + "...")
        else:
            print("Error:", response.json())
    except Exception as e:
        print(f"Solve API failed: {e}")

if __name__ == "__main__":
    test_api()