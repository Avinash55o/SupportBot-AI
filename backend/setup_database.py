#!/usr/bin/env python3
"""
Setup script to initialize database and sample data
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

def setup_database():
    """Setup database and create sample data"""
    with app.app_context():
        print("🗄️  Setting up database...")
        
        # Create all tables
        try:
            db.create_all()
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
        
        # Check if users already exist
        existing_users = User.query.count()
        if existing_users > 0:
            print(f"⚠️  Found {existing_users} existing users. Skipping user creation.")
        else:
            print("👥 Creating sample users...")
            
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
            
            try:
                db.session.commit()
                print("✅ Sample users created successfully")
            except Exception as e:
                print(f"❌ Error creating users: {e}")
                db.session.rollback()
                return False
        
        # Check if tickets already exist
        existing_tickets = Ticket.query.count()
        if existing_tickets > 0:
            print(f"⚠️  Found {existing_tickets} existing tickets. Skipping ticket creation.")
        else:
            print("🎫 Creating sample tickets...")
            
            # Get users for ticket creation
            user1 = User.query.filter_by(email='john@example.com').first()
            user2 = User.query.filter_by(email='jane@example.com').first()
            
            if user1 and user2:
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
                ]
                
                for ticket in tickets:
                    db.session.add(ticket)
                
                try:
                    db.session.commit()
                    print("✅ Sample tickets created successfully")
                except Exception as e:
                    print(f"❌ Error creating tickets: {e}")
                    db.session.rollback()
            else:
                print("⚠️  Users not found, skipping ticket creation")
        
        print("\n🎉 Database setup completed!")
        print("\n📧 Login Credentials:")
        print("  Admin: admin@supportbot.com / admin123")
        print("  User 1: john@example.com / user123")
        print("  User 2: jane@example.com / user123")
        
        # Print verification info
        print(f"\n📋 Database Summary:")
        print(f"  Users: {User.query.count()}")
        print(f"  Tickets: {Ticket.query.count()}")
        
        return True

if __name__ == "__main__":
    success = setup_database()
    if success:
        print("\n✅ Database setup completed successfully!")
    else:
        print("\n❌ Database setup failed!")
        sys.exit(1)
