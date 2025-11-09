# Setup Instructions - AI Chat Portal

Complete step-by-step guide to set up and run the AI Chat Portal application.

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.9 or higher** - [Download](https://www.python.org/downloads/)
- **Node.js 16 or higher** - [Download](https://nodejs.org/)
- **PostgreSQL 12 or higher** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Code Editor** (VS Code recommended) - [Download](https://code.visualstudio.com/)

Optional:
- **LM Studio** (for local LLM) - [Download](https://lmstudio.ai/)

---

## Part 1: Database Setup

### Step 1: Install PostgreSQL

1. Download and install PostgreSQL for your operating system
2. During installation, remember the password you set for the `postgres` user
3. Ensure PostgreSQL service is running

### Step 2: Create Database

**Option A: Using pgAdmin (GUI)**
1. Open pgAdmin
2. Connect to your PostgreSQL server
3. Right-click on "Databases" → "Create" → "Database"
4. Name: `chat_portal_db`
5. Click "Save"

**Option B: Using Command Line**
```bash
# Windows
psql -U postgres

# Linux/Mac
sudo -u postgres psql

# Then run:
CREATE DATABASE chat_portal_db;
\q
```

### Step 3: Verify Database
```bash
psql -U postgres -l
```
You should see `chat_portal_db` in the list.

---

## Part 2: Backend Setup (Django)

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Django and Django REST Framework
- PostgreSQL adapter (psycopg2)
- AI libraries (OpenAI, Anthropic, Google Generative AI)
- Other utilities

### Step 4: Configure Environment Variables

1. Create a `.env` file in the `backend` directory:
```bash
# Windows
copy env_example.txt .env

# Linux/Mac
cp env_example.txt .env
```

2. Edit `.env` file with your configuration:
```env
# Database Configuration
DB_NAME=chat_portal_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password_here
DB_HOST=localhost
DB_PORT=5432

# AI Provider Configuration
AI_PROVIDER=openai

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
```

**Getting API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Google Gemini: https://makersuite.google.com/app/apikey

**OR use LM Studio (No API key needed):**
```env
AI_PROVIDER=lmstudio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

Expected output:
```
Applying conversations.0001_initial... OK
Applying auth.0001_initial... OK
...
```

### Step 6: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```
Follow prompts to create admin account.

### Step 7: Start Backend Server
```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
```

**Test it:** Open browser to `http://localhost:8000/api/conversations/`

You should see the API response!

---

## Part 3: Frontend Setup (React)

### Step 1: Open New Terminal

Keep the backend server running. Open a new terminal window.

### Step 2: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 3: Install Dependencies
```bash
npm install
```

This will install:
- React and React Router
- Tailwind CSS
- Axios
- Other dependencies

**Note:** This may take a few minutes.

### Step 4: Start Frontend Development Server
```bash
npm run dev
```

Expected output:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Step 5: Open Application

Open your browser to: `http://localhost:3000`

You should see the AI Chat Portal interface!

---

## Part 4: Using LM Studio (Optional - Local LLM)

If you want to use a local LLM instead of cloud APIs:

### Step 1: Download LM Studio
1. Go to https://lmstudio.ai/
2. Download for your operating system
3. Install LM Studio

### Step 2: Download a Model
1. Open LM Studio
2. Click "Search" tab
3. Search for a model (e.g., "llama-2-7b-chat" or "mistral-7b")
4. Click download (choose GGUF format)
5. Wait for download to complete

### Step 3: Start Local Server
1. In LM Studio, click "Local Server" tab
2. Select the downloaded model
3. Click "Start Server"
4. Server will start on `http://localhost:1234`

### Step 4: Configure Backend
Edit `backend/.env`:
```env
AI_PROVIDER=lmstudio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
```

Restart the Django server.

---

## Part 5: Verification & Testing

### Test Backend API

**Test 1: Create Conversation**
```bash
curl -X POST http://localhost:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Chat"}'
```

**Test 2: Send Message**
```bash
curl -X POST http://localhost:8000/api/conversations/send_message/ \
  -H "Content-Type: application/json" \
  -d '{"conversation_id":1,"message":"Hello!"}'
```

### Test Frontend

1. **Chat Interface** (`http://localhost:3000/`)
   - Click "New Chat"
   - Type a message and press Send
   - Verify AI responds

2. **Conversations Dashboard** (`http://localhost:3000/conversations`)
   - View created conversations
   - Click on a conversation to view details

3. **Intelligence Page** (`http://localhost:3000/intelligence`)
   - Enter a query like "What did I discuss?"
   - Click "Search Conversations"

---

## Part 6: Admin Panel (Optional)

Django provides an admin panel to view and manage data.

1. **Access Admin Panel:** `http://localhost:8000/admin/`
2. **Login:** Use the superuser credentials you created
3. **View Data:** Browse Conversations and Messages

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'X'"
**Solution:**
```bash
# Activate virtual environment
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies again
pip install -r requirements.txt
```

### Issue: "psycopg2 installation error"
**Solution (Windows):**
```bash
pip install psycopg2-binary
```

### Issue: "Database connection failed"
**Solution:**
1. Check PostgreSQL is running:
   ```bash
   # Windows
   services.msc  # Look for "postgresql" service
   
   # Linux
   sudo systemctl status postgresql
   ```
2. Verify database credentials in `.env`
3. Test database connection:
   ```bash
   psql -U postgres -d chat_portal_db
   ```

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Issue: "npm install fails"
**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

### Issue: "AI API key error"
**Solution:**
1. Verify API key is correct in `.env`
2. Check API key has credits/quota
3. Test API key:
   ```python
   import openai
   openai.api_key = "your-key"
   openai.Model.list()
   ```

### Issue: "CORS error in browser"
**Solution:**
- Ensure Django backend is running
- Check `CORS_ALLOW_ALL_ORIGINS = True` in settings.py
- Clear browser cache

### Issue: "Frontend can't connect to backend"
**Solution:**
1. Verify backend is running on port 8000
2. Check proxy configuration in `frontend/vite.config.js`
3. Test API directly: `http://localhost:8000/api/conversations/`

---

## Running in Development

### Start Both Servers

**Terminal 1 (Backend):**
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
python manage.py runserver
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### Stop Servers
Press `Ctrl+C` in each terminal.

---

## Environment Configuration Summary

### Backend `.env` File
```env
# Required for Database
DB_NAME=chat_portal_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Required for AI
AI_PROVIDER=openai  # or anthropic, gemini, lmstudio
OPENAI_API_KEY=sk-...  # Only if using OpenAI
```

### Ports Used
- **Backend:** 8000 (Django)
- **Frontend:** 3000 (Vite/React)
- **Database:** 5432 (PostgreSQL)
- **LM Studio:** 1234 (if using local LLM)

---

## Next Steps

1. ✅ Both servers running
2. ✅ Can create conversations
3. ✅ AI responds to messages
4. ✅ Can view past conversations
5. ✅ Can query conversations

Now you're ready to use the AI Chat Portal!

---

## Additional Resources

- **Django Docs:** https://docs.djangoproject.com/
- **React Docs:** https://react.dev/
- **Tailwind CSS:** https://tailwindcss.com/docs
- **OpenAI API:** https://platform.openai.com/docs
- **LM Studio:** https://lmstudio.ai/docs

---

## Support

For issues or questions:
- Check the troubleshooting section above
- Review error messages carefully
- Email: devgods99@gmail.com

---

**Setup Complete! Happy Coding! 🚀**

