import requests
import json

BASE_URL = "https://backend-dun-ten-29.vercel.app"

def test_api():
    print("Testing LeetCode Solver API...")
    
    # Test health endpoint
    print("\n1. Testing health endpoint:")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test root endpoint
    print("\n2. Testing root endpoint:")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test solve endpoint
    print("\n3. Testing solve endpoint:")
    test_problem = """
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    You may assume that each input would have exactly one solution, and you may not use the same element twice.
    """
    
    payload = {
        "problem": test_problem,
        "language": "python"
    }
    
    response = requests.post(f"{BASE_URL}/solve", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_api()