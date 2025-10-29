import requests

API_KEY = "AIzaSyBd2jvMtrY4izfOfXD3NZReZtPUtyGQzU4"

def list_models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    list_models()