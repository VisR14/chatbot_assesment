# Architecture Documentation - AI Chat Portal

## System Architecture Overview

The AI Chat Portal is built using a modern full-stack architecture with clear separation of concerns between frontend, backend, database, and AI services.

```
┌──────────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER                             │
│                     (http://localhost:3000)                       │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            │ HTTP/REST API
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND (Vite)                         │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐     │
│  │    Pages    │  │  Components  │  │   API Service      │     │
│  │  - Chat     │  │  - Messages  │  │  - Axios Client    │     │
│  │  - Dashboard│  │  - Modals    │  │  - Endpoints       │     │
│  │  - Intel.   │  │  - Forms     │  │                    │     │
│  └─────────────┘  └──────────────┘  └────────────────────┘     │
│                                                                   │
│  Styling: Tailwind CSS  |  Routing: React Router                │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            │ REST API Calls (JSON)
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                DJANGO REST FRAMEWORK BACKEND                      │
│                    (http://localhost:8000)                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      API Layer                           │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │    │
│  │  │   Views      │  │ Serializers  │  │    URLs      │  │    │
│  │  │ - CRUD ops   │  │ - Validation │  │ - Routing    │  │    │
│  │  │ - Custom     │  │ - Transform  │  │ - Endpoints  │  │    │
│  │  │   actions    │  │              │  │              │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   Business Logic Layer                   │    │
│  │  ┌──────────────────┐      ┌──────────────────────┐     │    │
│  │  │   AI Service     │      │      Models          │     │    │
│  │  │ - Chat           │      │ - Conversation       │     │    │
│  │  │ - Summarize      │      │ - Message            │     │    │
│  │  │ - Analyze        │      │ - ORM Methods        │     │    │
│  │  │ - Query          │      │                      │     │    │
│  │  └──────────────────┘      └──────────────────────┘     │    │
│  └─────────────────────────────────────────────────────────┘    │
└───────────────┬──────────────────────┬───────────────────────────┘
                │                      │
                │ psycopg2            │ HTTP/API Calls
                ▼                      ▼
    ┌────────────────────┐   ┌────────────────────────┐
    │   PostgreSQL DB    │   │    AI Provider         │
    │                    │   │  ┌──────────────────┐  │
    │ - conversations    │   │  │   OpenAI API     │  │
    │ - messages         │   │  │      OR          │  │
    │ - Indexes          │   │  │  Anthropic API   │  │
    │ - Constraints      │   │  │      OR          │  │
    │                    │   │  │   Gemini API     │  │
    └────────────────────┘   │  │      OR          │  │
                             │  │   LM Studio      │  │
                             │  │   (localhost)    │  │
                             │  └──────────────────┘  │
                             └────────────────────────┘
```

---

## Component Breakdown

### 1. Frontend Layer (React + Tailwind CSS)

#### Pages
- **ChatInterface** (`/`)
  - Real-time chat with AI
  - Message history display
  - Conversation sidebar
  - Send/end conversation controls

- **ConversationsDashboard** (`/conversations`)
  - List all conversations
  - Search and filter
  - View conversation details
  - Display AI analysis results

- **ConversationIntelligence** (`/intelligence`)
  - Natural language query interface
  - Date range filters
  - Results display with relevant excerpts

#### Components
- Navigation bar with dark mode toggle
- Message bubbles (user/AI)
- Conversation cards
- Modal dialogs
- Loading states
- Form inputs

#### Services
- **API Service**: Centralized HTTP client using Axios
  - Handles all API calls
  - Error handling
  - Request/response transformation

---

### 2. Backend Layer (Django REST Framework)

#### API Endpoints

**Conversation Management:**
- `GET /api/conversations/` - List all conversations
- `GET /api/conversations/{id}/` - Get conversation details
- `POST /api/conversations/` - Create new conversation

**Chat Operations:**
- `POST /api/conversations/send_message/` - Send message and get AI response
- `POST /api/conversations/end_conversation/` - End and analyze conversation

**Intelligence:**
- `POST /api/conversations/query_conversations/` - Query past conversations

#### Models

**Conversation Model:**
```python
- id (Primary Key)
- title (CharField)
- status (active/ended)
- start_timestamp
- end_timestamp
- summary (AI-generated)
- topics (JSONField)
- key_points (JSONField)
- sentiment (positive/negative/neutral)
- embedding (JSONField - for future vector search)
```

**Message Model:**
```python
- id (Primary Key)
- conversation (ForeignKey)
- content (TextField)
- sender (user/ai)
- timestamp
- tokens_used
- model_used
```

