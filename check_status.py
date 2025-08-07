#!/usr/bin/env python3
"""
Script to check the status of backend and frontend servers
"""

import requests
import time
import subprocess
import sys
import os

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running at http://localhost:5000")
            return True
        else:
            print("❌ Backend responded with error status")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running (connection refused)")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False

def check_frontend():
    """Check if frontend is running"""
    try:
        response = requests.get('http://localhost:8080', timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running at http://localhost:8080")
            return True
        else:
            print("❌ Frontend responded with error status")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running (connection refused)")
        return False
    except Exception as e:
        print(f"❌ Error checking frontend: {e}")
        return False

def main():
    """Main function to check server status"""
    print("🔍 Checking SupportBot AI Server Status")
    print("=" * 50)
    
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    
    print("\n" + "=" * 50)
    
    if backend_ok and frontend_ok:
        print("🎉 All servers are running!")
        print("\n📋 Login Credentials:")
        print("\n👥 Regular Users:")
        print("   Email: john.smith@example.com")
        print("   Password: password123")
        print("\n   Email: sarah.johnson@example.com")
        print("   Password: password123")
        print("\n   Email: mike.wilson@example.com")
        print("   Password: password123")
        print("\n👨‍💼 Admin Users:")
        print("   Email: admin@supportbot.com")
        print("   Password: admin123")
        print("\n   Email: manager@supportbot.com")
        print("   Password: manager123")
        
        print("\n🌐 Access your application:")
        print("   Frontend: http://localhost:8080")
        print("   Backend API: http://localhost:5000")
        
        print("\n📊 Your dummy data includes:")
        print("   • 5 users (3 regular, 2 admin)")
        print("   • 15 tickets across all categories")
        print("   • Various priorities and statuses")
        
    elif backend_ok:
        print("⚠️  Backend is running but frontend is not")
        print("   Try running: npm run dev")
        
    elif frontend_ok:
        print("⚠️  Frontend is running but backend is not")
        print("   Try running: cd backend && python app.py")
        
    else:
        print("❌ Neither server is running")
        print("   Start backend: cd backend && python app.py")
        print("   Start frontend: npm run dev")

if __name__ == "__main__":
    main()
