@echo off
echo LeetCode Solver Backend Setup
echo ================================
echo.

cd /d "d:\profile\backend"

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Checking API configuration...
python setup_api.py

echo.
echo Starting Flask server...
echo API will be available at: http://localhost:5000
echo API docs at: http://localhost:5000/docs
echo.

python run_server.py