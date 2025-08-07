@echo off
echo ========================================
echo    SupportBot AI - Chatbot System
echo ========================================
echo.

echo [1/4] Setting up backend environment...
cd backend

echo [2/4] Installing Python dependencies...
pip install -r requirements.txt

echo [3/4] Initializing AI models and database...
python setup_chatbot.py

echo [4/4] Starting backend server...
start "Backend Server" python app.py

echo.
echo ========================================
echo    Backend started successfully!
echo ========================================
echo.
echo Starting frontend...
cd ..\frontend

echo Installing frontend dependencies...
npm install

echo Starting frontend development server...
start "Frontend Server" npm run dev

echo.
echo ========================================
echo    🎉 System is ready!
echo ========================================
echo.
echo 📱 Frontend: http://localhost:8080
echo 🔧 Backend:  http://localhost:5000
echo.
echo 👤 Login Credentials:
echo    Admin: admin@supportbot.com / admin123
echo    User:  john@example.com / user123
echo.
echo 🤖 Chatbot is available in the bottom-right corner
echo    after you log in to the system.
echo.
pause
