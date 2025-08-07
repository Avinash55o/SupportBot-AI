from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from config import Config
from models import db
from routes.user import user_blueprint
from routes.admin import admin_blueprint
from routes.dialogflow_webhook import dialogflow_webhook

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS for frontend integration
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8080", "http://127.0.0.1:8080"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

db.init_app(app)

# Health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'SupportBot AI Backend is running'}, 200

# Register blueprints
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(dialogflow_webhook, url_prefix="/api")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tables in app.db
    app.run(port=5000)