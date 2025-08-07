from flask import Blueprint, request, jsonify
from controllers.auth_controller import authenticate_admin
from controllers.ticket_controller import TicketController

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/login', methods=['POST'])
def admin_login():
    """Admin login"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Email and password required'}), 400
    
    try:
        token = authenticate_admin.login_admin(
            email=data['email'],
            password=data['password']
        )
        return jsonify({
            'message': 'Admin login successful',
            'token': token
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@admin_blueprint.route('/tickets', methods=['GET'])
def get_tickets():
    """Get all tickets (admin view)"""
    try:
        # Get query parameters for filtering
        status = request.args.get('status')
        priority = request.args.get('priority')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        ticket_controller = TicketController()
        tickets = ticket_controller.get_all_tickets(
            status=status,
            priority=priority,
            page=page,
            per_page=per_page
        )
        
        return jsonify({
            'tickets': [ticket.to_dict() for ticket in tickets['tickets']],
            'total': tickets['total'],
            'page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_blueprint.route('/tickets/<int:ticket_id>/assign', methods=['PUT'])
def assign_ticket_to_admin(ticket_id):
    """Assign a ticket to an admin"""
    data = request.get_json()
    
    if not data or 'admin_id' not in data:
        return jsonify({'error': 'Admin ID required'}), 400
    
    try:
        ticket_controller = TicketController()
        ticket = ticket_controller.assign_ticket(ticket_id, data['admin_id'])
        return jsonify({
            'message': 'Ticket assigned successfully',
            'ticket': ticket.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_blueprint.route('/tickets/<int:ticket_id>/status', methods=['PUT'])
def update_status(ticket_id):
    """Update ticket status"""
    data = request.get_json()
    
    if not data or 'status' not in data:
        return jsonify({'error': 'Status required'}), 400
    
    valid_statuses = ['open', 'in_progress', 'resolved', 'closed']
    if data['status'] not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    try:
        ticket_controller = TicketController()
        ticket = ticket_controller.update_ticket_status(
            ticket_id, 
            data['status'],
            data.get('notes', '')
        )
        return jsonify({
            'message': 'Status updated successfully',
            'ticket': ticket.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_blueprint.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket_details(ticket_id):
    """Get detailed ticket information"""
    try:
        ticket_controller = TicketController()
        ticket = ticket_controller.get_all_tickets(ticket_id=ticket_id)
        return jsonify(ticket.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@admin_blueprint.route('/analytics', methods=['GET'])
def get_analytics():
    """Get ticket analytics for dashboard"""
    try:
        ticket_controller = TicketController()
        analytics = ticket_controller.get_ticket_analytics()
        return jsonify(analytics), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_blueprint.route('/tickets/<int:ticket_id>/priority', methods=['PUT'])
def update_priority(ticket_id):
    """Update ticket priority"""
    data = request.get_json()
    
    if not data or 'priority' not in data:
        return jsonify({'error': 'Priority required'}), 400
    
    valid_priorities = ['low', 'normal', 'high', 'urgent']
    if data['priority'] not in valid_priorities:
        return jsonify({'error': 'Invalid priority'}), 400
    
    try:
        ticket_controller = TicketController()
        ticket = ticket_controller.update_ticket_status(
            ticket_id, 
            priority=data['priority']
        )
        return jsonify({
            'message': 'Priority updated successfully',
            'ticket': ticket.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400