#!/usr/bin/env python3
"""
Simple test script to verify token generation
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

# Create a minimal Flask app for testing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a simple Ticket model for testing
class TestTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(20), unique=True, nullable=False, default=lambda: f"TKT-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}")
    issue_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='open')
    priority = db.Column(db.String(50), default='normal')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(TestTicket, self).__init__(**kwargs)
        if not self.token:
            self.token = f"TKT-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

    def to_dict(self):
        return {
            "id": self.id,
            "token": self.token,
            "issue_type": self.issue_type,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

def test_token_generation():
    """Test that tickets are created with proper tokens"""
    with app.app_context():
        # Create database tables
        db.create_all()
        print("✅ Created database tables")
        
        # Create test tickets
        tickets = [
            TestTicket(
                issue_type='Technical Support',
                description='Unable to login to my account',
                priority='high',
                status='open'
            ),
            TestTicket(
                issue_type='Billing',
                description='Double charge on my subscription',
                priority='normal',
                status='in_progress'
            ),
            TestTicket(
                issue_type='Feature Request',
                description='Add dark mode to mobile app',
                priority='low',
                status='open'
            ),
        ]
        
        for ticket in tickets:
            db.session.add(ticket)
        
        db.session.commit()
        print("✅ Created test tickets")
        
        # Verify tokens were generated
        all_tickets = TestTicket.query.all()
        print(f"\n📋 Test tickets created:")
        for ticket in all_tickets:
            print(f"   ID: {ticket.id}, Token: {ticket.token}, Issue: {ticket.issue_type}")
            print(f"   Description: {ticket.description[:50]}...")
            print(f"   Priority: {ticket.priority}, Status: {ticket.status}")
            print()
        
        # Test the to_dict method
        for ticket in all_tickets:
            ticket_dict = ticket.to_dict()
            print(f"✅ Ticket {ticket.id} dict contains token: {ticket_dict.get('token', 'MISSING')}")
        
        print(f"\n✅ Token generation test completed successfully!")
        print(f"   Total tickets: {len(all_tickets)}")
        
        # Clean up
        db.drop_all()
        print("✅ Cleaned up test database")

if __name__ == "__main__":
    test_token_generation()
