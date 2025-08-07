from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

from config import Config
from models import db
# Import models to ensure they are registered with SQLAlchemy
from models.user import User
from models.ticket import Ticket
from routes.user import user_blueprint
from routes.admin import admin_blueprint
from routes.dialogflow_webhook import dialogflow_webhook

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS for frontend integration
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

db.init_app(app)

# Health check endpoint
@app.route('/health')
def health_check():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy', 
            'message': 'SupportBot AI Backend is running',
            'database': 'connected',
            'timestamp': '2024-01-01T00:00:00Z'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'message': 'Backend is running but database connection failed',
            'error': str(e)
        }), 500

# Root endpoint
@app.route('/')
def root():
    return jsonify({
        'message': 'SupportBot AI Backend API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'user': '/user/*',
            'admin': '/admin/*',
            'api': '/api/*'
        }
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(error):
    logger.error(f"Unhandled exception: {str(error)}")
    return jsonify({'error': 'An unexpected error occurred'}), 500

# Register blueprints
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(dialogflow_webhook, url_prefix="/api")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tables in app.db
    logger.info("Starting SupportBot AI Backend on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)