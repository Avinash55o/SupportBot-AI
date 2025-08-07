# 📧 Email Notification Setup Guide

This guide will help you configure the email notification system in `notifier.py`.

## 🔧 Required Configuration

You need to create a `.env` file in the `backend` directory with the following variables:

```env
# Database Configuration
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key-here

# Email Notification Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=avigamer503@gmail.com
SMTP_PASSWORD=your-app-password-here
```

## 📋 What You Need to Configure:

### 1. **Gmail Account Setup**
Since your notifier.py is configured for Gmail (`avigamer503@gmail.com`), you need to:

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this password in `SMTP_PASSWORD`

### 2. **Environment Variables**

Create a `.env` file in the `backend` directory with:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=avigamer503@gmail.com
SMTP_PASSWORD=your-16-digit-app-password
```

## 🚀 How to Use the Notifier

### Email Notifications
```python
from utils.notifier import send_email_notification

# Send ticket update notification
send_email_notification(
    to_email="user@example.com",
    subject="Ticket #123 Updated",
    message="Your ticket has been updated to 'In Progress'"
)
```

### Integration with Ticket System
You can integrate notifications into your ticket controller:

```python
# In ticket_controller.py
from utils.notifier import send_email_notification

def update_ticket_status(ticket_id, new_status):
    # Update ticket logic...
    
    # Send notification
    if ticket.user.email:
        send_email_notification(
            to_email=ticket.user.email,
            subject=f"Ticket #{ticket.id} Status Update",
            message=f"Your ticket '{ticket.issue_type}' has been updated to {new_status}"
        )
```

## 📧 Notification Examples

### 1. **Ticket Created**
```python
send_email_notification(
    to_email=user_email,
    subject="New Ticket Created",
    message=f"""
    Your ticket has been created successfully!
    
    Ticket ID: {ticket.id}
    Issue: {ticket.issue_type}
    Priority: {ticket.priority}
    Status: {ticket.status}
    
    We'll keep you updated on the progress.
    """
)
```

### 2. **Status Update**
```python
send_email_notification(
    to_email=user_email,
    subject=f"Ticket #{ticket.id} Status Changed",
    message=f"""
    Your ticket status has been updated:
    
    Previous Status: {old_status}
    New Status: {new_status}
    Updated By: {admin_name}
    
    We'll continue working on your issue.
    """
)
```

### 3. **Admin Assignment**
```python
send_email_notification(
    to_email=user_email,
    subject=f"Ticket #{ticket.id} Assigned",
    message=f"""
    Your ticket has been assigned to a support specialist:
    
    Ticket: {ticket.issue_type}
    Assigned To: {admin_name}
    Expected Response: Within 24 hours
    
    Thank you for your patience.
    """
)
```

## 🔒 Security Notes

1. **Never commit your `.env` file** to version control
2. **Use App Passwords** instead of your regular Gmail password
3. **Keep your credentials secure**
4. **Test with a small group** before sending to all users

## 🧪 Testing

You can test the email functionality:

```python
# Test email
send_email_notification(
    to_email="your-test-email@gmail.com",
    subject="Test Notification",
    message="This is a test email from SupportBot AI"
)
```

## 📱 Optional: SMS Notifications

If you want SMS notifications via Twilio, uncomment the SMS section in `notifier.py` and add:

```env
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_FROM_NUMBER=your-twilio-phone-number
```

## 🎯 Integration Points

The notifier can be integrated at these points in your application:

1. **Ticket Creation** - Notify user when ticket is created
2. **Status Updates** - Notify user when status changes
3. **Admin Assignment** - Notify user when admin is assigned
4. **Resolution** - Notify user when ticket is resolved
5. **Follow-up** - Send follow-up emails for unresolved tickets

## ⚠️ Troubleshooting

### Common Issues:

1. **"Authentication failed"** - Check your app password
2. **"Connection refused"** - Check SMTP settings
3. **"Recipient not found"** - Verify email address
4. **"Quota exceeded"** - Gmail has daily sending limits

### Debug Mode:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
# This will show detailed SMTP communication
```

---

**Remember:** Always test email notifications in a development environment before deploying to production!
