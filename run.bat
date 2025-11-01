@echo off
echo Starting Google Maps Lead Generator...
echo.

if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and add your BROWSER_USE_API_KEY
    pause
    exit
)

python app.py
