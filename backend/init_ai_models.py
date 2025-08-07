#!/usr/bin/env python3
"""
Script to initialize AI models with sample training data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.ml_loader import MLLoader
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Initialize AI models with sample training data"""
    logger.info("Initializing AI models...")
    
    # Initialize ML loader
    ml_loader = MLLoader()
    
    # Sample training data
    training_data = [
        # Billing related complaints
        {"text": "I have a billing issue with my account", "category": "billing", "priority": "high"},
        {"text": "My payment was charged twice", "category": "billing", "priority": "urgent"},
        {"text": "I need to update my billing information", "category": "billing", "priority": "normal"},
        {"text": "Why was I charged extra fees", "category": "billing", "priority": "high"},
        {"text": "I want to cancel my subscription", "category": "billing", "priority": "normal"},
        {"text": "There's an error in my bill", "category": "billing", "priority": "high"},
        {"text": "I need a refund", "category": "billing", "priority": "urgent"},
        {"text": "My billing address is wrong", "category": "billing", "priority": "normal"},
        
        # Technical issues
        {"text": "The system is not working properly", "category": "technical", "priority": "high"},
        {"text": "I can't log into my account", "category": "technical", "priority": "urgent"},
        {"text": "The website is loading slowly", "category": "technical", "priority": "normal"},
        {"text": "I'm getting an error message", "category": "technical", "priority": "high"},
        {"text": "The app keeps crashing", "category": "technical", "priority": "high"},
        {"text": "I can't access my dashboard", "category": "technical", "priority": "urgent"},
        {"text": "The page is not loading", "category": "technical", "priority": "normal"},
        {"text": "There's a bug in the system", "category": "technical", "priority": "high"},
        {"text": "The feature is not working", "category": "technical", "priority": "normal"},
        
        # Service issues
        {"text": "I need help with customer service", "category": "service", "priority": "normal"},
        {"text": "The service quality is poor", "category": "service", "priority": "high"},
        {"text": "The support team is not responding", "category": "service", "priority": "urgent"},
        {"text": "I want to complain about the service", "category": "service", "priority": "high"},
        {"text": "The customer service is terrible", "category": "service", "priority": "high"},
        {"text": "I need better support", "category": "service", "priority": "normal"},
        {"text": "The service is not as advertised", "category": "service", "priority": "high"},
        {"text": "I want to speak to a manager", "category": "service", "priority": "normal"},
        
        # General inquiries
        {"text": "I have a question about your services", "category": "general", "priority": "low"},
        {"text": "Can you provide more information", "category": "general", "priority": "low"},
        {"text": "I want to know more about your products", "category": "general", "priority": "low"},
        {"text": "What are your business hours", "category": "general", "priority": "low"},
        {"text": "I need information about pricing", "category": "general", "priority": "low"},
        {"text": "Can you help me understand the features", "category": "general", "priority": "low"},
        {"text": "I'm interested in your services", "category": "general", "priority": "low"},
        {"text": "What are the benefits of your product", "category": "general", "priority": "low"},
        
        # Emergency/Urgent issues
        {"text": "This is an emergency situation", "category": "emergency", "priority": "urgent"},
        {"text": "I need immediate assistance", "category": "emergency", "priority": "urgent"},
        {"text": "This is critical and urgent", "category": "emergency", "priority": "urgent"},
        {"text": "I can't access my account and it's urgent", "category": "emergency", "priority": "urgent"},
        {"text": "This is affecting my business operations", "category": "emergency", "priority": "urgent"},
    ]
    
    logger.info(f"Training models with {len(training_data)} sample records...")
    
    # Train models
    result = ml_loader.train_models(training_data)
    
    if result.get("success"):
        logger.info("✅ AI models trained successfully!")
        logger.info(f"Category accuracy: {result.get('category_accuracy', 0):.2%}")
        logger.info(f"Priority accuracy: {result.get('priority_accuracy', 0):.2%}")
        logger.info(f"Training samples: {result.get('training_samples', 0)}")
    else:
        logger.error(f"❌ Failed to train models: {result.get('error', 'Unknown error')}")
        return 1
    
    # Test the models
    logger.info("Testing models with sample inputs...")
    
    test_cases = [
        "I have a billing problem with my account",
        "The website is not working properly",
        "I need help with customer service",
        "This is an urgent issue that needs immediate attention",
        "I just have a general question about your services"
    ]
    
    for test_case in test_cases:
        category, cat_conf = ml_loader.predict_category(test_case)
        priority, pri_conf = ml_loader.predict_priority(test_case)
        sentiment = ml_loader.analyze_sentiment(test_case)
        
        logger.info(f"Test: '{test_case}'")
        logger.info(f"  Category: {category} ({cat_conf:.2%})")
        logger.info(f"  Priority: {priority} ({pri_conf:.2%})")
        logger.info(f"  Sentiment: {sentiment['sentiment']} ({sentiment['score']:.2f})")
        logger.info("")
    
    logger.info("🎉 AI models initialization completed!")
    return 0

if __name__ == "__main__":
    exit(main())
