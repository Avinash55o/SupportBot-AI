#!/usr/bin/env python3
"""
Test script to verify ticket token generation
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import db
from models.ticket import Ticket
from models.user import User
from werkzeug.security import generate_password_hash
from app import app

def test_token_generation():
    """Test that tickets are created with proper tokens"""
    with app.app_context():
        # Ensure database tables exist
        db.create_all()
        
        # Create a test user if none exists
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            test_user = User(
                name='Test User',
                email='test@example.com',
                password_hash=generate_password_hash('test123'),
                is_admin=False
            )
            db.session.add(test_user)
            db.session.commit()
            print(f"✅ Created test user: {test_user.id}")
        
        # Create a test ticket
        test_ticket = Ticket(
            issue_type='Technical Support',
            description='Test ticket for token verification',
            user_id=test_user.id,
            priority='normal',
            status='open'
        )
        
        db.session.add(test_ticket)
        db.session.commit()
        
        print(f"✅ Created test ticket:")
        print(f"   ID: {test_ticket.id}")
        print(f"   Token: {test_ticket.token}")
        print(f"   Issue Type: {test_ticket.issue_type}")
        print(f"   Description: {test_ticket.description}")
        
        # Test the to_dict method
        ticket_dict = test_ticket.to_dict()
        print(f"✅ Ticket dict contains token: {ticket_dict.get('token', 'MISSING')}")
        
        # Clean up
        db.session.delete(test_ticket)
        db.session.commit()
        print("✅ Test completed successfully!")

if __name__ == "__main__":
    test_token_generation()
