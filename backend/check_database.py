#!/usr/bin/env python3
"""
Check database for tickets and tokens
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import db
from models.ticket import Ticket
from models.user import User
from app import app

def check_database():
    """Check database for tickets and tokens"""
    with app.app_context():
        print("🔍 Checking database...")
        
        # Check if tables exist
        try:
            tickets = Ticket.query.all()
            users = User.query.all()
            print(f"✅ Database accessible")
            print(f"   Users: {len(users)}")
            print(f"   Tickets: {len(tickets)}")
            
            if tickets:
                print(f"\n📋 Tickets in database:")
                for ticket in tickets:
                    print(f"   ID: {ticket.id}")
                    print(f"   Token: {ticket.token}")
                    print(f"   Issue Type: {ticket.issue_type}")
                    print(f"   Description: {ticket.description[:50]}...")
                    print(f"   Status: {ticket.status}")
                    print(f"   Priority: {ticket.priority}")
                    print(f"   User ID: {ticket.user_id}")
                    print()
            else:
                print("❌ No tickets found in database")
                
                # Create a test ticket
                print("🧪 Creating a test ticket...")
                test_user = User.query.first()
                if test_user:
                    test_ticket = Ticket(
                        issue_type='Test Issue',
                        description='This is a test ticket to verify token generation',
                        user_id=test_user.id,
                        priority='normal',
                        status='open'
                    )
                    db.session.add(test_ticket)
                    db.session.commit()
                    print(f"✅ Created test ticket:")
                    print(f"   ID: {test_ticket.id}")
                    print(f"   Token: {test_ticket.token}")
                else:
                    print("❌ No users found to create test ticket")
                    
        except Exception as e:
            print(f"❌ Database error: {str(e)}")

if __name__ == "__main__":
    check_database()