#### AI Service Module

**Core Functions:**
1. **chat()** - Send messages to LLM and get responses
2. **generate_summary()** - Create conversation summary
3. **extract_topics()** - Identify main topics discussed
4. **analyze_sentiment()** - Determine conversation tone
5. **extract_key_points()** - Find decisions and action items
6. **query_conversations()** - Answer questions about past chats
7. **semantic_search()** - Find relevant conversations

**Provider Support:**
- OpenAI (GPT-3.5/4)
- Anthropic (Claude)
- Google (Gemini)
- LM Studio (Local models)

---

### 3. Database Layer (PostgreSQL)

#### Schema Design

**conversations table:**
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

CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_conversations_start ON conversations(start_timestamp DESC);
```

**messages table:**
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

CREATE INDEX idx_messages_conversation ON messages(conversation_id, timestamp);
CREATE INDEX idx_messages_sender ON messages(sender);
```

#### Indexes
- Primary keys on both tables
- Foreign key index on messages.conversation_id
- Timestamp index for sorting
- Status index for filtering

---

### 4. AI Integration Layer

#### Flow Diagram

```
┌──────────────┐
│ User Message │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  Django View         │
│  - Validate input    │
│  - Save user message │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────┐
│  AI Service              │
│  - Get conversation hist │
│  - Format for AI model   │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  AI Provider             │
│  - Process prompt        │
│  - Generate response     │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  Django View             │
│  - Save AI response      │
│  - Return to frontend    │
└──────┬───────────────────┘
       │
       ▼
┌──────────────┐
│ Display to   │
│ User         │
└──────────────┘
```

---

## Data Flow

### 1. Sending a Message

```
Frontend                Backend                  Database              AI Provider
   │                       │                        │                      │
   │  POST /send_message   │                        │                      │
   ├──────────────────────>│                        │                      │
   │                       │  Save user message     │                      │
   │                       ├───────────────────────>│                      │
   │                       │                        │                      │
   │                       │  Get conversation      │                      │
   │                       │  history               │                      │
   │                       │<───────────────────────┤                      │
   │                       │                        │                      │
   │                       │  Call AI with context  │                      │
   │                       ├───────────────────────────────────────────────>│
   │                       │                        │                      │
   │                       │  AI Response           │                      │
   │                       │<───────────────────────────────────────────────┤
   │                       │                        │                      │
   │                       │  Save AI message       │                      │
   │                       ├───────────────────────>│                      │
   │                       │                        │                      │
   │  Response (both msgs) │                        │                      │
   │<──────────────────────┤                        │                      │
   │                       │                        │                      │
```

### 2. Ending a Conversation

```
Frontend                Backend                  Database              AI Provider
   │                       │                        │                      │
   │  POST /end_conv       │                        │                      │
   ├──────────────────────>│                        │                      │
   │                       │  Get all messages      │                      │
   │                       ├───────────────────────>│                      │
   │                       │<───────────────────────┤                      │
   │                       │                        │                      │
   │                       │  Generate summary      │                      │
   │                       ├───────────────────────────────────────────────>│
   │                       │<───────────────────────────────────────────────┤
   │                       │                        │                      │
   │                       │  Extract topics        │                      │
   │                       ├───────────────────────────────────────────────>│
   │                       │<───────────────────────────────────────────────┤
   │                       │                        │                      │
   │                       │  Analyze sentiment     │                      │
   │                       ├───────────────────────────────────────────────>│
   │                       │<───────────────────────────────────────────────┤
   │                       │                        │                      │
   │                       │  Extract key points    │                      │
   │                       ├───────────────────────────────────────────────>│
   │                       │<───────────────────────────────────────────────┤
   │                       │                        │                      │
   │                       │  Update conversation   │                      │
   │                       │  with analysis         │                      │
   │                       ├───────────────────────>│                      │
   │                       │                        │                      │
   │  Response (analysis)  │                        │                      │
   │<──────────────────────┤                        │                      │
   │                       │                        │                      │
```

### 3. Querying Conversations

```
Frontend                Backend                  Database              AI Provider
   │                       │                        │                      │
   │  POST /query_conv     │                        │                      │
   ├──────────────────────>│                        │                      │
   │                       │  Get ended convs       │                      │
   │                       ├───────────────────────>│                      │
   │                       │<───────────────────────┤                      │
   │                       │                        │                      │
   │                       │  Semantic search       │                      │
   │                       │  (keyword matching)    │                      │
   │                       │                        │                      │
   │                       │  Build context         │                      │
   │                       │  from relevant convs   │                      │
   │                       │                        │                      │
   │                       │  Ask AI to answer      │                      │
   │                       ├───────────────────────────────────────────────>│
   │                       │                        │                      │
   │                       │  AI Answer             │                      │
   │                       │<───────────────────────────────────────────────┤
   │                       │                        │                      │
   │  Response (answer +   │                        │                      │
   │  relevant convs)      │                        │                      │
   │<──────────────────────┤                        │                      │
   │                       │                        │                      │
```

