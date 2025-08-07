#!/usr/bin/env python3
"""
Startup script for SupportBot AI Backend
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask',
        'flask-cors',
        'flask-sqlalchemy',
        'python-dotenv',
        'PyJWT',
        'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_database():
    """Check if database exists and is accessible"""
    db_path = Path("backend/app.db")
    if not db_path.exists():
        print("⚠️  Database not found. It will be created automatically.")
    else:
        print("✅ Database found")
    return True

def start_backend():
    """Start the backend server"""
    print("🚀 Starting SupportBot AI Backend...")
    
    # Change to backend directory
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    os.chdir(backend_dir)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Virtual environment not detected. Make sure to activate it first.")
        print("   On Windows: venv\\Scripts\\activate")
        print("   On macOS/Linux: source venv/bin/activate")
    
    # Start the Flask application
    try:
        print("📡 Starting Flask server on http://localhost:5000...")
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start backend server: {e}")
        return False
    except FileNotFoundError:
        print("❌ app.py not found in backend directory")
        return False
    
    return True

def test_connection():
    """Test if the backend is accessible"""
    print("🔍 Testing backend connection...")
    
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is running and accessible!")
                return True
            else:
                print(f"⚠️  Backend responded with status {response.status_code}")
        except requests.exceptions.ConnectionError:
            if i < max_retries - 1:
                print(f"⏳ Waiting for backend to start... (attempt {i+1}/{max_retries})")
                time.sleep(2)
            else:
                print("❌ Could not connect to backend server")
                return False
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    return False

def main():
    """Main function"""
    print("🤖 SupportBot AI Backend Startup")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Check database
    if not check_database():
        return 1
    
    # Start backend
    if not start_backend():
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
