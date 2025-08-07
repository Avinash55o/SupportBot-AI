import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Optional: For SMS via Twilio (if you want to use it)
# from twilio.rest import Client

def send_email_notification(to_email, subject, message):
    """
    Send an email notification.
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = smtp_user

    if not all([smtp_user, smtp_password, to_email]):
        print("Email notification not sent: missing credentials or recipient.")
        return False

    msg = MIMEMultipart()
    msg['From'] = "avigamer503@gmail.com"
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Optional: SMS notification via Twilio
# def send_sms_notification(to_number, message):
#     account_sid = os.getenv("TWILIO_ACCOUNT_SID")
#     auth_token = os.getenv("TWILIO_AUTH_TOKEN")
#     from_number = os.getenv("TWILIO_FROM_NUMBER")
#     if not all([account_sid, auth_token, from_number, to_number]):
#         print("SMS notification not sent: missing credentials or recipient.")
#         return False
#     try:
#         client = Client(account_sid, auth_token)
#         message = client.messages.create(
#             body=message,
#             from_=from_number,
#             to=to_number
#         )
#         print(f"SMS sent to {to_number}")
#         return True
#     except Exception as e:
#         print(f"Failed to send SMS: {e}")
#         return False

# Example usage:
# send_email_notification("recipient@example.com", "Test Subject", "Test message")
# send_sms_notification("+1234567890", "Test SMS message")