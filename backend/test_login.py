#!/usr/bin/env python3
"""
Test script to verify login functionality and sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db
from models.user import User
from werkzeug.security import check_password_hash

def test_login():
    """Test login functionality"""
    with app.app_context():
        print("🔍 Testing login functionality...")
        
        # Check if users exist
        users = User.query.all()
        print(f"Found {len(users)} users in database")
        
        for user in users:
            print(f"  - {user.email} (ID: {user.id}, Admin: {user.is_admin})")
        
        # Test specific user login
        test_email = 'john@example.com'
        test_password = 'user123'
        
        user = User.query.filter_by(email=test_email).first()
        if user:
            print(f"\n✅ Found user: {user.name} ({user.email})")
            
            # Test password
            if check_password_hash(user.password_hash, test_password):
                print("✅ Password check passed")
            else:
                print("❌ Password check failed")
                print(f"  Password hash: {user.password_hash}")
        else:
            print(f"❌ User {test_email} not found")
            print("  Run 'python init_sample_data.py' to create sample users")
        
        # Test admin user
        admin_email = 'admin@supportbot.com'
        admin_password = 'admin123'
        
        admin_user = User.query.filter_by(email=admin_email).first()
        if admin_user:
            print(f"\n✅ Found admin user: {admin_user.name} ({admin_user.email})")
            
            if check_password_hash(admin_user.password_hash, admin_password):
                print("✅ Admin password check passed")
            else:
                print("❌ Admin password check failed")
        else:
            print(f"❌ Admin user {admin_email} not found")

if __name__ == "__main__":
    test_login()
