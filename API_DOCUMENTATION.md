# API Documentation - AI Chat Portal

## Base URL
```
http://localhost:8000/api/
```

## Content Type
All POST requests should include:
```
Content-Type: application/json
```

---

## Endpoints

### 1. List All Conversations

**Endpoint:** `GET /api/conversations/`

**Description:** Retrieve all conversations with basic information.

**Query Parameters:**
- `status` (optional): Filter by status
  - Values: `active`, `ended`
- `search` (optional): Search in title and summary

**Example Request:**
```bash
curl http://localhost:8000/api/conversations/
```

**Example Request with Filters:**
```bash
curl "http://localhost:8000/api/conversations/?status=ended&search=travel"
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "count": 2,
  "conversations": [
    {
      "id": 1,
      "title": "Trip Planning Discussion",
      "status": "ended",
      "start_timestamp": "2024-01-15T10:30:00Z",
      "end_timestamp": "2024-01-15T11:00:00Z",
      "message_count": 12,
      "duration": 1800.0,
      "last_message": {
        "content": "Thank you for helping me plan!",
        "sender": "user",
        "timestamp": "2024-01-15T11:00:00Z"
      },
      "topics": ["travel", "Japan", "itinerary"],
      "sentiment": "positive",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T11:00:05Z"
    }
  ]
}
```

---

### 2. Get Specific Conversation

**Endpoint:** `GET /api/conversations/{id}/`

**Description:** Retrieve a specific conversation with full message history.

**Path Parameters:**
- `id` (required): Conversation ID

**Example Request:**
```bash
curl http://localhost:8000/api/conversations/1/
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "conversation": {
    "id": 1,
    "title": "Trip Planning Discussion",
    "status": "ended",
    "start_timestamp": "2024-01-15T10:30:00Z",
    "end_timestamp": "2024-01-15T11:00:00Z",
    "summary": "User discussed planning a trip to Japan, including travel dates, places to visit, and accommodation options. Key decisions included booking flights within the next week and researching hotels in Tokyo.",
    "topics": ["travel", "Japan", "itinerary", "accommodation"],
    "key_points": [
      "Book flights by next week",
      "Research hotels in Tokyo and Kyoto",
      "Visit during cherry blossom season",
      "Budget approximately $3000 for the trip"
    ],
    "sentiment": "positive",
    "message_count": 12,
    "duration": 1800.0,
    "messages": [
      {
        "id": 1,
        "conversation": 1,
        "content": "I want to plan a trip to Japan next spring",
        "sender": "user",
        "timestamp": "2024-01-15T10:30:00Z",
        "tokens_used": null,
        "model_used": null,
        "created_at": "2024-01-15T10:30:00Z"
      },
      {
        "id": 2,
        "conversation": 1,
        "content": "That's wonderful! Japan in spring is beautiful with cherry blossoms. What aspects of the trip would you like to plan first?",
        "sender": "ai",
        "timestamp": "2024-01-15T10:30:05Z",
        "tokens_used": 45,
        "model_used": "gpt-3.5-turbo",
        "created_at": "2024-01-15T10:30:05Z"
      }
    ],
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:00:05Z"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "success": false,
  "error": "Conversation not found"
}
```

---

### 3. Create New Conversation

**Endpoint:** `POST /api/conversations/`

**Description:** Create a new conversation.

**Request Body:**
```json
{
  "title": "New Conversation"
}
```

