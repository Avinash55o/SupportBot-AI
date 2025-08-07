#!/usr/bin/env python3
"""
Script to start the backend and populate dummy data
"""

import requests
import time
import subprocess
import sys
import os

def start_backend():
    """Start the Flask backend server"""
    print("Starting SupportBot AI Backend...")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    # Start the Flask app
    try:
        # Use subprocess to start the Flask app
        process = subprocess.Popen([sys.executable, 'app.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a bit for the server to start
        print("Waiting for server to start...")
        time.sleep(5)
        
        return process
    except Exception as e:
        print(f"Error starting backend: {e}")
        return None

def populate_dummy_data():
    """Populate the database with dummy data"""
    print("Populating database with dummy data...")
    
    try:
        response = requests.post('http://localhost:5000/populate-dummy-data')
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dummy data populated successfully!")
            print("\n📋 Login Credentials:")
            print("\n👥 Regular Users:")
            for user in data['credentials']['regular_users']:
                print(f"   Email: {user['email']}")
                print(f"   Password: {user['password']}")
            
            print("\n👨‍💼 Admin Users:")
            for user in data['credentials']['admin_users']:
                print(f"   Email: {user['email']}")
                print(f"   Password: {user['password']}")
            
            print("\n🌐 Access the application at: http://localhost:8080")
            return True
        else:
            print(f"❌ Failed to populate dummy data: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server. Make sure it's running on port 5000.")
        return False
    except Exception as e:
        print(f"❌ Error populating dummy data: {e}")
        return False

def main():
    """Main function"""
    print("🚀 SupportBot AI - Starting with Dummy Data")
    print("=" * 50)
    
    # Start the backend
    process = start_backend()
    
    if process is None:
        print("❌ Failed to start backend server")
        return
    
    try:
        # Populate dummy data
        success = populate_dummy_data()
        
        if success:
            print("\n✅ Setup complete! You can now:")
            print("   1. Access the frontend at: http://localhost:8080")
            print("   2. Login with any of the credentials above")
            print("   3. View tickets in both user and admin dashboards")
            print("\n🔄 The backend server is running. Press Ctrl+C to stop.")
            
            # Keep the server running
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping server...")
                process.terminate()
                process.wait()
                print("✅ Server stopped.")
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        process.terminate()
        process.wait()
        print("✅ Server stopped.")
    except Exception as e:
        print(f"❌ Error: {e}")
        process.terminate()
        process.wait()

if __name__ == "__main__":
    main()
