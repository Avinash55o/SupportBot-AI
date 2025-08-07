from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models import db
import jwt
import datetime
import os

class AuthController:
    def __init__(self):
        self.secret_key = os.getenv('SECRET_KEY', 'your-secret-key')
    
    def register_user(self, name, email, password, is_admin=False):
        """Register a new user"""
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise Exception("User with this email already exists")
        
        # Create new user
        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=is_admin
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    def get_user_by_email(self, email):
        """Get user by email"""
        return User.query.filter_by(email=email).first()
    
    def check_password(self, user, password):
        """Check if password is correct for user"""
        return check_password_hash(user.password_hash, password)
    
    def login_user(self, email, password):
        """Login user and return JWT token"""
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            raise Exception("Invalid email or password")
        
        # Generate JWT token
        token = jwt.encode(
            {
                'user_id': user.id,
                'email': user.email,
                'is_admin': user.is_admin,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            },
            self.secret_key,
            algorithm='HS256'
        )
        
        return token
    
    def login_admin(self, email, password):
        """Login admin and return JWT token"""
        user = User.query.filter_by(email=email, is_admin=True).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            raise Exception("Invalid admin credentials")
        
        # Generate JWT token
        token = jwt.encode(
            {
                'user_id': user.id,
                'email': user.email,
                'is_admin': True,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            },
            self.secret_key,
            algorithm='HS256'
        )
        
        return token
    
    def verify_token(self, token):
        """Verify JWT token and return user data"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return User.query.get(user_id)

# Create instance for use in routes
authenticate_user = AuthController()
authenticate_admin = AuthController()