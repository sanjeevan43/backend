@echo off
echo Starting LeetCode Solver Backend...
echo.

cd /d "d:\profile\backend"

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask server...
echo API will be available at: http://localhost:5000
echo API docs at: http://localhost:5000/docs
echo.

python run_server.py