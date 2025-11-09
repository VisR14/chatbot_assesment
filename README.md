# AI Chat Portal with Conversation Intelligence

A full-stack web application that enables intelligent chat management and conversation analysis using AI. Built with Django REST Framework and React.

## 🚀 Features

### Core Features
- **Real-time Chat Interface**: Interactive conversation with LLM (OpenAI, Claude, Gemini, or LM Studio)
- **Conversation Management**: Store, organize, and archive chats with full message history
- **Conversation Intelligence**: Ask questions about past conversations using natural language
- **Semantic Search**: Find conversations by meaning, not just keywords
- **AI Analysis**: Automatic summaries, topic extraction, sentiment analysis, and key points
- **Modern UI**: Clean, responsive interface with dark mode support

### Technical Highlights
- RESTful API architecture with Django REST Framework
- PostgreSQL database with optimized queries and indexing
- AI-powered natural language processing
- React with Tailwind CSS for beautiful, responsive UI
- Support for multiple AI providers (OpenAI, Anthropic, Gemini, LM Studio)
- Comprehensive conversation intelligence features

## 📋 Tech Stack

### Backend
- **Framework**: Django 4.2.7 with Django REST Framework
- **Database**: PostgreSQL
- **AI Integration**: OpenAI API / Anthropic Claude / Google Gemini / LM Studio

### Frontend
- **Framework**: React 18.2 with Vite
- **Styling**: Tailwind CSS 3.3
- **Routing**: React Router DOM 6
- **HTTP Client**: Axios
- **Icons**: React Icons

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐
│  React Frontend │ ◄─────► │ Django REST API  │
│  (Port 3000)    │  HTTP   │  (Port 8000)     │
└─────────────────┘         └──────────────────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │   PostgreSQL DB  │
                            └──────────────────┘
                                      │
                                      ▼
                            ┌──────────────────┐
                            │   AI Provider    │
                            │  (OpenAI/Claude/ │
                            │  Gemini/LMStudio)│
                            └──────────────────┘
```

## 📦 Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Git

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the example .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env and add your configuration
# - Database credentials
# - AI provider choice
# - API keys (if using cloud AI providers)
```

5. **Create PostgreSQL database**
```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE chat_portal_db;

-- Exit
\q
```

6. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser (optional, for admin panel)**
```bash
python manage.py createsuperuser
```

8. **Start the backend server**
```bash
python manage.py runserver
```

Backend will be running at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
npm run dev
```

Frontend will be running at `http://localhost:3000`

### Using LM Studio (Local LLM)

If you prefer to use a local LLM instead of cloud APIs:

1. **Download and install LM Studio** from https://lmstudio.ai/
2. **Download a model** (e.g., Llama, Mistral)
3. **Start the local server** in LM Studio (usually on port 1234)
4. **Set environment variables** in `.env`:
```
AI_PROVIDER=lmstudio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
```

## 🎯 Usage

### Starting a Conversation
1. Navigate to the **Chat** page
2. Click "New Chat" to start a conversation
3. Type your message and press Send
4. The AI will respond in real-time
5. Click "End Conversation" when finished to generate analysis

### Viewing Conversations
1. Go to the **Conversations** page
2. Browse all your past conversations
3. Use search and filters to find specific conversations
4. Click on any conversation to view full details including:
   - Complete message history
   - AI-generated summary
   - Extracted topics and key points
   - Sentiment analysis

### Querying Conversations
1. Navigate to the **Intelligence** page
2. Ask natural language questions like:
   - "What did I discuss about travel last week?"
   - "Show me conversations about technology"
   - "What decisions did I make yesterday?"
3. Optionally filter by date range
4. View AI-generated answers with relevant conversation excerpts

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Endpoints

#### 1. Get All Conversations
```http
GET /api/conversations/
```

**Query Parameters:**
- `status` (optional): Filter by status ('active' or 'ended')
- `search` (optional): Search in title and summary

**Response:**
```json
{
  "success": true,
  "count": 10,
  "conversations": [
    {
      "id": 1,
      "title": "Trip Planning",
      "status": "ended",
      "start_timestamp": "2024-01-15T10:30:00Z",
      "end_timestamp": "2024-01-15T11:00:00Z",
      "message_count": 12,
      "duration": 1800,
      "topics": ["travel", "Japan", "itinerary"],
      "sentiment": "positive"
    }
  ]
}
```

#### 2. Get Specific Conversation
```http
GET /api/conversations/{id}/
```

**Response:**
```json
{
  "success": true,
  "conversation": {
    "id": 1,
    "title": "Trip Planning",
    "status": "ended",
    "summary": "Discussion about planning a trip to Japan...",
    "topics": ["travel", "Japan"],
    "key_points": ["Book flights by next week", "Research hotels in Tokyo"],
    "sentiment": "positive",
    "messages": [
      {
        "id": 1,
        "content": "I want to plan a trip to Japan",
        "sender": "user",
        "timestamp": "2024-01-15T10:30:00Z"
      }
    ]
  }
}
```

#### 3. Create New Conversation
```http
POST /api/conversations/
Content-Type: application/json

{
  "title": "New Conversation"
}
```

**Response:**
```json
{
  "success": true,
  "conversation": {
    "id": 2,
    "title": "New Conversation",
    "status": "active"
  }
}
```