**Fields:**
- `title` (optional): Conversation title (will be auto-generated if not provided)

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My New Chat"}'
```

**Success Response (201 Created):**
```json
{
  "success": true,
  "conversation": {
    "id": 3,
    "title": "My New Chat",
    "status": "active",
    "start_timestamp": "2024-01-16T09:00:00Z",
    "end_timestamp": null,
    "summary": null,
    "topics": [],
    "key_points": [],
    "sentiment": null,
    "message_count": 0,
    "duration": null,
    "messages": [],
    "created_at": "2024-01-16T09:00:00Z",
    "updated_at": "2024-01-16T09:00:00Z"
  },
  "message": "Conversation created successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "errors": {
    "title": ["This field may not be blank."]
  }
}
```

---

### 4. Send Message

**Endpoint:** `POST /api/conversations/send_message/`

**Description:** Send a message in a conversation and receive AI response.

**Request Body:**
```json
{
  "conversation_id": 1,
  "message": "Hello, can you help me with something?"
}
```

**Fields:**
- `conversation_id` (required): ID of the conversation
- `message` (required): Message content

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/conversations/send_message/ \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 1,
    "message": "What are the best places to visit in Tokyo?"
  }'
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "user_message": {
    "id": 15,
    "conversation": 1,
    "content": "What are the best places to visit in Tokyo?",
    "sender": "user",
    "timestamp": "2024-01-16T10:30:00Z",
    "tokens_used": null,
    "model_used": null,
    "created_at": "2024-01-16T10:30:00Z"
  },
  "ai_response": {
    "id": 16,
    "conversation": 1,
    "content": "Tokyo has many amazing places to visit! Here are some top recommendations:\n\n1. Senso-ji Temple in Asakusa\n2. Shibuya Crossing and Hachiko Statue\n3. Tokyo Skytree for panoramic views\n4. Meiji Shrine in Harajuku\n5. Tsukiji Outer Market for food\n\nWould you like more details about any of these?",
    "sender": "ai",
    "timestamp": "2024-01-16T10:30:02Z",
    "tokens_used": 125,
    "model_used": "gpt-3.5-turbo",
    "created_at": "2024-01-16T10:30:02Z"
  }
}
```

**Error Responses:**

*Conversation Not Found (404):*
```json
{
  "success": false,
  "error": "Conversation not found"
}
```

*Conversation Not Active (400):*
```json
{
  "success": false,
  "error": "Conversation is not active"
}
```

*AI Service Error (500):*
```json
{
  "success": false,
  "error": "AI service error"
}
```

---

### 5. End Conversation

**Endpoint:** `POST /api/conversations/end_conversation/`

**Description:** End a conversation and trigger AI analysis (summary, topics, sentiment, key points).

**Request Body:**
```json
{
  "conversation_id": 1
}
```

**Fields:**
- `conversation_id` (required): ID of the conversation to end

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/conversations/end_conversation/ \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": 1}'
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "conversation": {
    "id": 1,
    "title": "Trip Planning Discussion",
    "status": "ended",
    "start_timestamp": "2024-01-15T10:30:00Z",
    "end_timestamp": "2024-01-15T11:00:00Z",
    "summary": "User discussed planning a trip to Japan, including travel dates, places to visit, and accommodation options. Key decisions included booking flights within the next week and researching hotels in Tokyo.",
    "topics": ["travel", "Japan", "itinerary", "accommodation"],
    "key_points": [
      "Book flights by next week",
      "Research hotels in Tokyo and Kyoto",
      "Visit during cherry blossom season",
      "Budget approximately $3000 for the trip"
    ],
    "sentiment": "positive",
    "message_count": 12,
    "duration": 1800.0,
    "messages": [],
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:00:05Z"
  },
  "message": "Conversation ended and analyzed successfully"
}
```

**Error Responses:**

*Already Ended (400):*
```json
{
  "success": false,
  "error": "Conversation is already ended"
}
```

*No Messages (400):*
```json
{
  "success": false,
  "error": "Cannot end conversation with no messages"
}
```

*Not Found (404):*
```json
{
  "success": false,
  "error": "Conversation not found"
}
```

---

### 6. Query Conversations (Intelligence)

**Endpoint:** `POST /api/conversations/query_conversations/`

**Description:** Query past conversations using natural language. The AI will search through ended conversations and provide intelligent answers with relevant excerpts.

**Request Body:**
```json
{
  "query": "What did I discuss about travel last week?",
  "date_from": "2024-01-01T00:00:00Z",
  "date_to": "2024-01-31T23:59:59Z",
  "limit": 5
}
```

**Fields:**
- `query` (required): Natural language question
- `date_from` (optional): Start date for filtering (ISO 8601 format)
- `date_to` (optional): End date for filtering (ISO 8601 format)
- `limit` (optional): Maximum number of relevant conversations to return (default: 5, max: 20)

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/conversations/query_conversations/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What travel plans did I discuss?",
    "limit": 3
  }'
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "query": "What travel plans did I discuss?",
  "answer": "Based on your conversations, you discussed planning a trip to Japan for next spring during cherry blossom season. You talked about visiting Tokyo and Kyoto, with key decisions including booking flights within the next week, researching hotels, and budgeting approximately $3000 for the trip. You also mentioned wanting to experience traditional Japanese culture and cuisine.",
  "relevant_conversations": [
    {
      "id": 1,
      "title": "Trip Planning Discussion",
      "status": "ended",
      "start_timestamp": "2024-01-15T10:30:00Z",
      "end_timestamp": "2024-01-15T11:00:00Z",
      "summary": "User discussed planning a trip to Japan...",
      "topics": ["travel", "Japan", "itinerary"],
      "key_points": ["Book flights by next week", "Research hotels"],
      "sentiment": "positive",
      "message_count": 12,
      "duration": 1800.0,
      "messages": [
        {
          "id": 1,
          "content": "I want to plan a trip to Japan next spring",
          "sender": "user",
          "timestamp": "2024-01-15T10:30:00Z"
        }
      ]
    }
  ],
  "count": 1
}
```