---

## Technology Stack Details

### Backend Stack
- **Python 3.9+**: Core language
- **Django 4.2**: Web framework
- **Django REST Framework 3.14**: API framework
- **PostgreSQL 12+**: Relational database
- **psycopg2**: PostgreSQL adapter
- **OpenAI/Anthropic/Google libraries**: AI integration

### Frontend Stack
- **React 18.2**: UI library
- **Vite 5.0**: Build tool and dev server
- **React Router 6**: Client-side routing
- **Tailwind CSS 3.3**: Utility-first CSS
- **Axios**: HTTP client
- **date-fns**: Date formatting
- **React Icons**: Icon library

---

## Security Considerations

### Current Implementation
- CORS enabled for development
- No authentication (development only)
- API keys stored in environment variables
- PostgreSQL password protection

### Production Recommendations
1. **Authentication**: Implement JWT or session-based auth
2. **Authorization**: User-based conversation access
3. **Rate Limiting**: Prevent API abuse
4. **HTTPS**: Encrypt all communications
5. **Input Validation**: Sanitize all user inputs
6. **SQL Injection**: Using ORM prevents this
7. **XSS Protection**: React handles this by default
8. **CSRF Protection**: Django middleware enabled

---

## Scalability Considerations

### Current Architecture
- Suitable for: Demo, development, small-scale deployment
- Limitations: Single server, no caching, synchronous processing

### Future Improvements
1. **Caching**: Redis for frequently accessed data
2. **Task Queue**: Celery for async AI processing
3. **Load Balancing**: Multiple backend instances
4. **Database**: Read replicas, connection pooling
5. **CDN**: Static asset delivery
6. **WebSockets**: Real-time updates without polling
7. **Vector Database**: For semantic search (Pinecone, Weaviate)
8. **Microservices**: Separate AI service

---

## Performance Optimization

### Backend
- Database indexes on frequently queried fields
- Pagination for large result sets
- Efficient ORM queries (select_related, prefetch_related)
- Asynchronous AI calls (future enhancement)

### Frontend
- Code splitting with React.lazy
- Memo-ization of expensive components
- Debouncing search inputs
- Virtualized lists for long conversations
- Optimistic UI updates

---

## Development Workflow

```
┌────────────────┐
│  Code Changes  │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│  Git Commit    │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│  Local Testing │
│  - Unit tests  │
│  - Manual test │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│  Git Push      │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│  Deployment    │
│  (Production)  │
└────────────────┘
```

---

## Error Handling Strategy

### Frontend
```javascript
try {
  const response = await apiService.sendMessage(id, msg);
  // Handle success
} catch (error) {
  // Show user-friendly error
  alert('Failed to send message');
  console.error(error);
}
```

### Backend
```python
try:
    # Business logic
except ModelDoesNotExist:
    return Response({'error': 'Not found'}, status=404)
except Exception as e:
    return Response({'error': str(e)}, status=500)
```

---

## Monitoring & Logging

### Current Implementation
- Django console logging
- Browser console for frontend errors
- Database query logging (DEBUG mode)

### Production Recommendations
1. **Centralized Logging**: ELK Stack or Datadog
2. **Error Tracking**: Sentry
3. **Performance Monitoring**: New Relic or AppDynamics
4. **Database Monitoring**: pgAdmin, pg_stat_statements
5. **API Monitoring**: Response times, error rates

---

## Deployment Architecture (Production)

```
                    ┌──────────────┐
                    │   CloudFlare │
                    │   (CDN/DNS)  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   Nginx      │
                    │  (Reverse    │
                    │   Proxy)     │
                    └──┬────────┬──┘
                       │        │
         ┌─────────────┘        └─────────────┐
         ▼                                     ▼
┌────────────────┐                   ┌────────────────┐
│  Static Files  │                   │   Gunicorn     │
│  (React Build) │                   │   (Django)     │
└────────────────┘                   └────────┬───────┘
                                              │
                                    ┌─────────▼────────┐
                                    │   PostgreSQL     │
                                    │   (Primary)      │
                                    └──────────────────┘
```

---

**Version:** 1.0  
**Last Updated:** January 2024

