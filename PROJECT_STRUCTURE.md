# Project Structure - AI Chat Portal

## Directory Tree

```
chatbot_assessment/
│
├── backend/                          # Django REST Framework Backend
│   ├── chat_portal/                  # Main Django project
│   │   ├── __init__.py
│   │   ├── asgi.py                   # ASGI configuration
│   │   ├── wsgi.py                   # WSGI configuration
│   │   ├── settings.py               # Django settings (database, apps, middleware)
│   │   └── urls.py                   # Root URL configuration
│   │
│   ├── conversations/                # Conversations Django app
│   │   ├── __init__.py
│   │   ├── admin.py                  # Django admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── models.py                 # Database models (Conversation, Message)
│   │   ├── serializers.py            # DRF serializers
│   │   ├── views.py                  # API views and endpoints
│   │   ├── urls.py                   # App URL routing
│   │   ├── ai_service.py             # AI integration module
│   │   ├── tests.py                  # Unit tests
│   │   └── migrations/               # Database migrations
│   │
│   ├── manage.py                     # Django management script
│   ├── requirements.txt              # Python dependencies
│   ├── env_example.txt               # Environment variables template
│   ├── sample_data.py                # Sample data generator script
│   └── .gitignore                    # Git ignore rules for backend
│
├── frontend/                         # React Frontend
│   ├── public/                       # Static public assets
│   │   └── vite.svg                  # Favicon
│   │
│   ├── src/                          # Source code
│   │   ├── pages/                    # Page components
│   │   │   ├── ChatInterface.jsx     # Main chat page
│   │   │   ├── ConversationsDashboard.jsx  # Conversations list
│   │   │   └── ConversationIntelligence.jsx # Query interface
│   │   │
│   │   ├── services/                 # Service modules
│   │   │   └── api.js                # API client (Axios)
│   │   │
│   │   ├── App.jsx                   # Root component with routing
│   │   ├── main.jsx                  # Application entry point
│   │   └── index.css                 # Global styles and Tailwind
│   │
│   ├── index.html                    # HTML template
│   ├── package.json                  # Node.js dependencies
│   ├── vite.config.js                # Vite configuration
│   ├── tailwind.config.js            # Tailwind CSS configuration
│   ├── postcss.config.js             # PostCSS configuration
│   └── .gitignore                    # Git ignore rules for frontend
│
├── docs/                             # Documentation (optional)
│   └── screenshots/                  # UI screenshots
│
├── README.md                         # Main project documentation
├── SETUP_INSTRUCTIONS.md             # Detailed setup guide
├── API_DOCUMENTATION.md              # API endpoint documentation
├── ARCHITECTURE.md                   # System architecture details
├── FEATURES.md                       # Feature documentation
├── PROJECT_STRUCTURE.md              # This file
└── .gitignore                        # Root git ignore

```

## File Descriptions

### Backend Files

#### `backend/chat_portal/`
**Main Django project configuration**

- **`settings.py`**: Core Django configuration
  - Database settings (PostgreSQL)
  - Installed apps
  - Middleware configuration
  - CORS settings
  - REST Framework configuration
  - AI provider settings

- **`urls.py`**: URL routing
  - Admin panel URLs
  - API URLs (includes conversations app)

- **`wsgi.py`** & **`asgi.py`**: Server interfaces
  - WSGI for traditional deployment
  - ASGI for async capabilities

#### `backend/conversations/`
**Main application logic**

- **`models.py`**: Database models (175 lines)
  - `Conversation` model with metadata
  - `Message` model with foreign keys
  - Model methods for calculations
  - Proper indexing for performance

- **`serializers.py`**: Data transformation (120 lines)
  - `ConversationListSerializer`: For list view
  - `ConversationDetailSerializer`: With messages
  - `MessageSerializer`: Individual messages
  - Custom serializers for actions

- **`views.py`**: API logic (250+ lines)
  - `ConversationViewSet`: Main viewset
  - CRUD operations
  - Custom actions (@action decorator)
  - Error handling
  - Business logic

- **`ai_service.py`**: AI integration (400+ lines)
  - `AIService` class
  - Multi-provider support
  - Chat functionality
  - Analysis methods (summary, topics, sentiment)
  - Query and search methods

- **`admin.py`**: Django admin interface
  - Custom admin views
  - List displays
  - Filters and search

- **`tests.py`**: Unit tests
  - Model tests
  - API tests
  - Test coverage

#### Other Backend Files

- **`manage.py`**: Django CLI
  - Run server
  - Migrations
  - Create superuser
  - Custom commands

- **`requirements.txt`**: Dependencies
  - Django & DRF
  - PostgreSQL adapter
  - AI libraries
  - Utilities

- **`sample_data.py`**: Data generator
  - Creates sample conversations
  - Useful for testing
  - Realistic data

### Frontend Files

#### `frontend/src/pages/`
**Page components (main views)**

- **`ChatInterface.jsx`** (300+ lines)
  - Real-time chat UI
  - Message display
  - Conversation sidebar
  - Send message logic
  - End conversation

