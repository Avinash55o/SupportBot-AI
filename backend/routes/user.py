from flask import Blueprint, request, jsonify
from controllers.auth_controller import authenticate_user
from controllers.ticket_controller import TicketController

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
        # Get user by email
        user = authenticate_user.get_user_by_email(data['email'])
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check password
        if not authenticate_user.check_password(user, data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate token
        token = authenticate_user.login_user(
            email=data['email'],
            password=data['password']
        )
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }), 200
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 401

@user_blueprint.route('/tickets', methods=['GET'])
def get_tickets():
    """Get all tickets for the logged-in user"""
    # Get user from token (implement token validation)
    user_id = request.args.get('user_id')  # In production, get from JWT token
    
    try:
        ticket_controller = TicketController()
        tickets = ticket_controller.get_user_tickets(user_id)
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
        ticket_controller = TicketController()
        ticket = ticket_controller.get_ticket_status(ticket_id, user_id)
        return jsonify(ticket.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404