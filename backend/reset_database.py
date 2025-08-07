#!/usr/bin/env python3
"""
Reset database and ensure token field is properly added
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import db
from models.user import User
from models.ticket import Ticket
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from app import app

def reset_database():
    """Reset database and create sample data with tokens"""
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("✅ Dropped all tables")
        
        # Create all tables
        db.create_all()
        print("✅ Created all tables")
        
        # Create sample users
        admin_user = User(
            name='Admin User',
            email='admin@supportbot.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin_user)
        
        user1 = User(
            name='John Doe',
            email='john@example.com',
            password_hash=generate_password_hash('user123'),
            is_admin=False
        )
        db.session.add(user1)
        
        user2 = User(
            name='Jane Smith',
            email='jane@example.com',
            password_hash=generate_password_hash('user123'),
            is_admin=False
        )
        db.session.add(user2)
        
        db.session.commit()
        print("✅ Created sample users")
        
        # Create sample tickets with tokens
        tickets = [
            Ticket(
                issue_type='Technical Support',
                description='Unable to login to my account. Getting "Invalid credentials" error.',
                status='open',
                priority='high',
                user_id=user1.id,
                notes='User reported login issues with error message',
                created_at=datetime.now() - timedelta(days=2)
            ),
            Ticket(
                issue_type='Billing',
                description='I was charged twice for my subscription this month.',
                status='in_progress',
                priority='normal',
                user_id=user1.id,
                notes='Double charge issue - investigating payment records',
                created_at=datetime.now() - timedelta(days=1)
            ),
            Ticket(
                issue_type='Feature Request',
                description='Would like to see a dark mode option in the mobile app.',
                status='open',
                priority='low',
                user_id=user2.id,
                notes='User requested dark mode feature for mobile app',
                created_at=datetime.now() - timedelta(hours=6)
            ),
        ]
        
        for ticket in tickets:
            db.session.add(ticket)
        
        db.session.commit()
        print("✅ Created sample tickets with tokens")
        
        # Verify tokens were generated
        all_tickets = Ticket.query.all()
        print(f"\n📋 Sample tickets created:")
        for ticket in all_tickets:
            print(f"   ID: {ticket.id}, Token: {ticket.token}, Issue: {ticket.issue_type}")
        
        print(f"\n✅ Database reset completed successfully!")
        print(f"   Users: {User.query.count()}")
        print(f"   Tickets: {Ticket.query.count()}")

if __name__ == "__main__":
    reset_database()
