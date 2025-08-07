import os
import pickle
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLLoader:
    def __init__(self, models_dir: str = "models"):
        """
        Initialize ML Loader with models directory
        
        Args:
            models_dir: Directory to store/load ML models
        """
        self.models_dir = models_dir
        self.vectorizer = None
        self.category_classifier = None
        self.priority_classifier = None
        self.lemmatizer = WordNetLemmatizer()
        
        # Create models directory if it doesn't exist
        os.makedirs(models_dir, exist_ok=True)
        
        # Download required NLTK data
        self._download_nltk_data()
        
        # Initialize or load models
        self._load_or_initialize_models()
    
    def _download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
    
    def _load_or_initialize_models(self):
        """Load existing models or initialize new ones"""
        vectorizer_path = os.path.join(self.models_dir, 'vectorizer.pkl')
        category_model_path = os.path.join(self.models_dir, 'category_classifier.pkl')
        priority_model_path = os.path.join(self.models_dir, 'priority_classifier.pkl')
        
        # Load or create vectorizer
        if os.path.exists(vectorizer_path):
            self.vectorizer = joblib.load(vectorizer_path)
            logger.info("Loaded existing vectorizer")
        else:
            self.vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            logger.info("Initialized new vectorizer")
        
        # Load or create category classifier
        if os.path.exists(category_model_path):
            self.category_classifier = joblib.load(category_model_path)
            logger.info("Loaded existing category classifier")
        else:
            self.category_classifier = MultinomialNB()
            logger.info("Initialized new category classifier")
        
        # Load or create priority classifier
        if os.path.exists(priority_model_path):
            self.priority_classifier = joblib.load(priority_model_path)
            logger.info("Loaded existing priority classifier")
        else:
            self.priority_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            logger.info("Initialized new priority classifier")
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for ML models
        
        Args:
            text: Input text to preprocess
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        stop_words = set(stopwords.words('english'))
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
        
        return ' '.join(tokens)
    
    def train_models(self, training_data: List[Dict]) -> Dict:
        """
        Train the ML models with provided data
        
        Args:
            training_data: List of dictionaries with 'text', 'category', 'priority' keys
            
        Returns:
            Dictionary with training results
        """
        if not training_data:
            logger.warning("No training data provided")
            return {"error": "No training data provided"}
        
        try:
            # Prepare data
            texts = [item.get('text', '') for item in training_data]
            categories = [item.get('category', 'general') for item in training_data]
            priorities = [item.get('priority', 'normal') for item in training_data]
            
            # Preprocess texts
            processed_texts = [self.preprocess_text(text) for text in texts]
            
            # Vectorize texts
            X = self.vectorizer.fit_transform(processed_texts)
            
            # Split data for training
            X_train, X_test, y_cat_train, y_cat_test = train_test_split(
                X, categories, test_size=0.2, random_state=42
            )
            _, _, y_pri_train, y_pri_test = train_test_split(
                X, priorities, test_size=0.2, random_state=42
            )
            
            # Train category classifier
            self.category_classifier.fit(X_train, y_cat_train)
            cat_predictions = self.category_classifier.predict(X_test)
            cat_accuracy = accuracy_score(y_cat_test, cat_predictions)
            
            # Train priority classifier
            self.priority_classifier.fit(X_train, y_pri_train)
            pri_predictions = self.priority_classifier.predict(X_test)
            pri_accuracy = accuracy_score(y_pri_test, pri_predictions)
            
            # Save models
            self._save_models()
            
            logger.info(f"Models trained successfully. Category accuracy: {cat_accuracy:.2f}, Priority accuracy: {pri_accuracy:.2f}")
            
            return {
                "success": True,
                "category_accuracy": cat_accuracy,
                "priority_accuracy": pri_accuracy,
                "training_samples": len(training_data)
            }
            
        except Exception as e:
            logger.error(f"Error training models: {str(e)}")
            return {"error": str(e)}
    
    def predict_category(self, text: str) -> Tuple[str, float]:
        """
        Predict category for given text
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (predicted_category, confidence_score)
        """
        try:
            processed_text = self.preprocess_text(text)
            if not processed_text:
                return "general", 0.0
            
            X = self.vectorizer.transform([processed_text])
            prediction = self.category_classifier.predict(X)[0]
            confidence = np.max(self.category_classifier.predict_proba(X))
            
            return prediction, confidence
        except Exception as e:
            logger.error(f"Error predicting category: {str(e)}")
            return "general", 0.0
    
    def predict_priority(self, text: str) -> Tuple[str, float]:
        """
        Predict priority for given text
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (predicted_priority, confidence_score)
        """
        try:
            processed_text = self.preprocess_text(text)
            if not processed_text:
                return "normal", 0.0
            
            X = self.vectorizer.transform([processed_text])
            prediction = self.priority_classifier.predict(X)[0]
            confidence = np.max(self.priority_classifier.predict_proba(X))
            
            return prediction, confidence
        except Exception as e:
            logger.error(f"Error predicting priority: {str(e)}")
            return "normal", 0.0
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of the text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with sentiment analysis results
        """
        try:
            from textblob import TextBlob
            
            blob = TextBlob(text)
            sentiment_score = blob.sentiment.polarity
            
            if sentiment_score > 0.1:
                sentiment = "positive"
            elif sentiment_score < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            return {
                "sentiment": sentiment,
                "score": sentiment_score,
                "subjectivity": blob.sentiment.subjectivity
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {"sentiment": "neutral", "score": 0.0, "subjectivity": 0.0}
    
    def extract_keywords(self, text: str, top_k: int = 5) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text: Input text
            top_k: Number of top keywords to return
            
        Returns:
            List of keywords
        """
        try:
            processed_text = self.preprocess_text(text)
            if not processed_text:
                return []
            
            # Use TF-IDF to extract keywords
            X = self.vectorizer.transform([processed_text])
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get TF-IDF scores
            tfidf_scores = X.toarray()[0]
            
            # Get top keywords
            top_indices = np.argsort(tfidf_scores)[-top_k:][::-1]
            keywords = [feature_names[i] for i in top_indices if tfidf_scores[i] > 0]
            
            return keywords
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []
    
    def _save_models(self):
        """Save trained models to disk"""
        try:
            joblib.dump(self.vectorizer, os.path.join(self.models_dir, 'vectorizer.pkl'))
            joblib.dump(self.category_classifier, os.path.join(self.models_dir, 'category_classifier.pkl'))
            joblib.dump(self.priority_classifier, os.path.join(self.models_dir, 'priority_classifier.pkl'))
            logger.info("Models saved successfully")
        except Exception as e:
            logger.error(f"Error saving models: {str(e)}")
    
    def get_model_info(self) -> Dict:
        """Get information about the current models"""
        return {
            "vectorizer_features": len(self.vectorizer.get_feature_names_out()) if self.vectorizer else 0,
            "category_classes": self.category_classifier.classes_.tolist() if self.category_classifier else [],
            "priority_classes": self.priority_classifier.classes_.tolist() if self.priority_classifier else [],
            "models_loaded": all([self.vectorizer, self.category_classifier, self.priority_classifier])
        }
