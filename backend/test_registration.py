#!/usr/bin/env python3
"""
Test user registration and tickets API
"""
import requests
import json

def test_registration_and_tickets():
    """Test user registration and tickets API"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing user registration and tickets...")
    
    # Test 1: Register a new user
    print("\n👤 Testing user registration...")
    register_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{base_url}/user/register", json=register_data)
        if response.status_code == 201:
            register_result = response.json()
            print(f"✅ Registration successful")
            print(f"   User ID: {register_result.get('user_id')}")
            user_id = register_result.get('user_id')
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        return
    
    # Test 2: Login with the new user
    print(f"\n🔐 Testing login with new user...")
    login_data = {
        "email": "test@example.com",
        "password": "test123"
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
    
    # Test 3: Create a ticket through the chatbot API
    print(f"\n🎫 Testing ticket creation...")
    ticket_data = {
        "description": "This is a test ticket to verify token generation",
        "user_id": user_id
    }
    
    try:
        response = requests.post(f"{base_url}/api/create-ticket", json=ticket_data)
        if response.status_code == 200:
            ticket_result = response.json()
            print(f"✅ Ticket creation successful")
            ticket = ticket_result.get('ticket', {})
            print(f"   Ticket ID: {ticket.get('id')}")
            print(f"   Token: {ticket.get('token', 'MISSING')}")
            print(f"   Issue Type: {ticket.get('issue_type')}")
            print(f"   Status: {ticket.get('status')}")
        else:
            print(f"❌ Ticket creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Ticket creation error: {str(e)}")
    
    # Test 4: Get user tickets
    print(f"\n🎫 Testing get user tickets...")
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

if __name__ == "__main__":
    test_registration_and_tickets()
