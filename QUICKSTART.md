# Quick Start Guide - AI Chat Portal

Get up and running in 10 minutes!

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 16+ installed
- [ ] PostgreSQL running
- [ ] AI API key (OpenAI/Claude/Gemini) OR LM Studio

---

## 5-Minute Setup

### Step 1: Database (2 minutes)

```bash
# Create database
psql -U postgres
CREATE DATABASE chat_portal_db;
\q
```

### Step 2: Backend (3 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy env_example.txt .env  # Windows
cp env_example.txt .env    # Linux/Mac

# Edit .env file - add your database password and AI API key
# Minimum required:
#   DB_PASSWORD=your_postgres_password
#   AI_PROVIDER=openai
#   OPENAI_API_KEY=your_api_key

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Backend running at: **http://localhost:8000** ✅

### Step 3: Frontend (2 minutes)

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend running at: **http://localhost:3000** ✅

---

## First Steps

1. **Open** `http://localhost:3000` in your browser
2. **Click** "New Chat" button
3. **Type** your first message
4. **Press** Send
5. **Wait** for AI response

Congratulations! 🎉 You're using the AI Chat Portal!

---

## Optional: Load Sample Data

```bash
cd backend
python sample_data.py
# Type 'yes' when prompted
```

This creates 4 sample conversations for testing.

---

## Troubleshooting Quick Fixes

### "Database connection failed"
```bash
# Check PostgreSQL is running
# Windows: services.msc → look for postgresql
# Linux: sudo systemctl status postgresql
```

### "AI API error"
- Check your API key in `.env`
- Verify you have credits/quota

### "Port already in use"
```bash
# Backend (port 8000)
# Kill the process using the port

# Frontend (port 3000)
npm run dev -- --port 3001  # Use different port
```

### "Module not found"
```bash
# Backend
cd backend
venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

## Using LM Studio (Local AI)

Don't have an API key? Use a local LLM!

1. **Download** [LM Studio](https://lmstudio.ai/)
2. **Install** and download a model
3. **Start** the local server (port 1234)
4. **Edit** `backend/.env`:
   ```
   AI_PROVIDER=lmstudio
   LM_STUDIO_BASE_URL=http://localhost:1234/v1
   ```
5. **Restart** Django server

---

## Test the API

```bash
# Test 1: List conversations
curl http://localhost:8000/api/conversations/

# Test 2: Create conversation
curl -X POST http://localhost:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test"}'

# Test 3: Send message
curl -X POST http://localhost:8000/api/conversations/send_message/ \
  -H "Content-Type: application/json" \
  -d '{"conversation_id":1,"message":"Hello!"}'
```

---

## Next Steps

- ✅ Create your first conversation
- ✅ End a conversation to see AI analysis
- ✅ Try the Intelligence page to query past chats
- ✅ Toggle dark mode
- ✅ Explore the Conversations Dashboard

---

## Common Commands

**Backend:**
```bash
python manage.py runserver     # Start server
python manage.py migrate        # Run migrations
python manage.py createsuperuser  # Create admin user
python sample_data.py          # Load sample data
```

**Frontend:**
```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
```

---

## Getting Help

1. Check **SETUP_INSTRUCTIONS.md** for detailed setup
2. Review **API_DOCUMENTATION.md** for API details
3. See **ARCHITECTURE.md** for system design
4. Email: devgods99@gmail.com

---

## Production Checklist

Before deploying:

- [ ] Change `SECRET_KEY` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Configure proper database
- [ ] Set up environment variables securely
- [ ] Use HTTPS
- [ ] Set up proper CORS
- [ ] Add authentication
- [ ] Configure rate limiting

---

**Time to First Message: < 10 minutes** ⚡

**Happy Chatting! 🚀**

