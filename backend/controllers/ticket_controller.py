from models.ticket import Ticket
from models.user import User
from models import db
from sqlalchemy import desc
from datetime import datetime, timedelta
from controllers.nlp_controller import NLPController
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TicketController:
    def __init__(self):
        """Initialize Ticket Controller with NLP Controller"""
        self.nlp_controller = NLPController()
    
    def create_ticket(self, issue_type, description, user_id=None, priority="normal"):
        """Create a new ticket with AI/ML analysis"""
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
            
            # Store AI analysis results (you might want to add an analysis field to Ticket model)
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
    
    def create_ticket_with_ai_analysis(self, description, user_id=None):
        """
        Create a ticket with full AI/ML analysis and intelligent categorization
        
        Args:
            description: Complaint description
            user_id: User ID (optional)
            
        Returns:
            Dictionary with ticket and analysis results
        """
        try:
            # Perform AI analysis
            analysis = self.nlp_controller.analyze_complaint(description)
            
            # Get intelligent response
            intelligent_response = self.nlp_controller.get_intelligent_response(description, analysis)
            
            # Extract entities
            entities = self.nlp_controller.extract_entities(description)
            
            # Find similar tickets
            similar_tickets = self.nlp_controller.get_similar_tickets(description, limit=3)
            
            # Create ticket with AI predictions
            ticket = self.create_ticket(
                issue_type=analysis.get("category", "general"),
                description=description,
                user_id=user_id,
                priority=analysis.get("priority", "normal")
            )
            
            return {
                "ticket": ticket.to_dict(),
                "analysis": analysis,
                "intelligent_response": intelligent_response,
                "entities": entities,
                "similar_tickets": similar_tickets
            }
            
        except Exception as e:
            logger.error(f"Error creating ticket with AI analysis: {str(e)}")
            # Fallback to basic ticket creation
            ticket = self.create_ticket(
                issue_type="general",
                description=description,
                user_id=user_id,
                priority="normal"
            )
            
            return {
                "ticket": ticket.to_dict(),
                "analysis": {"error": str(e)},
                "intelligent_response": "I'll create a ticket for our team to review your concern.",
                "entities": {},
                "similar_tickets": []
            }
    
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
        """Assign a ticket to an admin with AI suggestions"""
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
    
    def suggest_ticket_assignment(self, ticket_id):
        """
        Suggest admin assignment for a ticket using AI
        
        Args:
            ticket_id: ID of the ticket
            
        Returns:
            Dictionary with suggested admin and reasoning
        """
        try:
            ticket = Ticket.query.get(ticket_id)
            if not ticket:
                return {"error": "Ticket not found"}
            
            # Get available admins
            available_admins = User.query.filter_by(is_admin=True).all()
            
            if not available_admins:
                return {"error": "No available admins"}
            
            # Analyze ticket for assignment suggestions
            analysis = self.nlp_controller.analyze_complaint(ticket.description)
            
            # Get AI suggestion
            suggested_admin_id = self.nlp_controller.suggest_assignment(analysis, available_admins)
            
            if suggested_admin_id:
                suggested_admin = User.query.get(suggested_admin_id)
                return {
                    "suggested_admin": {
                        "id": suggested_admin.id,
                        "name": suggested_admin.name,
                        "email": suggested_admin.email
                    },
                    "reasoning": f"AI suggests {suggested_admin.name} based on category '{analysis.get('category')}' and priority '{analysis.get('priority')}'",
                    "analysis": analysis
                }
            else:
                return {"error": "Could not suggest assignment"}
                
        except Exception as e:
            logger.error(f"Error suggesting ticket assignment: {str(e)}")
            return {"error": str(e)}
    
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
        """Get analytics for admin dashboard with AI insights"""
        total_tickets = Ticket.query.count()
        open_tickets = Ticket.query.filter_by(status='open').count()
        in_progress_tickets = Ticket.query.filter_by(status='in_progress').count()
        resolved_tickets = Ticket.query.filter_by(status='resolved').count()
        
        # Get AI insights
        ai_insights = self._get_ai_insights()
        
        return {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "in_progress_tickets": in_progress_tickets,
            "resolved_tickets": resolved_tickets,
            "ai_insights": ai_insights
        }
    
    def _get_ai_insights(self):
        """Get AI-powered insights from ticket data"""
        try:
            # Get recent tickets for analysis
            recent_tickets = Ticket.query.order_by(desc(Ticket.created_at)).limit(100).all()
            
            if not recent_tickets:
                return {"message": "No tickets available for analysis"}
            
            # Analyze patterns
            categories = {}
            priorities = {}
            sentiments = []
            
            for ticket in recent_tickets:
                # Count categories
                categories[ticket.issue_type] = categories.get(ticket.issue_type, 0) + 1
                
                # Count priorities
                priorities[ticket.priority] = priorities.get(ticket.priority, 0) + 1
                
                # Analyze sentiment
                sentiment = self.nlp_controller.ml_loader.analyze_sentiment(ticket.description)
                sentiments.append(sentiment.get("sentiment", "neutral"))
            
            # Calculate insights
            total_analyzed = len(recent_tickets)
            avg_sentiment = sum(1 for s in sentiments if s == "positive") / total_analyzed if total_analyzed > 0 else 0
            
            return {
                "total_analyzed": total_analyzed,
                "category_distribution": categories,
                "priority_distribution": priorities,
                "average_sentiment": avg_sentiment,
                "top_categories": sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3],
                "top_priorities": sorted(priorities.items(), key=lambda x: x[1], reverse=True)[:3]
            }
            
        except Exception as e:
            logger.error(f"Error getting AI insights: {str(e)}")
            return {"error": str(e)}
    
    def get_similar_tickets(self, ticket_id, limit=5):
        """
        Get similar tickets using AI similarity analysis
        
        Args:
            ticket_id: ID of the ticket to find similar ones for
            limit: Maximum number of similar tickets to return
            
        Returns:
            List of similar tickets
        """
        try:
            ticket = Ticket.query.get(ticket_id)
            if not ticket:
                return []
            
            return self.nlp_controller.get_similar_tickets(ticket.description, limit)
            
        except Exception as e:
            logger.error(f"Error getting similar tickets: {str(e)}")
            return []
    
    def retrain_models_with_feedback(self, ticket_id, actual_category=None, actual_priority=None):
        """
        Retrain AI models with feedback from resolved tickets
        
        Args:
            ticket_id: ID of the resolved ticket
            actual_category: Actual category that was assigned
            actual_priority: Actual priority that was assigned
            
        Returns:
            Training results
        """
        try:
            ticket = Ticket.query.get(ticket_id)
            if not ticket:
                return {"error": "Ticket not found"}
            
            # Use current ticket values if not provided
            if not actual_category:
                actual_category = ticket.issue_type
            if not actual_priority:
                actual_priority = ticket.priority
            
            # Retrain models
            result = self.nlp_controller.train_with_feedback(ticket_id, actual_category, actual_priority)
            
            logger.info(f"Models retrained with feedback for ticket {ticket_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error retraining models: {str(e)}")
            return {"error": str(e)}
    
    def delete_ticket(self, ticket_id):
        """Delete a ticket"""
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