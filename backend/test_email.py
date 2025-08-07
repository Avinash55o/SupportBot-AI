#!/usr/bin/env python3
"""
Test script for email notifications
"""

import os
from dotenv import load_dotenv
from utils.notifier import send_email_notification

# Load environment variables
load_dotenv()

def test_email_notification():
    """Test the email notification functionality"""
    
    print("🧪 Testing Email Notification System")
    print("=" * 50)
    
    # Check if environment variables are set
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    if not smtp_user or not smtp_password:
        print("❌ Email configuration not found!")
        print("\n📋 Please create a .env file in the backend directory with:")
        print("SMTP_USER=avigamer503@gmail.com")
        print("SMTP_PASSWORD=your-app-password")
        print("\n🔧 Setup instructions:")
        print("1. Enable 2FA on your Gmail account")
        print("2. Generate an App Password")
        print("3. Add the credentials to .env file")
        return False
    
    print(f"✅ SMTP User: {smtp_user}")
    print(f"✅ SMTP Password: {'*' * len(smtp_password)}")
    
    # Test email
    test_email = input("\n📧 Enter your test email address: ").strip()
    
    if not test_email:
        print("❌ No email address provided")
        return False
    
    print(f"\n📤 Sending test email to {test_email}...")
    
    try:
        success = send_email_notification(
            to_email=test_email,
            subject="SupportBot AI - Test Email",
            message="""
Hello from SupportBot AI!

This is a test email to verify that the notification system is working correctly.

If you received this email, the notification system is properly configured.

Best regards,
SupportBot AI Team
            """
        )
        
        if success:
            print("✅ Test email sent successfully!")
            print("📧 Check your inbox for the test email")
            return True
        else:
            print("❌ Failed to send test email")
            return False
            
    except Exception as e:
        print(f"❌ Error sending test email: {e}")
        return False

def test_ticket_notifications():
    """Test various ticket notification scenarios"""
    
    print("\n🎫 Testing Ticket Notification Scenarios")
    print("=" * 50)
    
    test_email = input("📧 Enter email for ticket notifications: ").strip()
    
    if not test_email:
        print("❌ No email address provided")
        return
    
    # Test different notification types
    notifications = [
        {
            "subject": "Ticket #123 Created",
            "message": """
Your ticket has been created successfully!

Ticket Details:
- ID: #123
- Issue: Billing Problem
- Priority: High
- Status: Open

We'll keep you updated on the progress.
            """
        },
        {
            "subject": "Ticket #123 Status Updated",
            "message": """
Your ticket status has been updated!

Previous Status: Open
New Status: In Progress
Updated By: Support Team

We're working on resolving your issue.
            """
        },
        {
            "subject": "Ticket #123 Assigned",
            "message": """
Your ticket has been assigned to a specialist!

Ticket: Billing Problem
Assigned To: John Admin
Expected Response: Within 24 hours

Thank you for your patience.
            """
        },
        {
            "subject": "Ticket #123 Resolved",
            "message": """
Great news! Your ticket has been resolved!

Ticket: Billing Problem
Resolution: Payment issue corrected
Status: Resolved

Thank you for using our support system!
            """
        }
    ]
    
    for i, notification in enumerate(notifications, 1):
        print(f"\n📧 Sending notification {i}/4...")
        
        success = send_email_notification(
            to_email=test_email,
            subject=notification["subject"],
            message=notification["message"]
        )
        
        if success:
            print(f"✅ Notification {i} sent successfully!")
        else:
            print(f"❌ Failed to send notification {i}")
        
        # Wait a bit between emails
        import time
        time.sleep(2)

if __name__ == "__main__":
    print("🚀 SupportBot AI - Email Notification Tester")
    print("=" * 60)
    
    # Test basic email functionality
    if test_email_notification():
        print("\n🎉 Basic email test passed!")
        
        # Ask if user wants to test ticket notifications
        test_tickets = input("\n🎫 Test ticket notification scenarios? (y/n): ").lower().strip()
        
        if test_tickets == 'y':
            test_ticket_notifications()
    
    print("\n✅ Email testing complete!")
