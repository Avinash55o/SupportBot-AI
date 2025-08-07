# Troubleshooting Guide

This guide helps you resolve common issues with the SupportBot AI system.

## 🔴 Network Error Issues

### Problem: "Network error occurred" in login form

**Symptoms:**
- Login form shows "Network error occurred" message
- Cannot connect to backend server
- Frontend cannot communicate with backend

**Solutions:**

#### 1. Check if Backend is Running

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Start the backend server
python app.py
```

**Expected Output:**
```
Starting SupportBot AI Backend on port 5000...
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

#### 2. Test Backend Connection

```bash
# Test if backend is accessible
curl http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "SupportBot AI Backend is running",
  "database": "connected"
}
```

#### 3. Check Port Availability

Make sure port 5000 is not being used by another application:

```bash
# On Windows (PowerShell):
netstat -ano | findstr :5000

# On macOS/Linux:
lsof -i :5000
```

If port 5000 is in use, you can change it in `backend/app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Change to port 5001
```

#### 4. Check CORS Configuration

If you're getting CORS errors, make sure the backend CORS configuration includes your frontend URL:

```python
# In backend/app.py
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

#### 5. Check Firewall Settings

Make sure your firewall allows connections to port 5000:

**Windows:**
1. Open Windows Defender Firewall
2. Click "Allow an app or feature through Windows Defender Firewall"
3. Add Python or your application

**macOS/Linux:**
```bash
# Check if port is blocked
sudo ufw status
# If needed, allow the port
sudo ufw allow 5000
```

### Problem: Frontend Cannot Connect to Backend

#### 1. Check API Base URL

Make sure the frontend is using the correct API base URL. Check `frontend/src/lib/api.ts`:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
```

#### 2. Check Proxy Configuration

The frontend uses a proxy configuration in `frontend/vite.config.ts`:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, ''),
    },
    '/user': {
      target: 'http://localhost:5000',
      changeOrigin: true,
    },
    '/admin': {
      target: 'http://localhost:5000',
      changeOrigin: true,
    },
  },
},
```

#### 3. Test API Endpoints

You can test the API endpoints directly:

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test login endpoint (should return 400 for missing data)
curl -X POST http://localhost:5000/user/login \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 🟡 Common Issues

### Problem: Database Connection Error

**Solution:**
1. Make sure SQLite is installed
2. Check if the database file exists: `backend/app.db`
3. Ensure the backend has write permissions to the backend directory

### Problem: AI Models Not Loading

**Solution:**
1. Install AI dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Initialize AI models:
   ```bash
   python init_ai_models.py
   ```

### Problem: Frontend Build Issues

**Solution:**
1. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Check Node.js version (requires 18+):
   ```bash
   node --version
   ```

## 🟢 Quick Fixes

### Reset Everything

If you're having persistent issues, try resetting everything:

```bash
# 1. Stop all running servers (Ctrl+C)

# 2. Clear any cached data
rm -rf backend/app.db
rm -rf backend/models/
rm -rf frontend/node_modules/.vite

# 3. Reinstall dependencies
cd backend
pip install -r requirements.txt
cd ../frontend
npm install

# 4. Start fresh
cd ../backend
python app.py
# In another terminal:
cd frontend
npm run dev
```

### Check Logs

**Backend Logs:**
- Check the terminal where you started the backend server
- Look for error messages in red

**Frontend Logs:**
- Open browser developer tools (F12)
- Check the Console tab for errors
- Check the Network tab for failed requests

## 📞 Getting Help

If you're still experiencing issues:

1. **Check the logs** - Look for specific error messages
2. **Test step by step** - Start with backend, then frontend
3. **Verify dependencies** - Make sure all packages are installed
4. **Check versions** - Ensure you're using compatible versions

### Common Error Messages

| Error | Solution |
|-------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| "Port already in use" | Change port or kill existing process |
| "CORS error" | Check CORS configuration in backend |
| "Database locked" | Restart backend server |
| "Network error" | Check if backend is running on correct port |

## 🔧 Development Tips

### Running in Development Mode

1. **Backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

### Debug Mode

Enable debug mode for more detailed error messages:

```python
# In backend/app.py
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key-here
```

---

**Note:** If you continue to experience issues, please check the logs and provide specific error messages when seeking help.
