from flask import Blueprint, request, jsonify
from controllers.ticket_controller import TicketController

dialogflow_webhook = Blueprint('dialogflow_webhook', __name__)
ticket_controller = TicketController()

@dialogflow_webhook.route('/create-ticket', methods=['POST'])
def create_ticket():
    """Create a new ticket from frontend"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['issue_type', 'description']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        ticket = ticket_controller.create_ticket(
            issue_type=data['issue_type'],
            description=data['description'],
            user_id=data.get('user_id'),
            priority=data.get('priority', 'normal')
        )
        
        return jsonify(ticket.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400