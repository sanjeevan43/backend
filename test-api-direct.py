import requests
import json

def test_api():
    url = "https://backend-fl5mva3dw-sanjeevans-projects-45db636c.vercel.app/solve"
    
    test_problem = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
    
    payload = {
        "problem": test_problem,
        "language": "python"
    }
    
    try:
        print("Testing API connection...")
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Working!")
            print("Solution:", data.get('solution', 'No solution'))
        else:
            print("❌ API Error:", response.text)
            
    except Exception as e:
        print("❌ Connection Error:", str(e))

if __name__ == "__main__":
    test_api()