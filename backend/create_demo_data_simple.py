#!/usr/bin/env python3
"""
Create demo data using direct SQLite operations
"""
import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def create_demo_data():
    """Create demo data using direct SQLite operations"""
    db_path = 'app.db'
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Removed existing database")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🚀 Creating demo data for SupportBot AI...")
    
    # Create tables
    cursor.execute('''
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE ticket (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token VARCHAR(15) UNIQUE NOT NULL,
            issue_type VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            status VARCHAR(50) DEFAULT 'open',
            priority VARCHAR(50) DEFAULT 'normal',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            assigned_admin_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (assigned_admin_id) REFERENCES user (id)
        )
    ''')
    
    print("✅ Created database tables")
    
    # Create demo users
    print("\n👥 Creating demo users...")
    
    users = [
        ('Admin User', 'admin@supportbot.com', generate_password_hash('admin123'), True),
        ('John Doe', 'john@example.com', generate_password_hash('user123'), False),
        ('Jane Smith', 'jane@example.com', generate_password_hash('user123'), False),
        ('Mike Johnson', 'mike@example.com', generate_password_hash('user123'), False),
    ]
    
    cursor.executemany('''
        INSERT INTO user (name, email, password_hash, is_admin)
        VALUES (?, ?, ?, ?)
    ''', users)
    
    print("✅ Created demo users")
    
    # Generate tokens and create demo tickets
    print("\n🎫 Creating demo tickets...")
    
    def generate_token():
        """Generate a ticket token"""
        return f"TKT-{datetime.now().strftime('%y%m%d')}-{os.urandom(2).hex().upper()}"
    
    tickets = [
        # High priority technical issues
        (generate_token(), 'Technical Support', 'Unable to login to my account. Getting "Invalid credentials" error every time I try to access the dashboard.', 'open', 'high', 'User reported persistent login issues with error message', 2, None, datetime.now() - timedelta(days=2, hours=3)),
        (generate_token(), 'System Error', 'The application crashes when I try to upload files larger than 10MB. This is urgent as I need to submit my report today.', 'in_progress', 'urgent', 'File upload crash issue - investigating memory allocation', 3, None, datetime.now() - timedelta(days=1, hours=5)),
        
        # Billing and payment issues
        (generate_token(), 'Billing', 'I was charged twice for my subscription this month. Please refund the duplicate charge.', 'in_progress', 'normal', 'Double charge issue - investigating payment records', 2, None, datetime.now() - timedelta(days=1, hours=2)),
        (generate_token(), 'Payment Processing', 'My payment method was declined but I have sufficient funds. Please help me update my payment information.', 'open', 'high', 'Payment method update required', 4, None, datetime.now() - timedelta(hours=8)),
        
        # Feature requests
        (generate_token(), 'Feature Request', 'Would like to see a dark mode option in the mobile app. This would be very helpful for night-time usage.', 'open', 'low', 'User requested dark mode feature for mobile app', 3, None, datetime.now() - timedelta(hours=6)),
        (generate_token(), 'Feature Request', 'Please add the ability to export data to Excel format. Currently only CSV export is available.', 'open', 'normal', 'Excel export functionality requested', 2, None, datetime.now() - timedelta(hours=4)),
        
        # Resolved tickets
        (generate_token(), 'Bug Report', 'The search function is not working properly on the dashboard. It returns no results even for simple queries.', 'resolved', 'high', 'Search functionality fixed in latest update v2.1.3', 3, None, datetime.now() - timedelta(days=3)),
        (generate_token(), 'Account Management', 'Need to update my email address and phone number in my profile.', 'closed', 'normal', 'Account details updated successfully', 2, None, datetime.now() - timedelta(days=5)),
        
        # Recent tickets
        (generate_token(), 'Performance Issue', 'The application is running very slowly today. Pages take 10-15 seconds to load.', 'open', 'high', 'Performance degradation reported - monitoring server load', 4, None, datetime.now() - timedelta(hours=2)),
        (generate_token(), 'UI/UX Issue', 'The mobile app interface is not responsive on my iPhone. Buttons are too small to tap accurately.', 'open', 'normal', 'Mobile UI responsiveness issue - iOS specific', 3, None, datetime.now() - timedelta(hours=1)),
    ]
    
    cursor.executemany('''
        INSERT INTO ticket (token, issue_type, description, status, priority, notes, user_id, assigned_admin_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tickets)
    
    print("✅ Created demo tickets with tokens")
    
    # Commit changes
    conn.commit()
    
    # Verify data
    cursor.execute('SELECT COUNT(*) FROM user')
    user_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM ticket')
    ticket_count = cursor.fetchone()[0]
    
    print(f"\n📊 Demo Data Summary:")
    print(f"   Users: {user_count}")
    print(f"   Tickets: {ticket_count}")
    
    # Show sample tickets
    cursor.execute('''
        SELECT id, token, issue_type, status, priority, user_id 
        FROM ticket 
        ORDER BY created_at DESC 
        LIMIT 5
    ''')
    
    sample_tickets = cursor.fetchall()
    print(f"\n📋 Sample tickets created:")
    for ticket in sample_tickets:
        print(f"   ID: {ticket[0]:2d} | Token: {ticket[1]} | Issue: {ticket[2]}")
        print(f"   Status: {ticket[3]:12} | Priority: {ticket[4]:8} | User: {ticket[5]}")
        print()
    
    # Print login credentials
    print(f"\n🔐 Login Credentials:")
    print(f"   Admin: admin@supportbot.com / admin123")
    print(f"   User 1: john@example.com / user123")
    print(f"   User 2: jane@example.com / user123")
    print(f"   User 3: mike@example.com / user123")
    
    conn.close()
    print(f"\n✅ Demo data setup completed successfully!")
    print(f"   Database file: {db_path}")
    print(f"   The system is ready for testing with realistic data.")

if __name__ == "__main__":
    create_demo_data()
