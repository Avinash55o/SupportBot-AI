#!/usr/bin/env python3
"""
Test script for chatbot functionality
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Please start the backend first.")
        return False

def test_analyze_complaint():
    """Test complaint analysis endpoint"""
    try:
        test_complaint = "I can't login to my account. It says invalid credentials and this is urgent!"
        
        response = requests.post(
            f"{BASE_URL}/api/analyze-complaint",
            json={"text": test_complaint},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Complaint analysis successful")
            print(f"   Category: {data.get('analysis', {}).get('category', 'N/A')}")
            print(f"   Priority: {data.get('analysis', {}).get('priority', 'N/A')}")
            print(f"   Response: {data.get('intelligent_response', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Complaint analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing complaint analysis: {e}")
        return False

def test_create_ticket():
    """Test ticket creation endpoint"""
    try:
        test_description = "My application is not working properly. I need immediate assistance."
        
        response = requests.post(
            f"{BASE_URL}/api/create-ticket",
            json={
                "description": test_description,
                "user_id": 1  # Assuming user ID 1 exists
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Ticket creation successful")
            print(f"   Ticket ID: {data.get('ticket', {}).get('id', 'N/A')}")
            print(f"   Category: {data.get('analysis', {}).get('category', 'N/A')}")
            print(f"   Priority: {data.get('analysis', {}).get('priority', 'N/A')}")
            return True
        else:
            print(f"❌ Ticket creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing ticket creation: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 Testing Chatbot Functionality")
    print("=" * 40)
    
    # Test 1: Backend health
    if not test_backend_health():
        return
    
    # Wait a moment for backend to fully initialize
    time.sleep(2)
    
    # Test 2: Complaint analysis
    test_analyze_complaint()
    
    # Test 3: Ticket creation
    test_create_ticket()
    
    print("\n" + "=" * 40)
    print("🎉 Chatbot testing completed!")

if __name__ == "__main__":
    main()
