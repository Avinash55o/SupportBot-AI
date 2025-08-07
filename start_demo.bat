@echo off
echo 🚀 SupportBot AI - Starting Demo with Dummy Data
echo ================================================

cd /d "%~dp0"

echo Starting backend server...
cd backend
call venv\Scripts\activate
start /B python app.py

echo Waiting for server to start...
timeout /t 5 /nobreak > nul

echo Populating database with dummy data...
curl -X POST http://localhost:5000/populate-dummy-data

echo.
echo ✅ Setup complete!
echo.
echo 📋 Login Credentials:
echo.
echo 👥 Regular Users:
echo    Email: john.smith@example.com
echo    Password: password123
echo.
echo    Email: sarah.johnson@example.com
echo    Password: password123
echo.
echo    Email: mike.wilson@example.com
echo    Password: password123
echo.
echo 👨‍💼 Admin Users:
echo    Email: admin@supportbot.com
echo    Password: admin123
echo.
echo    Email: manager@supportbot.com
echo    Password: manager123
echo.
echo 🌐 Access the application at: http://localhost:8080
echo.
echo Press any key to stop the server...
pause > nul

echo Stopping server...
taskkill /f /im python.exe > nul 2>&1
echo ✅ Server stopped.
