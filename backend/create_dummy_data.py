#!/usr/bin/env python3
"""
Simple script to create dummy data through Flask app
"""

from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash

def create_dummy_data(app, db, User, Ticket):
    """Create dummy users and tickets"""
    
    with app.app_context():
        # Create dummy users
        users_data = [
            {'name': 'John Smith', 'email': 'john.smith@example.com', 'password': 'password123', 'is_admin': False},
            {'name': 'Sarah Johnson', 'email': 'sarah.johnson@example.com', 'password': 'password123', 'is_admin': False},
            {'name': 'Mike Wilson', 'email': 'mike.wilson@example.com', 'password': 'password123', 'is_admin': False},
            {'name': 'Admin User', 'email': 'admin@supportbot.com', 'password': 'admin123', 'is_admin': True},
            {'name': 'Support Manager', 'email': 'manager@supportbot.com', 'password': 'manager123', 'is_admin': True}
        ]
        
        users = []
        for user_data in users_data:
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                users.append(existing_user)
                continue
                
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password']),
                is_admin=user_data['is_admin']
            )
            db.session.add(user)
            users.append(user)
            print(f"Created user: {user_data['email']}")
        
        db.session.commit()
        
        # Create dummy tickets
        regular_users = [user for user in users if not user.is_admin]
        admin_users = [user for user in users if user.is_admin]
        
        tickets_data = [
            # Billing Issues
            {
                'issue_type': 'Billing Problem',
                'description': 'I was charged twice for my monthly subscription. The payment went through on both my credit card and PayPal. I need this resolved immediately as it\'s causing financial issues.',
                'priority': 'urgent',
                'status': 'open',
                'notes': 'Customer reports double billing issue. Requires immediate attention.'
            },
            {
                'issue_type': 'Payment Method Update',
                'description': 'I need to update my billing information. My credit card expired and I want to switch to a new one. Can you help me update my payment method?',
                'priority': 'normal',
                'status': 'in_progress',
                'notes': 'Customer needs to update payment method. Standard procedure.'
            },
            {
                'issue_type': 'Incorrect Charges',
                'description': 'I noticed some unexpected charges on my bill this month. There are fees that I don\'t recognize and I want to dispute them.',
                'priority': 'high',
                'status': 'open',
                'notes': 'Customer disputing charges. Requires investigation.'
            },
            
            # Technical Issues
            {
                'issue_type': 'Login Problems',
                'description': 'I can\'t log into my account. I keep getting an error message saying "Invalid credentials" even though I\'m sure my password is correct. I\'ve tried resetting it but still can\'t access my account.',
                'priority': 'urgent',
                'status': 'resolved',
                'notes': 'Password reset completed. Customer can now access account.'
            },
            {
                'issue_type': 'System Performance',
                'description': 'The website is loading very slowly today. It takes several minutes to load any page and sometimes times out completely. This is affecting my ability to work.',
                'priority': 'high',
                'status': 'in_progress',
                'notes': 'Investigating server performance issues. Monitoring system load.'
            },
            {
                'issue_type': 'Mobile App Crash',
                'description': 'The mobile app keeps crashing when I try to access the dashboard. It works fine on the website but the app is unusable. I\'m using the latest version.',
                'priority': 'normal',
                'status': 'open',
                'notes': 'Mobile app crash reported. Need to investigate app stability.'
            },
            {
                'issue_type': 'Feature Not Working',
                'description': 'The search function in the dashboard is not working properly. When I search for files, it doesn\'t return any results even though I know the files exist.',
                'priority': 'normal',
                'status': 'closed',
                'notes': 'Search functionality restored. Bug was in the indexing system.'
            },
            
            # Service Issues
            {
                'issue_type': 'Customer Service',
                'description': 'I\'ve been waiting for a response from customer service for over 3 days. I submitted a ticket but haven\'t heard back yet. This is unacceptable.',
                'priority': 'high',
                'status': 'open',
                'notes': 'Customer service delay complaint. Need to improve response times.'
            },
            {
                'issue_type': 'Service Quality',
                'description': 'The quality of service has declined significantly over the past few months. Response times are slower and the support team seems less knowledgeable.',
                'priority': 'normal',
                'status': 'in_progress',
                'notes': 'Service quality feedback. Under review by management.'
            },
            {
                'issue_type': 'Account Cancellation',
                'description': 'I want to cancel my subscription. I\'ve been a customer for 2 years but the recent changes to the service don\'t meet my needs anymore.',
                'priority': 'normal',
                'status': 'open',
                'notes': 'Subscription cancellation request. Standard retention process.'
            },
            
            # General Inquiries
            {
                'issue_type': 'Product Information',
                'description': 'I\'m interested in upgrading my current plan to the premium version. Can you provide more information about the features and pricing?',
                'priority': 'low',
                'status': 'resolved',
                'notes': 'Provided detailed information about premium features and pricing.'
            },
            {
                'issue_type': 'Feature Request',
                'description': 'I would like to suggest a new feature for the platform. It would be very helpful to have a bulk export function for reports.',
                'priority': 'low',
                'status': 'open',
                'notes': 'Feature request submitted. Will be reviewed by product team.'
            },
            {
                'issue_type': 'General Question',
                'description': 'I have a question about the data retention policy. How long do you keep user data and what happens to it when an account is deleted?',
                'priority': 'low',
                'status': 'resolved',
                'notes': 'Provided detailed information about data retention policies.'
            },
            
            # Emergency Issues
            {
                'issue_type': 'Security Breach',
                'description': 'I think my account has been compromised. I received an email about a login from an unknown location and I didn\'t make that login attempt.',
                'priority': 'urgent',
                'status': 'in_progress',
                'notes': 'Security incident reported. Immediate investigation required.'
            },
            {
                'issue_type': 'Data Loss',
                'description': 'All my data disappeared from my account. I had important files that are now gone and I need them recovered immediately.',
                'priority': 'urgent',
                'status': 'open',
                'notes': 'Critical data loss reported. Emergency recovery process initiated.'
            }
        ]
        
        base_time = datetime.now() - timedelta(days=30)
        
        for ticket_data in tickets_data:
            # Create varied timestamps
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            
            created_at = base_time + timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
            
            # Randomly assign to a regular user
            user = random.choice(regular_users)
            
            # Randomly assign to an admin (for some tickets)
            assigned_admin = random.choice(admin_users) if random.random() > 0.3 else None
            
            ticket = Ticket(
                issue_type=ticket_data['issue_type'],
                description=ticket_data['description'],
                status=ticket_data['status'],
                priority=ticket_data['priority'],
                notes=ticket_data['notes'],
                user_id=user.id,
                assigned_admin_id=assigned_admin.id if assigned_admin else None,
                created_at=created_at,
                updated_at=created_at + timedelta(hours=random.randint(1, 48)) if ticket_data['status'] != 'open' else created_at
            )
            
            db.session.add(ticket)
            print(f"Created ticket: {ticket_data['issue_type']} (Priority: {ticket_data['priority']}, Status: {ticket_data['status']})")
        
        db.session.commit()
        print(f"Created {len(tickets_data)} dummy tickets")
        
        print("\n=== Database Population Complete ===")
        print("Login Credentials:")
        print("Regular Users:")
        for user in users:
            if not user.is_admin:
                print(f"  Email: {user.email}, Password: password123")
        print("\nAdmin Users:")
        for user in users:
            if user.is_admin:
                print(f"  Email: {user.email}, Password: admin123/manager123")

if __name__ == "__main__":
    print("This script should be imported and used with the Flask app context")
