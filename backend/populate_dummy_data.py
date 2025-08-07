#!/usr/bin/env python3
"""
Script to populate the database with dummy tickets and users for demonstration
"""

import sys
import os
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db
from models.user import User
from models.ticket import Ticket

def create_dummy_users():
    """Create dummy users for demonstration"""
    users = [
        {
            'name': 'John Smith',
            'email': 'john.smith@example.com',
            'password': 'password123',
            'is_admin': False
        },
        {
            'name': 'Sarah Johnson',
            'email': 'sarah.johnson@example.com',
            'password': 'password123',
            'is_admin': False
        },
        {
            'name': 'Mike Wilson',
            'email': 'mike.wilson@example.com',
            'password': 'password123',
            'is_admin': False
        },
        {
            'name': 'Admin User',
            'email': 'admin@supportbot.com',
            'password': 'admin123',
            'is_admin': True
        },
        {
            'name': 'Support Manager',
            'email': 'manager@supportbot.com',
            'password': 'manager123',
            'is_admin': True
        }
    ]
    
    created_users = []
    for user_data in users:
        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if existing_user:
            print(f"User {user_data['email']} already exists, skipping...")
            created_users.append(existing_user)
            continue
            
        user = User(
            name=user_data['name'],
            email=user_data['email'],
            password_hash=generate_password_hash(user_data['password']),
            is_admin=user_data['is_admin']
        )
        db.session.add(user)
        created_users.append(user)
        print(f"Created user: {user_data['email']}")
    
    db.session.commit()
    return created_users

