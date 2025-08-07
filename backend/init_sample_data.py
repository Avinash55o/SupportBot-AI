#!/usr/bin/env python3
"""
Initialize sample data for testing the frontend-backend integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db
from models.user import User
from models.ticket import Ticket
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def create_sample_data():
    """Create sample users and tickets for testing"""
    with app.app_context():
        # Drop and recreate all tables to ensure clean state
        print("🗑️  Dropping existing tables...")
        db.drop_all()
        
        print("🏗️  Creating new tables...")
        db.create_all()
        
        print("✅ Database schema created")
        
        # Create admin user
        admin_user = User(
            name='Admin User',
            email='admin@supportbot.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin_user)
        
        # Create regular users
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
        print("✅ Created users")
        
        # Create sample tickets
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
            Ticket(
                issue_type='Bug Report',
                description='The search function is not working properly on the dashboard.',
                status='resolved',
                priority='high',
                user_id=user2.id,
                notes='Search functionality fixed in latest update',
                created_at=datetime.now() - timedelta(days=3)
            ),
            Ticket(
                issue_type='Account Management',
                description='Need to update my email address and phone number.',
                status='closed',
                priority='normal',
                user_id=user1.id,
                notes='Account details updated successfully',
                created_at=datetime.now() - timedelta(days=5)
            ),
        ]
        
        for ticket in tickets:
            db.session.add(ticket)
        
        db.session.commit()
        print("✅ Created sample tickets")
        
        print("\n🎉 Sample data created successfully!")
        print("\n📧 Login Credentials:")
        print("  Admin: admin@supportbot.com / admin123")
        print("  User 1: john@example.com / user123")
        print("  User 2: jane@example.com / user123")
        print(f"\n📊 Created {len(tickets)} tickets for testing")
        
        # Print some verification info
        print(f"\n📋 Database Summary:")
        print(f"  Users: {User.query.count()}")
        print(f"  Tickets: {Ticket.query.count()}")
        print(f"  Open tickets: {Ticket.query.filter_by(status='open').count()}")
        print(f"  High priority tickets: {Ticket.query.filter_by(priority='high').count()}")

if __name__ == "__main__":
    create_sample_data()