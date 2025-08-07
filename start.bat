@echo off
echo Starting SupportBot AI...
echo.

echo Installing dependencies...
npm install
cd frontend && npm install && cd ..

echo.
echo Starting backend and frontend...
echo Backend will be available at: http://localhost:5000
echo Frontend will be available at: http://localhost:8080
echo.

npm run dev