def create_dummy_tickets(users):
    """Create dummy tickets with realistic data"""
    
    # Separate regular users and admins
    regular_users = [user for user in users if not user.is_admin]
    admin_users = [user for user in users if user.is_admin]
    
    # Sample complaint data with different categories and priorities
    complaints = [
        # Billing Issues
        {
            'issue_type': 'Billing Problem',
            'description': 'I was charged twice for my monthly subscription. The payment went through on both my credit card and PayPal. I need this resolved immediately as it\'s causing financial issues.',
            'category': 'billing',
            'priority': 'urgent',
            'status': 'open',
            'notes': 'Customer reports double billing issue. Requires immediate attention.'
        },
        {
            'issue_type': 'Payment Method Update',
            'description': 'I need to update my billing information. My credit card expired and I want to switch to a new one. Can you help me update my payment method?',
            'category': 'billing',
            'priority': 'normal',
            'status': 'in_progress',
            'notes': 'Customer needs to update payment method. Standard procedure.'
        },
        {
            'issue_type': 'Incorrect Charges',
            'description': 'I noticed some unexpected charges on my bill this month. There are fees that I don\'t recognize and I want to dispute them.',
            'category': 'billing',
            'priority': 'high',
            'status': 'open',
            'notes': 'Customer disputing charges. Requires investigation.'
        },
        
        # Technical Issues
        {
            'issue_type': 'Login Problems',
            'description': 'I can\'t log into my account. I keep getting an error message saying "Invalid credentials" even though I\'m sure my password is correct. I\'ve tried resetting it but still can\'t access my account.',
            'category': 'technical',
            'priority': 'urgent',
            'status': 'resolved',
            'notes': 'Password reset completed. Customer can now access account.'
        },
        {
            'issue_type': 'System Performance',
            'description': 'The website is loading very slowly today. It takes several minutes to load any page and sometimes times out completely. This is affecting my ability to work.',
            'category': 'technical',
            'priority': 'high',
            'status': 'in_progress',
            'notes': 'Investigating server performance issues. Monitoring system load.'
        },
        {
            'issue_type': 'Mobile App Crash',
            'description': 'The mobile app keeps crashing when I try to access the dashboard. It works fine on the website but the app is unusable. I\'m using the latest version.',
            'category': 'technical',
            'priority': 'normal',
            'status': 'open',
            'notes': 'Mobile app crash reported. Need to investigate app stability.'
        },
        {
            'issue_type': 'Feature Not Working',
            'description': 'The search function in the dashboard is not working properly. When I search for files, it doesn\'t return any results even though I know the files exist.',
            'category': 'technical',
            'priority': 'normal',
            'status': 'closed',
            'notes': 'Search functionality restored. Bug was in the indexing system.'
        },
        
        # Service Issues
        {
            'issue_type': 'Customer Service',
            'description': 'I\'ve been waiting for a response from customer service for over 3 days. I submitted a ticket but haven\'t heard back yet. This is unacceptable.',
            'category': 'service',
            'priority': 'high',
            'status': 'open',
            'notes': 'Customer service delay complaint. Need to improve response times.'
        },
        {
            'issue_type': 'Service Quality',
            'description': 'The quality of service has declined significantly over the past few months. Response times are slower and the support team seems less knowledgeable.',
            'category': 'service',
            'priority': 'normal',
            'status': 'in_progress',
            'notes': 'Service quality feedback. Under review by management.'
        },
        {
            'issue_type': 'Account Cancellation',
            'description': 'I want to cancel my subscription. I\'ve been a customer for 2 years but the recent changes to the service don\'t meet my needs anymore.',
            'category': 'service',
            'priority': 'normal',
            'status': 'open',
            'notes': 'Subscription cancellation request. Standard retention process.'
        },
        
        # General Inquiries
        {
            'issue_type': 'Product Information',
            'description': 'I\'m interested in upgrading my current plan to the premium version. Can you provide more information about the features and pricing?',
            'category': 'general',
            'priority': 'low',
            'status': 'resolved',
            'notes': 'Provided detailed information about premium features and pricing.'
        },
        {
            'issue_type': 'Feature Request',
            'description': 'I would like to suggest a new feature for the platform. It would be very helpful to have a bulk export function for reports.',
            'category': 'general',
            'priority': 'low',
            'status': 'open',
            'notes': 'Feature request submitted. Will be reviewed by product team.'
        },
        {
            'issue_type': 'General Question',
            'description': 'I have a question about the data retention policy. How long do you keep user data and what happens to it when an account is deleted?',
            'category': 'general',
            'priority': 'low',
            'status': 'resolved',
            'notes': 'Provided detailed information about data retention policies.'
        },
        
        # Emergency Issues
        {
            'issue_type': 'Security Breach',
            'description': 'I think my account has been compromised. I received an email about a login from an unknown location and I didn\'t make that login attempt.',
            'category': 'emergency',
            'priority': 'urgent',
            'status': 'in_progress',
            'notes': 'Security incident reported. Immediate investigation required.'
        },
        {
            'issue_type': 'Data Loss',
            'description': 'All my data disappeared from my account. I had important files that are now gone and I need them recovered immediately.',
            'category': 'emergency',
            'priority': 'urgent',
            'status': 'open',
            'notes': 'Critical data loss reported. Emergency recovery process initiated.'
        }
    ]
    
    # Create tickets with varied timestamps
    base_time = datetime.now() - timedelta(days=30)
    
    for i, complaint in enumerate(complaints):
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
            issue_type=complaint['issue_type'],
            description=complaint['description'],
            status=complaint['status'],
            priority=complaint['priority'],
            notes=complaint['notes'],
            user_id=user.id,
            assigned_admin_id=assigned_admin.id if assigned_admin else None,
            created_at=created_at,
            updated_at=created_at + timedelta(hours=random.randint(1, 48)) if complaint['status'] != 'open' else created_at
        )
        
        db.session.add(ticket)
        print(f"Created ticket: {complaint['issue_type']} (Priority: {complaint['priority']}, Status: {complaint['status']})")
    
    db.session.commit()
    print(f"Created {len(complaints)} dummy tickets")

def main():
    """Main function to populate the database"""
    with app.app_context():
        print("Starting database population...")
        
        # Create users
        print("\n=== Creating Users ===")
        users = create_dummy_users()
        
        # Create tickets
        print("\n=== Creating Tickets ===")
        create_dummy_tickets(users)
        
        print("\n=== Database Population Complete ===")
        print("Dummy data has been successfully created!")
        print("\nLogin Credentials:")
        print("Regular Users:")
        for user in users:
            if not user.is_admin:
                print(f"  Email: {user.email}, Password: password123")
        print("\nAdmin Users:")
        for user in users:
            if user.is_admin:
                print(f"  Email: {user.email}, Password: admin123/manager123")

if __name__ == "__main__":
    main()
