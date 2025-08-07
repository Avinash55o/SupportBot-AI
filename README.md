# SupportBot AI - Intelligent Complaint Management System

An AI-powered complaint management system with a Flask backend and React frontend, featuring intelligent chatbot support, automated ticket generation, and real-time tracking.

## Features

- 🤖 **AI-Powered Chatbot**: Intelligent complaint categorization and processing
- 📝 **Smart Ticket Generation**: Automated ticket creation with priority assignment
- 📊 **Real-Time Tracking**: Live status updates and progress monitoring
- 🔐 **User Authentication**: Secure login/registration system
- 👨‍💼 **Admin Dashboard**: Comprehensive ticket management interface
- 🎨 **Modern UI**: Beautiful, responsive design with shadcn/ui components

## Tech Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **JWT**: Authentication tokens
- **CORS**: Cross-origin resource sharing

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

3. **Environment Setup**
   
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=sqlite:///app.db
   SECRET_KEY=your-secret-key-here
   ```

4. **Start the development servers**
   ```bash
   # Start both frontend and backend concurrently
   npm run dev
   
   # Or start them separately:
   # Backend (Terminal 1)
   npm run dev:backend
   
   # Frontend (Terminal 2)
   npm run dev:frontend
   ```

5. **Access the application**
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
│   ├── models/            # Database models
│   ├── routes/            # API endpoints
│   └── utils/             # Utility functions
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── lib/           # Utility functions
│   │   ├── pages/         # Page components
│   │   └── App.tsx        # Main app component
│   ├── package.json       # Node dependencies
│   └── vite.config.ts     # Vite configuration
├── package.json           # Root package.json
└── README.md             # This file
```

## API Integration

The frontend and backend are fully integrated through a RESTful API:

### Authentication Endpoints
- `POST /user/register` - User registration
- `POST /user/login` - User login
- `POST /admin/login` - Admin login

### Ticket Management
- `GET /user/tickets` - Get user tickets
- `GET /admin/tickets` - Get all tickets (admin)
- `PUT /admin/tickets/{id}/status` - Update ticket status
- `PUT /admin/tickets/{id}/priority` - Update ticket priority

### Key Integration Features

1. **CORS Configuration**: Backend configured to accept requests from frontend
2. **Proxy Setup**: Vite dev server proxies API requests to Flask backend
3. **Authentication**: JWT tokens stored in localStorage
4. **Real-time Updates**: React Query for efficient data fetching and caching

## Development

### Backend Development
```bash
cd backend
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run Flask development server
python app.py
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Database
The application uses SQLite by default. The database file (`app.db`) is automatically created when you first run the backend.

## Production Deployment

### Backend
1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables
3. Use a production WSGI server (Gunicorn)
4. Set up reverse proxy (Nginx)

### Frontend
1. Build the application: `npm run build`
2. Serve static files with a web server
3. Configure API base URL for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details
