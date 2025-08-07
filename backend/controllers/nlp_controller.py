from typing import Dict, List, Tuple, Optional
import logging
from utils.ml_loader import MLLoader
from models.ticket import Ticket
from models import db
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPController:
    def __init__(self):
        """Initialize NLP Controller with ML Loader"""
        self.ml_loader = MLLoader()
        self._initialize_training_data()
    
    def _initialize_training_data(self):
        """Initialize with some training data if models are not trained"""
        # This is sample training data - in production, you'd load from database
        sample_training_data = [
            # Billing related
            {"text": "I have a billing issue with my account", "category": "billing", "priority": "high"},
            {"text": "My payment was charged twice", "category": "billing", "priority": "urgent"},
            {"text": "I need to update my billing information", "category": "billing", "priority": "normal"},
            {"text": "Why was I charged extra fees", "category": "billing", "priority": "high"},
            
            # Technical issues
            {"text": "The system is not working properly", "category": "technical", "priority": "high"},
            {"text": "I can't log into my account", "category": "technical", "priority": "urgent"},
            {"text": "The website is loading slowly", "category": "technical", "priority": "normal"},
            {"text": "I'm getting an error message", "category": "technical", "priority": "high"},
            
            # Service issues
            {"text": "I need help with customer service", "category": "service", "priority": "normal"},
            {"text": "The service quality is poor", "category": "service", "priority": "high"},
            {"text": "I want to cancel my subscription", "category": "service", "priority": "normal"},
            {"text": "The support team is not responding", "category": "service", "priority": "urgent"},
            
            # General inquiries
            {"text": "I have a question about your services", "category": "general", "priority": "low"},
            {"text": "Can you provide more information", "category": "general", "priority": "low"},
            {"text": "I want to know more about your products", "category": "general", "priority": "low"},
        ]
        
        # Train models if they haven't been trained yet
        if not self.ml_loader.get_model_info()["models_loaded"]:
            logger.info("Training models with sample data...")
            self.ml_loader.train_models(sample_training_data)
    
    def analyze_complaint(self, text: str) -> Dict:
        """
        Analyze a complaint text using AI/ML
        
        Args:
            text: Complaint text to analyze
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Predict category and priority
            category, cat_confidence = self.ml_loader.predict_category(text)
            priority, pri_confidence = self.ml_loader.predict_priority(text)
            
            # Analyze sentiment
            sentiment_analysis = self.ml_loader.analyze_sentiment(text)
            
            # Extract keywords
            keywords = self.ml_loader.extract_keywords(text, top_k=5)
            
            # Determine urgency based on keywords and sentiment
            urgency_score = self._calculate_urgency_score(text, sentiment_analysis, priority)
            
            return {
                "category": category,
                "category_confidence": cat_confidence,
                "priority": priority,
                "priority_confidence": pri_confidence,
                "sentiment": sentiment_analysis,
                "keywords": keywords,
                "urgency_score": urgency_score,
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error analyzing complaint: {str(e)}")
            return {
                "category": "general",
                "category_confidence": 0.0,
                "priority": "normal",
                "priority_confidence": 0.0,
                "sentiment": {"sentiment": "neutral", "score": 0.0, "subjectivity": 0.0},
                "keywords": [],
                "urgency_score": 0.0,
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
    
    def _calculate_urgency_score(self, text: str, sentiment: Dict, priority: str) -> float:
        """
        Calculate urgency score based on text content, sentiment, and priority
        
        Args:
            text: Complaint text
            sentiment: Sentiment analysis results
            priority: Predicted priority
            
        Returns:
            Urgency score between 0 and 1
        """
        urgency_score = 0.0
        
        # Base score from priority
        priority_scores = {
            "urgent": 0.9,
            "high": 0.7,
            "normal": 0.5,
            "low": 0.3
        }
        urgency_score += priority_scores.get(priority, 0.5) * 0.4
        
        # Sentiment impact
        sentiment_score = abs(sentiment.get("score", 0))
        urgency_score += sentiment_score * 0.3
        
        # Keyword-based urgency
        urgent_keywords = [
            "urgent", "emergency", "critical", "immediate", "asap", "broken",
            "down", "failed", "error", "issue", "problem", "not working"
        ]
        
        text_lower = text.lower()
        urgent_keyword_count = sum(1 for keyword in urgent_keywords if keyword in text_lower)
        urgency_score += min(urgent_keyword_count * 0.1, 0.3)
        
        return min(urgency_score, 1.0)
    
    def get_intelligent_response(self, text: str, analysis: Dict) -> str:
        """
        Generate intelligent response based on analysis
        
        Args:
            text: Original complaint text
            analysis: Analysis results from analyze_complaint
            
        Returns:
            Intelligent response text
        """
        category = analysis.get("category", "general")
        priority = analysis.get("priority", "normal")
        sentiment = analysis.get("sentiment", {}).get("sentiment", "neutral")
        
        # Base responses based on category and priority
        responses = {
            "billing": {
                "urgent": "I understand this is an urgent billing matter. I'm creating a high-priority ticket that will be escalated immediately to our billing team. They will contact you within 2 hours.",
                "high": "I see you have a billing concern. I'm creating a high-priority ticket for our billing team to review your account and resolve this issue promptly.",
                "normal": "I'll create a billing ticket for our team to review your account and address your concern.",
                "low": "I'll create a billing inquiry ticket for our team to assist you with your question."
            },
            "technical": {
                "urgent": "This sounds like a critical technical issue. I'm creating an urgent ticket that will be escalated to our IT team immediately. They will respond within 1 hour.",
                "high": "I understand you're experiencing technical difficulties. I'll create a high-priority technical support ticket for our IT team to resolve this issue.",
                "normal": "I'll create a technical support ticket for our IT team to investigate and resolve this issue.",
                "low": "I'll create a technical inquiry ticket for our support team to assist you."
            },
            "service": {
                "urgent": "This is an urgent service issue. I'm creating a high-priority ticket that will be escalated to our management team immediately.",
                "high": "I understand your service concern. I'll create a high-priority ticket for our service team to address this issue promptly.",
                "normal": "I'll create a service ticket for our team to review and address your concern.",
                "low": "I'll create a service inquiry ticket for our team to assist you."
            },
            "general": {
                "urgent": "I understand this is urgent. I'm creating a high-priority ticket for our team to address your concern immediately.",
                "high": "I'll create a high-priority ticket for our team to address your concern promptly.",
                "normal": "I'll create a ticket for our team to review and respond to your inquiry.",
                "low": "I'll create a general inquiry ticket for our team to assist you."
            }
        }
        
        # Get appropriate response
        response = responses.get(category, responses["general"]).get(priority, responses["general"]["normal"])
        
        # Add sentiment-based personalization
        if sentiment == "negative":
            response += " I apologize for any inconvenience you've experienced."
        elif sentiment == "positive":
            response += " Thank you for your patience and understanding."
        
        return response
    
    def suggest_assignment(self, analysis: Dict, available_admins: List[Dict]) -> Optional[int]:
        """
        Suggest admin assignment based on analysis and available admins
        
        Args:
            analysis: Analysis results from analyze_complaint
            available_admins: List of available admin users
            
        Returns:
            Suggested admin ID or None
        """
        if not available_admins:
            return None
        
        category = analysis.get("category", "general")
        priority = analysis.get("priority", "normal")
        
        # Simple assignment logic - can be enhanced with more sophisticated algorithms
        for admin in available_admins:
            # Check if admin has expertise in the category
            if hasattr(admin, 'expertise') and category in admin.expertise:
                return admin.id
            
            # Check if admin has low workload
            if hasattr(admin, 'current_tickets') and admin.current_tickets < 5:
                return admin.id
        
        # Default to first available admin
        return available_admins[0].id if available_admins else None
    
    def extract_entities(self, text: str) -> Dict:
        """
        Extract named entities from text (basic implementation)
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with extracted entities
        """
        entities = {
            "emails": [],
            "phone_numbers": [],
            "urls": [],
            "dates": [],
            "amounts": []
        }
        
        import re
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        entities["emails"] = re.findall(email_pattern, text)
        
        # Extract phone numbers
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        entities["phone_numbers"] = re.findall(phone_pattern, text)
        
        # Extract URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        entities["urls"] = re.findall(url_pattern, text)
        
        # Extract amounts (basic)
        amount_pattern = r'\$\d+(?:\.\d{2})?'
        entities["amounts"] = re.findall(amount_pattern, text)
        
        return entities
    
    def get_similar_tickets(self, text: str, limit: int = 5) -> List[Dict]:
        """
        Find similar tickets based on text similarity
        
        Args:
            text: Input text to find similar tickets for
            limit: Maximum number of similar tickets to return
            
        Returns:
            List of similar tickets
        """
        try:
            # Get all tickets from database
            all_tickets = Ticket.query.all()
            
            if not all_tickets:
                return []
            
            # Calculate similarity scores
            similarities = []
            for ticket in all_tickets:
                # Use TF-IDF similarity (simplified)
                similarity_score = self._calculate_text_similarity(text, ticket.description)
                similarities.append({
                    "ticket": ticket.to_dict(),
                    "similarity_score": similarity_score
                })
            
            # Sort by similarity score and return top results
            similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            return [item["ticket"] for item in similarities[:limit]]
            
        except Exception as e:
            logger.error(f"Error finding similar tickets: {str(e)}")
            return []
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts using TF-IDF
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            
            # Preprocess texts
            processed_text1 = self.ml_loader.preprocess_text(text1)
            processed_text2 = self.ml_loader.preprocess_text(text2)
            
            # Vectorize texts
            X = self.ml_loader.vectorizer.transform([processed_text1, processed_text2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(X[0:1], X[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating text similarity: {str(e)}")
            return 0.0
    
    def train_with_feedback(self, ticket_id: int, actual_category: str, actual_priority: str) -> Dict:
        """
        Retrain models with feedback from resolved tickets
        
        Args:
            ticket_id: ID of the resolved ticket
            actual_category: Actual category that was assigned
            actual_priority: Actual priority that was assigned
            
        Returns:
            Training results
        """
        try:
            # Get the ticket
            ticket = Ticket.query.get(ticket_id)
            if not ticket:
                return {"error": "Ticket not found"}
            
            # Prepare training data
            training_data = [{
                "text": ticket.description,
                "category": actual_category,
                "priority": actual_priority
            }]
            
            # Retrain models
            result = self.ml_loader.train_models(training_data)
            
            logger.info(f"Models retrained with feedback for ticket {ticket_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error training with feedback: {str(e)}")
            return {"error": str(e)}