#### 4. Send Message
```http
POST /api/conversations/send_message/
Content-Type: application/json

{
  "conversation_id": 1,
  "message": "Hello, how can you help me?"
}
```

**Response:**
```json
{
  "success": true,
  "user_message": {
    "id": 10,
    "content": "Hello, how can you help me?",
    "sender": "user",
    "timestamp": "2024-01-15T10:35:00Z"
  },
  "ai_response": {
    "id": 11,
    "content": "Hello! I'm here to assist you...",
    "sender": "ai",
    "timestamp": "2024-01-15T10:35:02Z",
    "tokens_used": 150,
    "model_used": "gpt-3.5-turbo"
  }
}
```

#### 5. End Conversation
```http
POST /api/conversations/end_conversation/
Content-Type: application/json

{
  "conversation_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "conversation": {
    "id": 1,
    "status": "ended",
    "summary": "User discussed planning a trip to Japan...",
    "topics": ["travel", "Japan", "planning"],
    "sentiment": "positive",
    "key_points": ["Book flights", "Research hotels"]
  }
}
```

#### 6. Query Conversations
```http
POST /api/conversations/query_conversations/
Content-Type: application/json

{
  "query": "What did I discuss about travel?",
  "date_from": "2024-01-01T00:00:00Z",
  "date_to": "2024-01-31T23:59:59Z",
  "limit": 5
}
```

**Response:**
```json
{
  "success": true,
  "query": "What did I discuss about travel?",
  "answer": "Based on your conversations, you discussed planning a trip to Japan...",
  "relevant_conversations": [
    {
      "id": 1,
      "title": "Trip Planning",
      "summary": "...",
      "messages": []
    }
  ],
  "count": 1
}
```

## 🗂️ Database Schema

### Conversations Table
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    status VARCHAR(10) DEFAULT 'active',
    start_timestamp TIMESTAMP DEFAULT NOW(),
    end_timestamp TIMESTAMP NULL,
    summary TEXT,
    topics JSONB DEFAULT '[]',
    key_points JSONB DEFAULT '[]',
    sentiment VARCHAR(50),
    embedding JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Messages Table
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    sender VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    tokens_used INTEGER,
    model_used VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 📸 Screenshots

### Chat Interface
![Chat Interface](docs/screenshots/chat-interface.png)
*Real-time chat with AI featuring message history and conversation management*

### Conversations Dashboard
![Conversations Dashboard](docs/screenshots/conversations-dashboard.png)
*Browse and search through all conversations with filtering options*

### Conversation Intelligence
![Conversation Intelligence](docs/screenshots/intelligence-page.png)
*Query past conversations using natural language*

### Dark Mode
![Dark Mode](docs/screenshots/dark-mode.png)
*Beautiful dark mode support throughout the application*

## 🔧 Configuration

### AI Provider Configuration

#### OpenAI
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

#### Anthropic Claude
```env
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

#### Google Gemini
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=...
```

#### LM Studio (Local)
```env
AI_PROVIDER=lmstudio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
```

## 🧪 Sample Conversations

The repository includes sample conversation data for testing. To load sample data:

```bash
cd backend
python manage.py loaddata sample_conversations.json
```

## 🚀 Deployment

### Backend Deployment (Production)

1. **Set DEBUG=False** in settings.py
2. **Configure production database**
3. **Set up environment variables** securely
4. **Collect static files**:
```bash
python manage.py collectstatic
```
5. **Use Gunicorn** as WSGI server:
```bash
gunicorn chat_portal.wsgi:application
```

### Frontend Deployment

1. **Build the production bundle**:
```bash
npm run build
```
2. **Serve the `dist` folder** using a web server (Nginx, Apache, etc.)

## 🤝 Contributing

This is an assignment project. For any questions, contact: devgods99@gmail.com

## 📝 License

This project is created as part of a technical assessment.

## 🎨 Code Quality

- **Clean Code**: Well-structured, readable code with proper comments
- **OOP Principles**: Object-oriented design throughout the application
- **Error Handling**: Comprehensive error handling and validation
- **Responsive Design**: Mobile-friendly UI with Tailwind CSS
- **Performance**: Optimized queries and efficient data fetching

## 🔍 Testing the Application

### Manual Testing Checklist

1. **Chat Interface**
   - [ ] Create new conversation
   - [ ] Send messages and receive AI responses
   - [ ] View message history
   - [ ] End conversation and verify analysis

2. **Conversations Dashboard**
   - [ ] View all conversations
   - [ ] Search conversations
   - [ ] Filter by status
   - [ ] View conversation details

3. **Conversation Intelligence**
   - [ ] Query past conversations
   - [ ] Apply date filters
   - [ ] View relevant results
   - [ ] Test different query types

4. **Dark Mode**
   - [ ] Toggle dark mode
   - [ ] Verify all pages support dark mode
   - [ ] Check readability and contrast

## 📞 Support

For questions or issues:
- Email: devgods99@gmail.com
- Submit issues via the assignment portal

## 🌟 Bonus Features Implemented

- ✅ Dark mode toggle
- ✅ Clean, modern UI with smooth animations
- ✅ Conversation search and filtering
- ✅ Real-time message updates
- ✅ Comprehensive conversation analytics
- ✅ Multiple AI provider support
- ✅ Responsive design for all screen sizes

---

**Built with ❤️ for the Full Stack Developer Assessment**

