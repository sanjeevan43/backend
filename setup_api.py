#!/usr/bin/env python3
"""
Setup script to configure the API with proper API key
"""
import os
import sys

def setup_api_key():
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    
    print("LeetCode Solver API Setup")
    print("=" * 40)
    print()
    print("To use the full AI-powered features, you need a Gemini API key.")
    print("Get one free at: https://makersuite.google.com/app/apikey")
    print()
    print("Without an API key, the system will use built-in fallback solutions")
    print("for common LeetCode problems (Two Sum, Palindrome, etc.)")
    print()
    
    api_key = input("Enter your Gemini API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Read current .env file
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Replace the API key line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('GEMINI_API_KEY='):
                lines[i] = f'GEMINI_API_KEY={api_key}'
                break
        
        # Write back to .env file
        with open(env_file, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ API key configured successfully!")
    else:
        print("⚠️  No API key provided. Using fallback solutions only.")
    
    print()
    print("Setup complete! Run 'python run_server.py' to start the API.")

if __name__ == "__main__":
    setup_api_key()