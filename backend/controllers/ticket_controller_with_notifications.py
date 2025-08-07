from models.ticket import Ticket
from models.user import User
from models import db
from sqlalchemy import desc
from datetime import datetime, timedelta
from controllers.nlp_controller import NLPController
from utils.notifier import send_email_notification
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TicketControllerWithNotifications:
    def __init__(self):
        """Initialize Ticket Controller with NLP Controller and Notifications"""
        self.nlp_controller = NLPController()
    
    def create_ticket(self, issue_type, description, user_id=None, priority="normal"):
        """Create a new ticket with AI/ML analysis and email notification"""
        try:
            # Analyze the complaint using AI/ML
            analysis = self.nlp_controller.analyze_complaint(description)
            
            # Use AI-predicted category and priority if not provided
            if not issue_type or issue_type == "auto":
                issue_type = analysis.get("category", "general")
            
            if priority == "auto":
                priority = analysis.get("priority", "normal")
            
            # Create ticket with AI analysis
            ticket = Ticket(
                issue_type=issue_type,
                description=description,
                user_id=user_id,
                priority=priority,
                status='open'
            )
            
            db.session.add(ticket)
            db.session.commit()
            
            # Send email notification to user
            if user_id:
                user = User.query.get(user_id)
                if user and user.email:
                    self._send_ticket_created_notification(ticket, user)
            
            # Store AI analysis results
            logger.info(f"Ticket {ticket.id} created with AI analysis: {analysis}")
            
            return ticket
            
        except Exception as e:
            logger.error(f"Error creating ticket with AI analysis: {str(e)}")
            # Fallback to basic ticket creation
            ticket = Ticket(
                issue_type=issue_type,
                description=description,
                user_id=user_id,
                priority=priority,
                status='open'
            )
            
            db.session.add(ticket)
            db.session.commit()
            
            return ticket
    
    def update_ticket_status(self, ticket_id, status=None, priority=None, notes=None, admin_id=None):
        """Update ticket status and send notification"""
        try:
            ticket = Ticket.query.get(ticket_id)
            if not ticket:
                return {"error": "Ticket not found"}
            
            old_status = ticket.status
            old_priority = ticket.priority
            
            # Update ticket
            if status:
                ticket.status = status
            if priority:
                ticket.priority = priority
            if notes:
                ticket.notes = notes
            
            ticket.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Send notification to user
            if ticket.user and ticket.user.email:
                self._send_status_update_notification(ticket, old_status, old_priority, admin_id)
            
            return {"success": True, "ticket": ticket.to_dict()}
            
        except Exception as e:
            logger.error(f"Error updating ticket status: {str(e)}")
            return {"error": str(e)}
    
    def assign_ticket(self, ticket_id, admin_id):
        """Assign ticket to admin and send notification"""
        try:
            ticket = Ticket.query.get(ticket_id)
            admin = User.query.get(admin_id)
            
            if not ticket:
                return {"error": "Ticket not found"}
            if not admin or not admin.is_admin:
                return {"error": "Invalid admin"}
            
            old_admin_id = ticket.assigned_admin_id
            ticket.assigned_admin_id = admin_id
            ticket.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Send notification to user
            if ticket.user and ticket.user.email:
                self._send_assignment_notification(ticket, admin)
            
            return {"success": True, "ticket": ticket.to_dict()}
            
        except Exception as e:
            logger.error(f"Error assigning ticket: {str(e)}")
            return {"error": str(e)}
    
    def resolve_ticket(self, ticket_id, resolution_notes=None, admin_id=None):
        """Resolve ticket and send notification"""
        try:
            ticket = Ticket.query.get(ticket_id)
            if not ticket:
                return {"error": "Ticket not found"}
            
            ticket.status = "resolved"
            if resolution_notes:
                ticket.notes = resolution_notes
            ticket.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Send resolution notification to user
            if ticket.user and ticket.user.email:
                self._send_resolution_notification(ticket, resolution_notes, admin_id)
            
            return {"success": True, "ticket": ticket.to_dict()}
            
        except Exception as e:
            logger.error(f"Error resolving ticket: {str(e)}")
            return {"error": str(e)}
    
    # Email Notification Methods
    
    def _send_ticket_created_notification(self, ticket, user):
        """Send notification when ticket is created"""
        subject = f"Ticket #{ticket.id} Created - {ticket.issue_type}"
        message = f"""
Dear {user.name},

Your ticket has been created successfully!

Ticket Details:
- Ticket ID: #{ticket.id}
- Issue Type: {ticket.issue_type}
- Priority: {ticket.priority.title()}
- Status: {ticket.status.title()}
- Description: {ticket.description[:100]}{'...' if len(ticket.description) > 100 else ''}

We'll keep you updated on the progress of your ticket.

Best regards,
SupportBot AI Team
        """
        
        send_email_notification(user.email, subject, message)
    
    def _send_status_update_notification(self, ticket, old_status, old_priority, admin_id=None):
        """Send notification when ticket status is updated"""
        admin_name = "Support Team"
        if admin_id:
            admin = User.query.get(admin_id)
            if admin:
                admin_name = admin.name
        
        subject = f"Ticket #{ticket.id} Status Updated"
        message = f"""
Dear {ticket.user.name},

Your ticket status has been updated!

Ticket Details:
- Ticket ID: #{ticket.id}
- Issue: {ticket.issue_type}
- Previous Status: {old_status.title()}
- New Status: {ticket.status.title()}
- Previous Priority: {old_priority.title()}
- Current Priority: {ticket.priority.title()}
- Updated By: {admin_name}

We're working to resolve your issue as quickly as possible.

Best regards,
SupportBot AI Team
        """
        
        send_email_notification(ticket.user.email, subject, message)
    
    def _send_assignment_notification(self, ticket, admin):
        """Send notification when ticket is assigned to admin"""
        subject = f"Ticket #{ticket.id} Assigned to Specialist"
        message = f"""
Dear {ticket.user.name},

Your ticket has been assigned to a support specialist!

Ticket Details:
- Ticket ID: #{ticket.id}
- Issue: {ticket.issue_type}
- Assigned To: {admin.name}
- Expected Response: Within 24 hours
- Priority: {ticket.priority.title()}

Your specialist will review your case and provide updates.

Thank you for your patience.

Best regards,
SupportBot AI Team
        """
        
        send_email_notification(ticket.user.email, subject, message)
    
    def _send_resolution_notification(self, ticket, resolution_notes, admin_id=None):
        """Send notification when ticket is resolved"""
        admin_name = "Support Team"
        if admin_id:
            admin = User.query.get(admin_id)
            if admin:
                admin_name = admin.name
        
        subject = f"Ticket #{ticket.id} Resolved"
        message = f"""
Dear {ticket.user.name},

Great news! Your ticket has been resolved!

Ticket Details:
- Ticket ID: #{ticket.id}
- Issue: {ticket.issue_type}
- Resolution: {resolution_notes or 'Issue has been resolved'}
- Resolved By: {admin_name}
- Resolution Date: {ticket.updated_at.strftime('%Y-%m-%d %H:%M')}

If you have any further questions, please don't hesitate to create a new ticket.

Thank you for using our support system!

Best regards,
SupportBot AI Team
        """
        
        send_email_notification(ticket.user.email, subject, message)
    
    def send_follow_up_notification(self, ticket):
        """Send follow-up notification for unresolved tickets"""
        if ticket.status == "open" and ticket.created_at < datetime.utcnow() - timedelta(days=3):
            subject = f"Ticket #{ticket.id} - Follow-up"
            message = f"""
Dear {ticket.user.name},

We wanted to follow up on your ticket to ensure you're receiving the support you need.

Ticket Details:
- Ticket ID: #{ticket.id}
- Issue: {ticket.issue_type}
- Status: {ticket.status.title()}
- Created: {ticket.created_at.strftime('%Y-%m-%d')}

If you need immediate assistance, please reply to this email or create a new ticket.

Best regards,
SupportBot AI Team
            """
            
            send_email_notification(ticket.user.email, subject, message)
    
    # Additional helper methods
    def get_user_tickets(self, user_id):
        """Get all tickets for a specific user"""
        return Ticket.query.filter_by(user_id=user_id).order_by(desc(Ticket.created_at)).all()
    
    def get_all_tickets(self, status=None, priority=None, page=1, per_page=10):
        """Get all tickets with optional filtering"""
        query = Ticket.query
        
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        
        return query.order_by(desc(Ticket.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    def get_ticket_analytics(self):
        """Get ticket analytics for admin dashboard"""
        total_tickets = Ticket.query.count()
        open_tickets = Ticket.query.filter_by(status='open').count()
        in_progress_tickets = Ticket.query.filter_by(status='in_progress').count()
        resolved_tickets = Ticket.query.filter_by(status='resolved').count()
        
        return {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "in_progress_tickets": in_progress_tickets,
            "resolved_tickets": resolved_tickets,
            "resolution_rate": (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0
        }

# Example usage:
# controller = TicketControllerWithNotifications()
# 
# # Create ticket with notification
# ticket = controller.create_ticket("billing", "I have a billing issue", user_id=1)
# 
# # Update status with notification
# controller.update_ticket_status(ticket.id, status="in_progress", admin_id=2)
# 
# # Assign ticket with notification
# controller.assign_ticket(ticket.id, admin_id=2)
# 
# # Resolve ticket with notification
# controller.resolve_ticket(ticket.id, "Issue resolved", admin_id=2)
