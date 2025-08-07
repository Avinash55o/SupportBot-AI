from models.ticket import Ticket
from models.user import User
from models import db
from sqlalchemy import desc
from datetime import datetime, timedelta

class TicketController:
    def create_ticket(self, issue_type, description, user_id=None, priority="normal"):
        """Create a new ticket"""
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
    
    def get_user_tickets(self, user_id):
        """Get all tickets for a specific user"""
        return Ticket.query.filter_by(user_id=user_id).order_by(desc(Ticket.created_at)).all()
    
    def get_all_tickets(self, status=None, priority=None, page=1, per_page=10, ticket_id=None):
        """Get all tickets with optional filtering and pagination"""
        query = Ticket.query
        
        if ticket_id:
            return query.filter_by(id=ticket_id).first()
        
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        
        # Add pagination
        pagination = query.order_by(desc(Ticket.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            'tickets': pagination.items,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }
    
    def get_ticket_status(self, ticket_id, user_id):
        """Get ticket status for a specific user"""
        ticket = Ticket.query.filter_by(id=ticket_id, user_id=user_id).first()
        if not ticket:
            raise Exception("Ticket not found or access denied")
        return ticket
    
    def assign_ticket(self, ticket_id, admin_id):
        """Assign a ticket to an admin"""
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise Exception("Ticket not found")
        
        admin = User.query.filter_by(id=admin_id, is_admin=True).first()
        if not admin:
            raise Exception("Admin not found")
        
        ticket.assigned_admin_id = admin_id
        ticket.status = 'assigned'
        ticket.updated_at = datetime.utcnow()
        
        db.session.commit()
        return ticket
    
    def update_ticket_status(self, ticket_id, status=None, priority=None, notes=None):
        """Update ticket status and/or priority"""
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise Exception("Ticket not found")
        
        if status:
            ticket.status = status
        if priority:
            ticket.priority = priority
        if notes:
            # You might want to add a notes field to your Ticket model
            pass
        
        ticket.updated_at = datetime.utcnow()
        db.session.commit()
        
        return ticket
    
    def get_ticket_analytics(self):
        """Get analytics for admin dashboard"""
        total_tickets = Ticket.query.count()
        open_tickets = Ticket.query.filter_by(status='open').count()
        in_progress_tickets = Ticket.query.filter_by(status='in_progress').count()
        resolved_tickets = Ticket.query.filter_by(status='resolved').count()
        
        # Get tickets by priority
        high_priority = Ticket.query.filter_by(priority='high').count()
        urgent_priority = Ticket.query.filter_by(priority='urgent').count()
        
        # Get tickets created in last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_tickets = Ticket.query.filter(Ticket.created_at >= week_ago).count()
        
        # Calculate average resolution time (for resolved tickets)
        resolved_tickets_data = Ticket.query.filter_by(status='resolved').all()
        total_resolution_time = 0
        resolved_count = 0
        
        for ticket in resolved_tickets_data:
            if ticket.updated_at and ticket.created_at:
                resolution_time = (ticket.updated_at - ticket.created_at).total_seconds() / 3600  # hours
                total_resolution_time += resolution_time
                resolved_count += 1
        
        avg_resolution_time = total_resolution_time / resolved_count if resolved_count > 0 else 0
        
        return {
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'in_progress_tickets': in_progress_tickets,
            'resolved_tickets': resolved_tickets,
            'high_priority_tickets': high_priority,
            'urgent_tickets': urgent_priority,
            'recent_tickets': recent_tickets,
            'avg_resolution_time_hours': round(avg_resolution_time, 2)
        }
    
    def delete_ticket(self, ticket_id):
        """Delete a ticket (admin only)"""
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise Exception("Ticket not found")
        
        db.session.delete(ticket)
        db.session.commit()
        
        return {"message": "Ticket deleted successfully"}

# Create instances for use in routes
create_ticket = TicketController().create_ticket
get_user_tickets = TicketController().get_user_tickets
get_all_tickets = TicketController().get_all_tickets
get_ticket_status = TicketController().get_ticket_status
assign_ticket = TicketController().assign_ticket
update_ticket_status = TicketController().update_ticket_status
get_ticket_analytics = TicketController().get_ticket_analytics