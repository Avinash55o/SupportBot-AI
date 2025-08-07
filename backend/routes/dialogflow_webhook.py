from flask import Blueprint, request, jsonify
from controllers.ticket_controller import TicketController
from controllers.nlp_controller import NLPController
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dialogflow_webhook = Blueprint('dialogflow_webhook', __name__)
ticket_controller = TicketController()
nlp_controller = NLPController()

@dialogflow_webhook.route('/create-ticket', methods=['POST'])
def create_ticket():
    """Create a new ticket from frontend with AI analysis"""
    data = request.get_json()
    
    if not data or not data.get('description'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Use AI-powered ticket creation
        result = ticket_controller.create_ticket_with_ai_analysis(
            description=data['description'],
            user_id=data.get('user_id')
        )
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Error creating ticket: {str(e)}")
        return jsonify({'error': str(e)}), 400

@dialogflow_webhook.route('/analyze-complaint', methods=['POST'])
def analyze_complaint():
    """Analyze complaint text using AI/ML"""
    data = request.get_json()
    
    if not data or not data.get('text'):
        return jsonify({'error': 'Missing text field'}), 400
    
    try:
        # Perform AI analysis
        analysis = nlp_controller.analyze_complaint(data['text'])
        
        # Get intelligent response
        intelligent_response = nlp_controller.get_intelligent_response(data['text'], analysis)
        
        # Extract entities
        entities = nlp_controller.extract_entities(data['text'])
        
        # Find similar tickets
        similar_tickets = nlp_controller.get_similar_tickets(data['text'], limit=3)
        
        return jsonify({
            'analysis': analysis,
            'intelligent_response': intelligent_response,
            'entities': entities,
            'similar_tickets': similar_tickets
        }), 200
        
    except Exception as e:
        logger.error(f"Error analyzing complaint: {str(e)}")
        return jsonify({'error': str(e)}), 400

@dialogflow_webhook.route('/suggest-assignment/<int:ticket_id>', methods=['GET'])
def suggest_assignment(ticket_id):
    """Get AI suggestion for ticket assignment"""
    try:
        suggestion = ticket_controller.suggest_ticket_assignment(ticket_id)
        return jsonify(suggestion), 200
    except Exception as e:
        logger.error(f"Error suggesting assignment: {str(e)}")
        return jsonify({'error': str(e)}), 400

@dialogflow_webhook.route('/similar-tickets/<int:ticket_id>', methods=['GET'])
def get_similar_tickets(ticket_id):
    """Get similar tickets using AI similarity analysis"""
    try:
        similar_tickets = ticket_controller.get_similar_tickets(ticket_id)
        return jsonify({'similar_tickets': similar_tickets}), 200
    except Exception as e:
        logger.error(f"Error getting similar tickets: {str(e)}")
        return jsonify({'error': str(e)}), 400

@dialogflow_webhook.route('/retrain-models', methods=['POST'])
def retrain_models():
    """Retrain AI models with feedback"""
    data = request.get_json()
    
    if not data or not data.get('ticket_id'):
        return jsonify({'error': 'Missing ticket_id field'}), 400
    
    try:
        result = ticket_controller.retrain_models_with_feedback(
            ticket_id=data['ticket_id'],
            actual_category=data.get('actual_category'),
            actual_priority=data.get('actual_priority')
        )
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error retraining models: {str(e)}")
        return jsonify({'error': str(e)}), 400

@dialogflow_webhook.route('/ai-insights', methods=['GET'])
def get_ai_insights():
    """Get AI-powered insights from ticket data"""
    try:
        analytics = ticket_controller.get_ticket_analytics()
        return jsonify(analytics), 200
    except Exception as e:
        logger.error(f"Error getting AI insights: {str(e)}")
        return jsonify({'error': str(e)}), 400