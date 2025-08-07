# 🚀 SupportBot AI - Demo Setup Guide

This guide will help you quickly set up and run the SupportBot AI application with dummy data for demonstration purposes.

## 📋 Prerequisites

- Python 3.8+ installed
- Node.js 18+ installed
- Git (for cloning the repository)

## 🛠️ Quick Setup

### Option 1: Windows (Recommended)
1. Double-click `start_demo.bat` in the project root
2. Wait for the setup to complete
3. Access the application at http://localhost:8080

### Option 2: Manual Setup

#### 1. Install Dependencies
```bash
# Install root dependencies
npm install

# Install frontend dependencies
cd frontend && npm install && cd ..

# Install backend dependencies
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
cd ..
```

#### 2. Start the Application
```bash
# Start both frontend and backend
npm run dev
```

#### 3. Populate Dummy Data
```bash
# In a new terminal, activate the virtual environment
cd backend
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Populate dummy data
curl -X POST http://localhost:5000/populate-dummy-data
```

## 👥 Demo Login Credentials

### Regular Users
- **Email:** john.smith@example.com
- **Password:** password123

- **Email:** sarah.johnson@example.com
- **Password:** password123

- **Email:** mike.wilson@example.com
- **Password:** password123

### Admin Users
- **Email:** admin@supportbot.com
- **Password:** admin123

- **Email:** manager@supportbot.com
- **Password:** manager123

## 🎯 What You'll See

### User Dashboard
- View your own tickets
- Create new tickets through the AI chatbot
- Track ticket status and progress
- Chat with the AI assistant

### Admin Dashboard
- View all tickets in the system
- Filter tickets by status, priority, and category
- Update ticket status and assign admins
- View AI-powered analytics and insights
- See category and priority distributions
- Access model performance metrics

### AI Chatbot Features
- Real-time complaint analysis
- Automatic categorization (billing, technical, service, general, emergency)
- Priority assignment (urgent, high, normal, low)
- Sentiment analysis
- Entity extraction (emails, phone numbers, etc.)
- Intelligent response generation

## 📊 Sample Data Included

The dummy data includes 15 realistic tickets across different categories:

### Billing Issues (3 tickets)
- Double billing problem (urgent, open)
- Payment method update (normal, in_progress)
- Incorrect charges dispute (high, open)

### Technical Issues (4 tickets)
- Login problems (urgent, resolved)
- System performance issues (high, in_progress)
- Mobile app crashes (normal, open)
- Feature not working (normal, closed)

### Service Issues (3 tickets)
- Customer service delays (high, open)
- Service quality feedback (normal, in_progress)
- Account cancellation request (normal, open)

### General Inquiries (3 tickets)
- Product information request (low, resolved)
- Feature request (low, open)
- General question (low, resolved)

### Emergency Issues (2 tickets)
- Security breach (urgent, in_progress)
- Data loss (urgent, open)

## 🔧 Troubleshooting

### Backend Issues
- Make sure the virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify the database is created: `python init_db.py`

### Frontend Issues
- Ensure Node.js dependencies are installed: `npm install`
- Check that the backend is running on port 5000
- Verify the frontend is running on port 8080

### Database Issues
- Delete `app.db` and restart to reset the database
- Run the populate endpoint again: `curl -X POST http://localhost:5000/populate-dummy-data`

## 🎉 Demo Tips

1. **Start with a Regular User**: Login as john.smith@example.com to see the user experience
2. **Try the AI Chatbot**: Create a new ticket through the chatbot to see AI analysis
3. **Switch to Admin**: Login as admin@supportbot.com to see the admin dashboard
4. **Explore Analytics**: Check out the charts and metrics in the admin dashboard
5. **Update Tickets**: Try changing ticket statuses to see the system in action

## 📞 Support

If you encounter any issues:
1. Check the console for error messages
2. Verify all services are running (backend on port 5000, frontend on port 8080)
3. Ensure the database is properly initialized
4. Try restarting the application

---

**Happy Demo! 🚀**
