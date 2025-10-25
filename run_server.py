#!/usr/bin/env python3
"""
Simple server runner for local development
"""
import os
import sys
from api.index import app

if __name__ == "__main__":
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting LeetCode Solver API on port {port}")
    print(f"Debug mode: {debug}")
    print(f"Visit: http://localhost:{port}")
    print(f"API docs: http://localhost:{port}/docs")
    
    app.run(host='0.0.0.0', port=port, debug=debug)