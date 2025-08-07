#!/usr/bin/env python3
"""
Setup demo data for the SupportBot AI system
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def setup_demo_data():
    """Setup comprehensive demo data"""
    try:
        # Import after adding path
        from models import db
        from models.user import User
        from models.ticket import Ticket
        from app import app
        
        with app.app_context():
            print("🚀 Setting up demo data for SupportBot AI...")
            
            # Drop all tables and recreate
            db.drop_all()
            print("✅ Dropped existing tables")
            
            # Create all tables with proper schema
            db.create_all()
            print("✅ Created tables with proper schema")
            
            # Create demo users
            print("\n👥 Creating demo users...")
            
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
            
            user3 = User(
                name='Mike Johnson',
                email='mike@example.com',
                password_hash=generate_password_hash('user123'),
                is_admin=False
            )
            db.session.add(user3)
            
            db.session.commit()
            print("✅ Created demo users")
            
            # Create demo tickets with various scenarios
            print("\n🎫 Creating demo tickets...")
            
            tickets = [
                # High priority technical issues
                Ticket(
                    issue_type='Technical Support',
                    description='Unable to login to my account. Getting "Invalid credentials" error every time I try to access the dashboard.',
                    status='open',
                    priority='high',
                    user_id=user1.id,
                    notes='User reported persistent login issues with error message',
                    created_at=datetime.now() - timedelta(days=2, hours=3)
                ),
                Ticket(
                    issue_type='System Error',
                    description='The application crashes when I try to upload files larger than 10MB. This is urgent as I need to submit my report today.',
                    status='in_progress',
                    priority='urgent',
                    user_id=user2.id,
                    notes='File upload crash issue - investigating memory allocation',
                    created_at=datetime.now() - timedelta(days=1, hours=5)
                ),
                
                # Billing and payment issues
                Ticket(
                    issue_type='Billing',
                    description='I was charged twice for my subscription this month. Please refund the duplicate charge.',
                    status='in_progress',
                    priority='normal',
                    user_id=user1.id,
                    notes='Double charge issue - investigating payment records',
                    created_at=datetime.now() - timedelta(days=1, hours=2)
                ),
                Ticket(
                    issue_type='Payment Processing',
                    description='My payment method was declined but I have sufficient funds. Please help me update my payment information.',
                    status='open',
                    priority='high',
                    user_id=user3.id,
                    notes='Payment method update required',
                    created_at=datetime.now() - timedelta(hours=8)
                ),
                
                # Feature requests
                Ticket(
                    issue_type='Feature Request',
                    description='Would like to see a dark mode option in the mobile app. This would be very helpful for night-time usage.',
                    status='open',
                    priority='low',
                    user_id=user2.id,
                    notes='User requested dark mode feature for mobile app',
                    created_at=datetime.now() - timedelta(hours=6)
                ),
                Ticket(
                    issue_type='Feature Request',
                    description='Please add the ability to export data to Excel format. Currently only CSV export is available.',
                    status='open',
                    priority='normal',
                    user_id=user1.id,
                    notes='Excel export functionality requested',
                    created_at=datetime.now() - timedelta(hours=4)
                ),
                
                # Resolved tickets
                Ticket(
                    issue_type='Bug Report',
                    description='The search function is not working properly on the dashboard. It returns no results even for simple queries.',
                    status='resolved',
                    priority='high',
                    user_id=user2.id,
                    notes='Search functionality fixed in latest update v2.1.3',
                    created_at=datetime.now() - timedelta(days=3)
                ),
                Ticket(
                    issue_type='Account Management',
                    description='Need to update my email address and phone number in my profile.',
                    status='closed',
                    priority='normal',
                    user_id=user1.id,
                    notes='Account details updated successfully',
                    created_at=datetime.now() - timedelta(days=5)
                ),
                
                # Recent tickets
                Ticket(
                    issue_type='Performance Issue',
                    description='The application is running very slowly today. Pages take 10-15 seconds to load.',
                    status='open',
                    priority='high',
                    user_id=user3.id,
                    notes='Performance degradation reported - monitoring server load',
                    created_at=datetime.now() - timedelta(hours=2)
                ),
                Ticket(
                    issue_type='UI/UX Issue',
                    description='The mobile app interface is not responsive on my iPhone. Buttons are too small to tap accurately.',
                    status='open',
                    priority='normal',
                    user_id=user2.id,
                    notes='Mobile UI responsiveness issue - iOS specific',
                    created_at=datetime.now() - timedelta(hours=1)
                ),
            ]
            
            for ticket in tickets:
                db.session.add(ticket)
            
            db.session.commit()
            print("✅ Created demo tickets with tokens")
            
            # Verify tokens were generated correctly
            all_tickets = Ticket.query.all()
            print(f"\n📋 Demo tickets created ({len(all_tickets)} total):")
            for ticket in all_tickets:
                print(f"   ID: {ticket.id:2d} | Token: {ticket.token} | Issue: {ticket.issue_type}")
                print(f"   Status: {ticket.status:12} | Priority: {ticket.priority:8} | User: {ticket.user_id}")
                print(f"   Description: {ticket.description[:60]}...")
                print()
            
            # Print summary statistics
            print(f"\n📊 Demo Data Summary:")
            print(f"   Users: {User.query.count()}")
            print(f"   Tickets: {Ticket.query.count()}")
            print(f"   Open tickets: {Ticket.query.filter_by(status='open').count()}")
            print(f"   High priority tickets: {Ticket.query.filter_by(priority='high').count()}")
            print(f"   Urgent tickets: {Ticket.query.filter_by(priority='urgent').count()}")
            
            # Print login credentials
            print(f"\n🔐 Login Credentials:")
            print(f"   Admin: admin@supportbot.com / admin123")
            print(f"   User 1: john@example.com / user123")
            print(f"   User 2: jane@example.com / user123")
            print(f"   User 3: mike@example.com / user123")
            
            print(f"\n✅ Demo data setup completed successfully!")
            print(f"   The system is ready for testing with realistic data.")
            
    except Exception as e:
        print(f"❌ Error setting up demo data: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_demo_data()
