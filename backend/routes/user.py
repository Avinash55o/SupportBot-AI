from flask import Blueprint, request, jsonify
from controllers.auth_controller import authenticate_user
from controllers.ticket_controller import get_user_tickets, get_ticket_status

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(k in data for k in ['name', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Call auth controller to register user
        user = authenticate_user.register_user(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user.id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_blueprint.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Email and password required'}), 400
    
    try:
        token = authenticate_user.login_user(
            email=data['email'],
            password=data['password']
        )
        return jsonify({
            'message': 'Login successful',
            'token': token
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@user_blueprint.route('/tickets', methods=['GET'])
def get_tickets():
    """Get all tickets for the logged-in user"""
    # Get user from token (implement token validation)
    user_id = request.args.get('user_id')  # In production, get from JWT token
    
    try:
        tickets = get_user_tickets(user_id)
        return jsonify({
            'tickets': [ticket.to_dict() for ticket in tickets]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_blueprint.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """Get specific ticket details"""
    user_id = request.args.get('user_id')  # In production, get from JWT token
    
    try:
        ticket = get_ticket_status(ticket_id, user_id)
        return jsonify(ticket.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404