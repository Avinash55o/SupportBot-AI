#!/usr/bin/env python3
"""
Test API endpoints for token functionality
"""
import requests
import json

def test_api_endpoints():
    """Test API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing API endpoints...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Server is running: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the backend server first.")
        return
    
    # Test 2: Test user login
    print("\n🔐 Testing user login...")
    login_data = {
        "email": "john@example.com",
        "password": "user123"
    }
    
    try:
        response = requests.post(f"{base_url}/user/login", json=login_data)
        if response.status_code == 200:
            login_result = response.json()
            print(f"✅ Login successful")
            print(f"   User ID: {login_result.get('user', {}).get('id')}")
            user_id = login_result.get('user', {}).get('id')
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return
    
    # Test 3: Get user tickets
    print(f"\n🎫 Testing get user tickets for user {user_id}...")
    try:
        response = requests.get(f"{base_url}/user/tickets?user_id={user_id}")
        if response.status_code == 200:
            tickets_result = response.json()
            tickets = tickets_result.get('tickets', [])
            print(f"✅ Retrieved {len(tickets)} tickets")
            
            for ticket in tickets:
                print(f"   Ticket ID: {ticket.get('id')}")
                print(f"   Token: {ticket.get('token', 'MISSING')}")
                print(f"   Issue Type: {ticket.get('issue_type')}")
                print(f"   Status: {ticket.get('status')}")
                print()
        else:
            print(f"❌ Failed to get tickets: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Get tickets error: {str(e)}")
    
    # Test 4: Test admin login
    print("\n🔐 Testing admin login...")
    admin_login_data = {
        "email": "admin@supportbot.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{base_url}/admin/login", json=admin_login_data)
        if response.status_code == 200:
            print(f"✅ Admin login successful")
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Admin login error: {str(e)}")
    
    # Test 5: Get all tickets (admin view)
    print(f"\n🎫 Testing get all tickets (admin view)...")
    try:
        response = requests.get(f"{base_url}/admin/tickets")
        if response.status_code == 200:
            tickets_result = response.json()
            tickets = tickets_result.get('tickets', [])
            print(f"✅ Retrieved {len(tickets)} tickets (admin view)")
            
            for ticket in tickets:
                print(f"   Ticket ID: {ticket.get('id')}")
                print(f"   Token: {ticket.get('token', 'MISSING')}")
                print(f"   Issue Type: {ticket.get('issue_type')}")
                print(f"   Status: {ticket.get('status')}")
                print()
        else:
            print(f"❌ Failed to get all tickets: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Get all tickets error: {str(e)}")

if __name__ == "__main__":
    test_api_endpoints()