**No Results Response (200 OK):**
```json
{
  "success": true,
  "query": "What did I discuss about Mars colonization?",
  "answer": "No relevant conversations found for your query.",
  "relevant_conversations": [],
  "count": 0
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "errors": {
    "query": ["This field is required."]
  }
}
```

---

## Common Response Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 201  | Created (for new conversations) |
| 400  | Bad Request (validation error or invalid operation) |
| 404  | Not Found (conversation doesn't exist) |
| 500  | Internal Server Error (AI service error, etc.) |

---

## Error Response Format

All error responses follow this format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

Or for validation errors:

```json
{
  "success": false,
  "errors": {
    "field_name": ["Error message for this field"]
  }
}
```

---

## Example Usage Flow

### Complete Chat Session Example

```bash
# 1. Create a new conversation
curl -X POST http://localhost:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Travel Planning"}'

# Response: conversation_id = 5

# 2. Send first message
curl -X POST http://localhost:8000/api/conversations/send_message/ \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 5,
    "message": "I want to plan a trip to Paris"
  }'

# 3. Send follow-up messages
curl -X POST http://localhost:8000/api/conversations/send_message/ \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 5,
    "message": "What are the must-visit places?"
  }'

# 4. End the conversation
curl -X POST http://localhost:8000/api/conversations/end_conversation/ \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": 5}'

# 5. Query about this conversation later
curl -X POST http://localhost:8000/api/conversations/query_conversations/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What did I plan about Paris?"
  }'
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. In production, consider implementing:
- Per-IP rate limiting
- Per-user rate limiting
- Token bucket or sliding window algorithm

---

## Authentication

The current implementation does not include authentication. For production:
- Implement JWT or session-based authentication
- Add user model and associate conversations with users
- Protect endpoints with authentication middleware

---

## Notes

1. **Conversation Status**: Conversations can only be in two states: `active` or `ended`
2. **AI Analysis**: Summary, topics, sentiment, and key points are only generated when ending a conversation
3. **Message Ordering**: Messages are always returned in chronological order
4. **Timestamps**: All timestamps are in ISO 8601 format (UTC)
5. **AI Provider**: The backend supports multiple AI providers (OpenAI, Claude, Gemini, LM Studio) configured via environment variables

---

## Testing with curl

Here's a complete test script:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api"

echo "1. Creating conversation..."
CONV_ID=$(curl -s -X POST $BASE_URL/conversations/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Conversation"}' | jq -r '.conversation.id')

echo "Created conversation ID: $CONV_ID"

echo "2. Sending message..."
curl -X POST $BASE_URL/conversations/send_message/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\":$CONV_ID,\"message\":\"Hello AI!\"}"

echo "3. Getting conversation..."
curl $BASE_URL/conversations/$CONV_ID/

echo "4. Ending conversation..."
curl -X POST $BASE_URL/conversations/end_conversation/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\":$CONV_ID}"

echo "Done!"
```

---

**API Version:** 1.0  
**Last Updated:** January 2024

