/**
 * API Service Module
 * Handles all HTTP requests to the Django backend.
 */
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API Service object with all endpoints
const apiService = {
  /**
   * Conversation Management APIs
   */

  // Get all conversations
  getAllConversations: async (params = {}) => {
    try {
      const response = await api.get('/conversations/', { params })
      return response.data
    } catch (error) {
      console.error('Error fetching conversations:', error)
      throw error
    }
  },

  // Get a specific conversation by ID
  getConversation: async (id) => {
    try {
      const response = await api.get(`/conversations/${id}/`)
      return response.data
    } catch (error) {
      console.error('Error fetching conversation:', error)
      throw error
    }
  },

  // Create a new conversation
  createConversation: async (title = '') => {
    try {
      const response = await api.post('/conversations/', { title })
      return response.data
    } catch (error) {
      console.error('Error creating conversation:', error)
      throw error
    }
  },

  // Send a message in a conversation
  sendMessage: async (conversationId, message) => {
    try {
      const response = await api.post('/conversations/send_message/', {
        conversation_id: conversationId,
        message: message,
      })
      return response.data
    } catch (error) {
      console.error('Error sending message:', error)
      throw error
    }
  },

  // End a conversation
  endConversation: async (conversationId) => {
    try {
      const response = await api.post('/conversations/end_conversation/', {
        conversation_id: conversationId,
      })
      return response.data
    } catch (error) {
      console.error('Error ending conversation:', error)
      throw error
    }
  },

  /**
   * Conversation Intelligence APIs
   */

  // Query past conversations
  queryConversations: async (query, filters = {}) => {
    try {
      const response = await api.post('/conversations/query_conversations/', {
        query: query,
        ...filters,
      })
      return response.data
    } catch (error) {
      console.error('Error querying conversations:', error)
      throw error
    }
  },
}

export default apiService

