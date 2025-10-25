#!/usr/bin/env python3
"""
Simple test script to verify API functionality
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_root():
    """Test root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return False

def test_solve():
    """Test solve endpoint"""
    test_problem = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
    
    try:
        response = requests.post(
            f"{BASE_URL}/solve",
            json={"problem": test_problem, "language": "python"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Solve endpoint: {response.status_code}")
        result = response.json()
        print(f"Status: {result.get('status', 'unknown')}")
        if 'solution' in result:
            print("Solution received successfully")
        else:
            print(f"Error: {result.get('error', 'unknown error')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Solve endpoint failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Solve Endpoint", test_solve)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{test_name}: {status}")