- **`ConversationsDashboard.jsx`** (400+ lines)
  - List all conversations
  - Search and filter
  - Conversation cards
  - Detail modal
  - Statistics

- **`ConversationIntelligence.jsx`** (300+ lines)
  - Query interface
  - Date filters
  - Results display
  - Relevant conversations
  - Example queries

#### `frontend/src/`
**Core application files**

- **`App.jsx`** (100 lines)
  - Root component
  - Navigation
  - Routing
  - Dark mode toggle
  - Layout structure

- **`main.jsx`**: Entry point
  - React rendering
  - App initialization

- **`index.css`**: Global styles
  - Tailwind directives
  - Custom animations
  - Scrollbar styling

#### `frontend/src/services/`
**Service layer**

- **`api.js`** (100+ lines)
  - Axios configuration
  - API endpoints
  - Error handling
  - Request/response interceptors

#### Frontend Configuration

- **`package.json`**: Dependencies
  - React, React Router
  - Tailwind CSS
  - Axios
  - Build tools

- **`vite.config.js`**: Vite settings
  - Dev server
  - Proxy configuration
  - Build options

- **`tailwind.config.js`**: Tailwind customization
  - Custom colors
  - Theme extensions
  - Dark mode config

### Documentation Files

- **`README.md`** (500+ lines)
  - Project overview
  - Features list
  - Installation guide
  - Usage examples
  - API documentation
  - Screenshots section

- **`SETUP_INSTRUCTIONS.md`** (600+ lines)
  - Step-by-step setup
  - Troubleshooting
  - Environment configuration
  - Database setup
  - Testing instructions

- **`API_DOCUMENTATION.md`** (800+ lines)
  - All endpoints
  - Request/response examples
  - Error codes
  - Authentication (future)
  - Rate limiting (future)

- **`ARCHITECTURE.md`** (600+ lines)
  - System architecture
  - Data flow diagrams
  - Component breakdown
  - Technology stack
  - Deployment guide

- **`FEATURES.md`** (500+ lines)
  - Detailed feature descriptions
  - Technical implementation
  - User flows
  - Future enhancements

- **`PROJECT_STRUCTURE.md`**: This file
  - Directory tree
  - File descriptions
  - Line counts
  - Purpose of each file

## Code Statistics

### Backend
```
Django Project:
- Python files: 15+
- Total lines of code: ~2500
- Models: 2 (Conversation, Message)
- API endpoints: 6
- Serializers: 5+
- Views: 1 ViewSet with custom actions
```

### Frontend
```
React Application:
- JavaScript/JSX files: 8+
- Total lines of code: ~1500
- Pages: 3
- Components: 10+ (including subcomponents)
- Services: 1 (API)
```

### Documentation
```
Markdown files: 6
Total documentation lines: ~3000
Code examples: 50+
Diagrams: 10+
```

## Technology Distribution

### Backend Stack
```
Python:        85%
Configuration: 10%
Documentation: 5%
```

### Frontend Stack
```
JavaScript/JSX: 70%
CSS/Tailwind:   20%
Configuration:  5%
HTML:          5%
```

## Key Directories Explained

### `/backend/chat_portal/`
Main Django project settings and configuration. Think of this as the "control center" of the backend.

### `/backend/conversations/`
The core application containing all business logic, models, and API endpoints. This is where most backend development happens.

### `/frontend/src/pages/`
Main UI pages that users interact with. Each file represents a route/page in the application.

### `/frontend/src/services/`
Business logic and API communication layer. Separates API calls from UI components.

## Import Structure

### Backend Imports
```python
# Standard library
import os
from typing import List

# Django
from django.db import models
from rest_framework import viewsets

# Local
from .models import Conversation
from .serializers import ConversationSerializer
```

### Frontend Imports
```javascript
// React
import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

// External libraries
import axios from 'axios'
import { format } from 'date-fns'

// Local
import apiService from '../services/api'
```

## Build Output

### Backend
```
After migrations:
- Database tables created
- Indexes established
- Constraints enforced
```

### Frontend
```
After npm run build:
- dist/
  ├── assets/
  │   ├── index-[hash].js
  │   └── index-[hash].css
  └── index.html
```

## Environment Files

### Backend `.env`
```
DB_NAME=chat_portal_db
DB_USER=postgres
DB_PASSWORD=...
AI_PROVIDER=openai
OPENAI_API_KEY=...
```

### Frontend (uses backend proxy)
No separate .env needed in development. Vite proxy handles API routing.

---

## Quick Navigation

- **To modify database schema**: `backend/conversations/models.py`
- **To add/modify API endpoints**: `backend/conversations/views.py`
- **To change AI behavior**: `backend/conversations/ai_service.py`
- **To modify chat UI**: `frontend/src/pages/ChatInterface.jsx`
- **To change styling**: `frontend/src/index.css` or Tailwind classes
- **To add new routes**: `frontend/src/App.jsx`
- **To configure database**: `backend/chat_portal/settings.py`

---

**Total Files**: 50+  
**Total Lines of Code**: ~6000+  
**Documentation**: Comprehensive  
**Test Coverage**: Basic unit tests included

