#!/usr/bin/env python3
"""
Setup script for chatbot functionality
Initializes AI models and ensures everything is ready
"""
import os
import sys
import time
import requests
from utils.ml_loader import MLLoader
from models import db
from models.user import User
from models.ticket import Ticket
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def setup_database():
    """Setup database and create sample data"""
    print("🗄️  Setting up database...")
    
    try:
        # Create tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if users exist
        user_count = User.query.count()
        if user_count == 0:
            print("📝 Creating sample users...")
            
            # Create admin user
            admin_user = User(
                name='Admin User',
                email='admin@supportbot.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin_user)
            
            # Create regular users
            user1 = User(
                name='John Doe',
                email='john@example.com',
                password_hash=generate_password_hash('user123'),
                is_admin=False
            )
            db.session.add(user1)
            
            user2 = User(
                name='Jane Smith',
                email='jane@example.com',
                password_hash=generate_password_hash('user123'),
                is_admin=False
            )
            db.session.add(user2)
            
            db.session.commit()
            print("✅ Sample users created")
            
            # Create sample tickets
            print("📋 Creating sample tickets...")
            tickets = [
                Ticket(
                    issue_type='Technical Support',
                    description='Unable to login to my account. Getting "Invalid credentials" error.',
                    status='open',
                    priority='high',
                    user_id=user1.id,
                    notes='User reported login issues with error message',
                    created_at=datetime.now() - timedelta(days=2)
                ),
                Ticket(
                    issue_type='Billing',
                    description='I was charged twice for my subscription this month.',
                    status='in_progress',
                    priority='normal',
                    user_id=user1.id,
                    notes='Double charge issue - investigating payment records',
                    created_at=datetime.now() - timedelta(days=1)
                ),
                Ticket(
                    issue_type='Feature Request',
                    description='Would like to see a dark mode option in the mobile app.',
                    status='open',
                    priority='low',
                    user_id=user2.id,
                    notes='User requested dark mode feature for mobile app',
                    created_at=datetime.now() - timedelta(hours=6)
                ),
            ]
            
            for ticket in tickets:
                db.session.add(ticket)
            
            db.session.commit()
            print("✅ Sample tickets created")
            
        else:
            print(f"✅ Found {user_count} existing users")
            
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def setup_ai_models():
    """Setup AI models with sample training data"""
    print("🤖 Setting up AI models...")
    
    try:
        # Initialize ML loader
        ml_loader = MLLoader()
        print("✅ ML Loader initialized")
        
        # Sample training data
        training_data = [
            # Technical Support
            {"text": "I can't login to my account", "category": "Technical Support", "priority": "high"},
            {"text": "Login not working", "category": "Technical Support", "priority": "high"},
            {"text": "Password reset not working", "category": "Technical Support", "priority": "high"},
            {"text": "App crashes when I open it", "category": "Technical Support", "priority": "urgent"},
            {"text": "Website is down", "category": "Technical Support", "priority": "urgent"},
            {"text": "Can't access my dashboard", "category": "Technical Support", "priority": "normal"},
            {"text": "Slow loading times", "category": "Technical Support", "priority": "normal"},
            
            # Billing
            {"text": "I was charged twice", "category": "Billing", "priority": "high"},
            {"text": "Wrong amount charged", "category": "Billing", "priority": "high"},
            {"text": "Need refund", "category": "Billing", "priority": "normal"},
            {"text": "Billing question", "category": "Billing", "priority": "low"},
            {"text": "Payment method not working", "category": "Billing", "priority": "normal"},
            {"text": "Subscription renewal issue", "category": "Billing", "priority": "normal"},
            
            # Feature Request
            {"text": "Would like dark mode", "category": "Feature Request", "priority": "low"},
            {"text": "Need new feature", "category": "Feature Request", "priority": "low"},
            {"text": "Can you add mobile app", "category": "Feature Request", "priority": "normal"},
            {"text": "Request for new functionality", "category": "Feature Request", "priority": "low"},
            
            # General Support
            {"text": "How do I use this feature", "category": "General Support", "priority": "low"},
            {"text": "Need help with setup", "category": "General Support", "priority": "normal"},
            {"text": "Question about service", "category": "General Support", "priority": "low"},
            {"text": "General inquiry", "category": "General Support", "priority": "low"},
        ]
        
        # Train models
        print("🧠 Training AI models...")
        training_result = ml_loader.train_models(training_data)
        print(f"✅ Models trained successfully")
        print(f"   Category accuracy: {training_result.get('category_accuracy', 'N/A')}")
        print(f"   Priority accuracy: {training_result.get('priority_accuracy', 'N/A')}")
        
        # Test models
        print("🧪 Testing AI models...")
        test_text = "I can't login to my account and this is urgent!"
        category, cat_conf = ml_loader.predict_category(test_text)
        priority, pri_conf = ml_loader.predict_priority(test_text)
        sentiment = ml_loader.analyze_sentiment(test_text)
        keywords = ml_loader.extract_keywords(test_text)
        
        print(f"✅ Test prediction successful:")
        print(f"   Category: {category} ({cat_conf:.2%})")
        print(f"   Priority: {priority} ({pri_conf:.2%})")
        print(f"   Sentiment: {sentiment['sentiment']} (score: {sentiment['score']:.2f})")
        print(f"   Keywords: {', '.join(keywords[:3])}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI model setup failed: {e}")
        return False

def test_backend_endpoints():
    """Test backend endpoints"""
    print("🔗 Testing backend endpoints...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test analyze complaint endpoint
        test_data = {"text": "I can't login to my account"}
        response = requests.post(
            "http://localhost:5000/api/analyze-complaint",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Analyze complaint endpoint working")
        else:
            print(f"❌ Analyze complaint endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Test create ticket endpoint
        test_data = {"description": "Test ticket creation", "user_id": 1}
        response = requests.post(
            "http://localhost:5000/api/create-ticket",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 201:
            print("✅ Create ticket endpoint working")
        else:
            print(f"❌ Create ticket endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Please start the backend first.")
        return False
    except Exception as e:
        print(f"❌ Endpoint testing failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Chatbot System")
    print("=" * 50)
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed. Exiting.")
        return
    
    # Setup AI models
    if not setup_ai_models():
        print("❌ AI model setup failed. Exiting.")
        return
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the backend: python app.py")
    print("2. Start the frontend: cd frontend && npm run dev")
    print("3. Open http://localhost:8080 in your browser")
    print("4. Login with: admin@supportbot.com / admin123")
    print("5. Test the chatbot functionality")
    
    # Test endpoints if backend is running
    print("\n🔍 Testing endpoints...")
    time.sleep(2)
    test_backend_endpoints()

if __name__ == "__main__":
    # Import Flask app context
    from app import app
    
    with app.app_context():
        main()
