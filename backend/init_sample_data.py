#!/usr/bin/env python3
"""
Initialize database with sample data
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def init_sample_data():
    """Initialize database with sample data"""
    try:
        # Import after adding path
        from models import db
        from models.user import User
        from models.ticket import Ticket
        from app import app
        
        with app.app_context():
            print("🔧 Initializing database with sample data...")
            
            # Check if data already exists
            existing_users = User.query.count()
            existing_tickets = Ticket.query.count()
            
            if existing_users > 0:
                print(f"✅ Database already has {existing_users} users and {existing_tickets} tickets")
                return
            
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
            
            print(f"\n✅ Database initialization completed successfully!")
            print(f"   Users: {User.query.count()}")
            print(f"   Tickets: {Ticket.query.count()}")
            
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_sample_data()