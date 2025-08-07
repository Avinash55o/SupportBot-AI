#!/usr/bin/env python3
"""
Test script to verify frontend-backend integration
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:8080"

def test_backend_health():
    """Test if backend is running and responding"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"❌ Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend is not accessible: {e}")
        return False

def test_frontend_health():
    """Test if frontend is running and responding"""
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running and accessible")
            return True
        else:
            print(f"❌ Frontend responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend is not accessible: {e}")
        return False

def test_api_endpoints():
    """Test basic API endpoints"""
    endpoints = [
        ("/user/register", "POST"),
        ("/user/login", "POST"),
        ("/admin/login", "POST"),
    ]
    
    for endpoint, method in endpoints:
        try:
            if method == "POST":
                response = requests.post(
                    f"{BACKEND_URL}{endpoint}",
                    json={"test": "data"},
                    timeout=5
                )
            else:
                response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=5)
            
            # We expect 400 for invalid data, but endpoint should be reachable
            if response.status_code in [200, 400, 401]:
                print(f"✅ {method} {endpoint} - Endpoint accessible")
            else:
                print(f"❌ {method} {endpoint} - Unexpected status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {method} {endpoint} - Error: {e}")

def main():
    """Run all integration tests"""
    print("🚀 Testing SupportBot AI Integration")
    print("=" * 50)
    
    # Test backend health
    backend_ok = test_backend_health()
    
    # Test frontend health
    frontend_ok = test_frontend_health()
    
    # Test API endpoints if backend is running
    if backend_ok:
        print("\n🔍 Testing API Endpoints:")
        test_api_endpoints()
    
    print("\n" + "=" * 50)
    if backend_ok and frontend_ok:
        print("🎉 Integration test passed! Both frontend and backend are running.")
        print(f"📱 Frontend: {FRONTEND_URL}")
        print(f"🔧 Backend API: {BACKEND_URL}")
    else:
        print("❌ Integration test failed. Please check the services.")
        if not backend_ok:
            print("💡 Make sure to start the backend: cd backend && python app.py")
        if not frontend_ok:
            print("💡 Make sure to start the frontend: cd frontend && npm run dev")

if __name__ == "__main__":
    main()
