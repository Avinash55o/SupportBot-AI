#!/usr/bin/env python3
"""
Test script to verify backend connection and basic functionality
"""

import requests
import json
import sys

def test_backend_connection():
    """Test if the backend is running and accessible"""
    base_url = "http://localhost:5000"
    
    print(" Testing backend connection...")
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print(" Health check passed")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
        else:
            print(f" Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(" Could not connect to backend server")
        print("   Make sure the backend is running on http://localhost:5000")
        return False
    except requests.exceptions.Timeout:
        print(" Backend connection timeout")
        return False
    except Exception as e:
        print(f" Health check error: {str(e)}")
        return False
    
    # Test 2: Root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint accessible")
        else:
            print(f"❌ Root endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {str(e)}")
    
    # Test 3: User registration endpoint (should return 400 for missing data)
    try:
        response = requests.post(f"{base_url}/user/register", 
                               json={}, 
                               headers={'Content-Type': 'application/json'},
                               timeout=5)
        if response.status_code == 400:
            print("✅ User registration endpoint accessible")
        else:
            print(f"⚠️  User registration endpoint returned unexpected status {response.status_code}")
    except Exception as e:
        print(f"❌ User registration endpoint error: {str(e)}")
    
    # Test 4: User login endpoint (should return 400 for missing data)
    try:
        response = requests.post(f"{base_url}/user/login", 
                               json={}, 
                               headers={'Content-Type': 'application/json'},
                               timeout=5)
        if response.status_code == 400:
            print("✅ User login endpoint accessible")
        else:
            print(f"⚠️  User login endpoint returned unexpected status {response.status_code}")
    except Exception as e:
        print(f"❌ User login endpoint error: {str(e)}")
    
    print("\n🎉 Backend connection test completed!")
    return True

if __name__ == "__main__":
    success = test_backend_connection()
    sys.exit(0 if success else 1)
