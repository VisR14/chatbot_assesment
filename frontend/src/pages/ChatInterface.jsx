import React, { useState, useEffect, useRef } from 'react'
import { FiSend, FiPlus, FiCheck } from 'react-icons/fi'
import { format } from 'date-fns'
import apiService from '../services/api'

function ChatInterface() {
  const [conversations, setConversations] = useState([])
  const [currentConversation, setCurrentConversation] = useState(null)
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [sending, setSending] = useState(false)
  const messagesEndRef = useRef(null)

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Load active conversations on mount
  useEffect(() => {
    loadActiveConversations()
  }, [])

  const loadActiveConversations = async () => {
    try {
      const response = await apiService.getAllConversations({ status: 'active' })
      setConversations(response.conversations || [])
    } catch (error) {
      console.error('Failed to load conversations:', error)
    }
  }

  const startNewConversation = async () => {
    try {
      setLoading(true)
      const response = await apiService.createConversation('New Conversation')
      if (response.success) {
        const newConv = response.conversation
        setCurrentConversation(newConv)
        setMessages([])
        setConversations([newConv, ...conversations])
      }
    } catch (error) {
      console.error('Failed to create conversation:', error)
      alert('Failed to create new conversation')
    } finally {
      setLoading(false)
    }
  }

  const loadConversation = async (conversationId) => {
    try {
      setLoading(true)
      const response = await apiService.getConversation(conversationId)
      if (response.success) {
        setCurrentConversation(response.conversation)
        setMessages(response.conversation.messages || [])
      }
    } catch (error) {
      console.error('Failed to load conversation:', error)
      alert('Failed to load conversation')
    } finally {
      setLoading(false)
    }
  }

  const sendMessage = async (e) => {
    e.preventDefault()
    
    if (!inputMessage.trim()) return
    
    if (!currentConversation) {
      // Create new conversation first
      await startNewConversation()
      // Wait a bit for state to update
      setTimeout(() => sendMessageToConversation(inputMessage), 500)
      return
    }

    await sendMessageToConversation(inputMessage)
  }

  const sendMessageToConversation = async (message) => {
    if (!currentConversation) {
      alert('Please create a conversation first')
      return
    }

    try {
      setSending(true)
      
      // Optimistically add user message to UI
      const tempUserMessage = {
        id: Date.now(),
        content: message,
        sender: 'user',
        timestamp: new Date().toISOString(),
      }
      setMessages(prev => [...prev, tempUserMessage])
      setInputMessage('')

      // Send to API
      const response = await apiService.sendMessage(currentConversation.id, message)
      
      if (response.success) {
        // Replace temp message with real messages from server
        setMessages(prev => {
          const filtered = prev.filter(msg => msg.id !== tempUserMessage.id)
          return [...filtered, response.user_message, response.ai_response]
        })

        // Update conversation title if it changed
        if (response.ai_response) {
          const updatedConvs = conversations.map(conv =>
            conv.id === currentConversation.id
              ? { ...conv, updated_at: new Date().toISOString() }
              : conv
          )
          setConversations(updatedConvs)
        }
      }
    } catch (error) {
      console.error('Failed to send message:', error)
      alert('Failed to send message. Please try again.')
      // Remove optimistic message on error
      setMessages(prev => prev.filter(msg => msg.id !== Date.now()))
    } finally {
      setSending(false)
    }
  }

  const endCurrentConversation = async () => {
    if (!currentConversation) return

    if (!window.confirm('Are you sure you want to end this conversation? It will be analyzed and saved.')) {
      return
    }

    try {
      setLoading(true)
      const response = await apiService.endConversation(currentConversation.id)
      
      if (response.success) {
        alert('Conversation ended and analyzed successfully!')
        setCurrentConversation(null)
        setMessages([])
        loadActiveConversations()
      }
    } catch (error) {
      console.error('Failed to end conversation:', error)
      alert('Failed to end conversation')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex gap-6 h-[calc(100vh-12rem)]">
      {/* Sidebar - Conversations List */}
      <div className="w-64 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 flex flex-col">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <button
            onClick={startNewConversation}
            disabled={loading}
            className="w-full flex items-center justify-center px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors disabled:opacity-50"
          >
            <FiPlus className="mr-2" />
            New Chat
          </button>
        </div>

        <div className="flex-1 overflow-y-auto custom-scrollbar">
          {conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => loadConversation(conv.id)}
              className={`w-full text-left px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-700 border-b border-gray-100 dark:border-gray-700 transition-colors ${
                currentConversation?.id === conv.id ? 'bg-primary-50 dark:bg-primary-900' : ''
              }`}
            >
              <div className="font-medium text-sm text-gray-900 dark:text-white truncate">
                {conv.title || 'New Conversation'}
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                {conv.message_count || 0} messages
              </div>
            </button>
          ))}
          {conversations.length === 0 && (
            <div className="p-4 text-center text-gray-500 dark:text-gray-400 text-sm">
              No active conversations
            </div>
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 flex flex-col">
        {/* Chat Header */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <div>
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              {currentConversation?.title || 'Chat with AI'}
            </h2>
            {currentConversation && (
              <p className="text-sm text-gray-500 dark:text-gray-400">
                {messages.length} messages
              </p>
            )}
          </div>
          {currentConversation && (
            <button
              onClick={endCurrentConversation}
              disabled={loading}
              className="flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors disabled:opacity-50"
            >
              <FiCheck className="mr-2" />
              End Conversation
            </button>
          )}
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-4">
          {messages.length === 0 && !loading && (
            <div className="flex items-center justify-center h-full text-gray-500 dark:text-gray-400">
              <div className="text-center">
                <FiSend size={48} className="mx-auto mb-4 opacity-20" />
                <p>Start a conversation with AI</p>
                <p className="text-sm mt-2">Type a message below to begin</p>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} message-enter`}
            >
              <div
                className={`max-w-[70%] rounded-lg px-4 py-3 ${
                  message.sender === 'user'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                }`}
              >
                <div className="text-sm whitespace-pre-wrap break-words">{message.content}</div>
                <div
                  className={`text-xs mt-1 ${
                    message.sender === 'user' ? 'text-primary-100' : 'text-gray-500 dark:text-gray-400'
                  }`}
                >
                  {format(new Date(message.timestamp), 'HH:mm')}
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 dark:bg-gray-700 rounded-lg px-4 py-3">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <form onSubmit={sendMessage} className="flex gap-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              disabled={sending}
              className="flex-1 px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={sending || !inputMessage.trim()}
              className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              <FiSend className="mr-2" />
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface

