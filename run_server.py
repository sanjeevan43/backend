import os
from api.index import app

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    print(f"Starting API on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)