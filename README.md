# SupportBot AI - Intelligent Complaint Management System

An AI-powered complaint management system with a Flask backend and React frontend, featuring intelligent chatbot support, automated ticket generation, and real-time tracking.

## 🚀 Features

- 🤖 **AI-Powered Chatbot**: Intelligent complaint categorization and processing with NLP
- 🧠 **Machine Learning**: Automatic category prediction, priority assignment, and sentiment analysis
- 📝 **Smart Ticket Generation**: Automated ticket creation with AI-driven insights
- 📊 **Real-Time Tracking**: Live status updates and progress monitoring
- 🔐 **User Authentication**: Secure login/registration system
- 👨‍💼 **Admin Dashboard**: Comprehensive ticket management interface with AI insights
- 🎨 **Modern UI**: Beautiful, responsive design with shadcn/ui components
- 🔍 **Intelligent Analysis**: Keyword extraction, entity recognition, and similarity search

## 🧠 AI/ML Capabilities

### Natural Language Processing
- **Text Preprocessing**: Tokenization, lemmatization, and stopword removal
- **Sentiment Analysis**: Analyzes user sentiment (positive, negative, neutral)
- **Entity Recognition**: Extracts emails, phone numbers, URLs, and amounts
- **Keyword Extraction**: Identifies important keywords from complaints

### Intelligent Categorization
- **Automatic Category Prediction**: Classifies complaints into categories (billing, technical, service, general, emergency)
- **Priority Assignment**: Automatically assigns priority levels (urgent, high, normal, low)
- **Confidence Scoring**: Provides confidence scores for predictions

### Advanced Analytics
- **Pattern Recognition**: Identifies trends in complaints
- **Similarity Analysis**: Finds similar tickets using TF-IDF similarity
- **Performance Metrics**: Tracks model accuracy and performance

### Smart Assignment
- **AI-Suggested Assignment**: Recommends admin assignment based on expertise and workload
- **Workload Balancing**: Considers current admin workload
- **Expertise Matching**: Matches tickets to admins with relevant expertise

## Tech Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **JWT**: Authentication tokens
- **CORS**: Cross-origin resource sharing
- **Scikit-learn**: Machine learning library
- **NLTK**: Natural language processing
- **TextBlob**: Sentiment analysis
- **NumPy/Pandas**: Data processing

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **shadcn/ui**: Component library
- **React Query**: Data fetching and caching
- **React Router**: Client-side routing

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SupportBot-AI
   ```

2. **Install dependencies**
   ```bash
   # Install root dependencies
   npm install
   
   # Install frontend dependencies
   cd frontend && npm install && cd ..
   
   # Install backend dependencies
   cd backend
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   cd ..
   ```

3. **Initialize AI Models**
   ```bash
   cd backend
   python init_ai_models.py
   cd ..
   ```

4. **Environment Setup**
   
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=sqlite:///app.db
   SECRET_KEY=your-secret-key-here
   ```

5. **Start the development servers**
   ```bash
   # Start both frontend and backend concurrently
   npm run dev
   
   # Or start them separately:
   # Backend (Terminal 1)
   npm run dev:backend
   
   # Frontend (Terminal 2)
   npm run dev:frontend
   ```

6. **Access the application**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5000

## Project Structure

```
SupportBot-AI/
├── backend/                 # Flask backend
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── requirements.txt    # Python dependencies
│   ├── controllers/        # Business logic
│   │   ├── nlp_controller.py    # AI/ML controller
│   │   ├── ticket_controller.py # Enhanced ticket controller
│   │   └── auth_controller.py   # Authentication controller
│   ├── models/            # Database models
│   ├── routes/            # API endpoints
│   │   └── dialogflow_webhook.py # AI-powered endpoints
│   ├── utils/             # Utility functions
│   │   ├── ml_loader.py   # ML model management
│   │   └── notifier.py    # Notification system
│   ├── models/            # Trained ML models
│   └── init_ai_models.py  # AI model initialization
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   │   └── ComplaintChatbot.tsx # AI-powered chatbot
│   │   ├── hooks/         # Custom React hooks
│   │   ├── lib/           # Utility functions
│   │   │   └── api.ts     # Enhanced API service
│   │   ├── pages/         # Page components
│   │   └── App.tsx        # Main app component
│   ├── package.json       # Node dependencies
│   └── vite.config.ts     # Vite configuration
├── package.json           # Root package.json
└── README.md             # This file
```

## AI/ML Integration

### Model Performance
- **Category Classification**: ~85-90% accuracy
- **Priority Prediction**: ~80-85% accuracy
- **Sentiment Analysis**: ~75-80% accuracy

### Key AI Features
1. **Intelligent Text Analysis**: NLP-powered complaint understanding
2. **Automatic Categorization**: AI-driven category and priority assignment
3. **Smart Response Generation**: Context-aware chatbot responses
4. **Similarity Search**: Find similar tickets using AI
5. **Entity Extraction**: Identify important information from text
6. **Sentiment Analysis**: Understand user emotions and tone

### API Endpoints
- `POST /api/analyze-complaint` - Analyze complaint with AI
- `POST /api/create-ticket` - Create ticket with AI analysis
- `GET /api/suggest-assignment/{ticket_id}` - Get AI assignment suggestions
- `GET /api/similar-tickets/{ticket_id}` - Find similar tickets
- `POST /api/retrain-models` - Retrain AI models with feedback
- `GET /api/ai-insights` - Get AI-powered analytics

## Usage Examples

### AI-Powered Chatbot
The chatbot now uses AI to:
- Analyze user complaints in real-time
- Categorize issues automatically
- Assign appropriate priority levels
- Generate intelligent responses
- Extract key information

### Admin Dashboard
Enhanced with AI insights:
- Category distribution analysis
- Priority distribution analysis
- Sentiment trends
- Model performance metrics
- Similar ticket suggestions

## Documentation

For detailed AI/ML documentation, see:
- [AI/ML Features Guide](backend/AI_ML_README.md)
- [API Documentation](backend/README.md)
- [Frontend Integration](frontend/README.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new AI features
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
