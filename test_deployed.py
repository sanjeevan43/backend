import requests

def test_deployed_api():
    base_url = "https://backend-md5z3cdmp-sanjeevans-projects-45db636c.vercel.app"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health status: {response.status_code}")
        if response.status_code == 200:
            print(f"Health response: {response.json()}")
        else:
            print(f"Health error: {response.text}")
    except Exception as e:
        print(f"Health failed: {e}")
    
    # Test solve endpoint
    payload = {
        "problem": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "language": "python"
    }
    
    try:
        response = requests.post(f"{base_url}/solve", json=payload, timeout=30)
        print(f"Solve status: {response.status_code}")
        if response.status_code == 200:
            print("Solve API working!")
            result = response.json()
            print(f"Solution preview: {result.get('solution', 'No solution')[:100]}...")
        else:
            print(f"Solve failed: {response.text}")
    except Exception as e:
        print(f"Solve error: {e}")

if __name__ == "__main__":
    test_deployed_api()