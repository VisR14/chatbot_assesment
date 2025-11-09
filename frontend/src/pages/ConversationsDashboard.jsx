import React, { useState, useEffect } from 'react'
import { FiCalendar, FiMessageSquare, FiClock, FiTag, FiSearch } from 'react-icons/fi'
import { format } from 'date-fns'
import apiService from '../services/api'

function ConversationsDashboard() {
  const [conversations, setConversations] = useState([])
  const [selectedConversation, setSelectedConversation] = useState(null)
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')

  useEffect(() => {
    loadConversations()
  }, [])

  const loadConversations = async () => {
    try {
      setLoading(true)
      const response = await apiService.getAllConversations()
      if (response.success) {
        setConversations(response.conversations || [])
      }
    } catch (error) {
      console.error('Failed to load conversations:', error)
    } finally {
      setLoading(false)
    }
  }

  const viewConversationDetails = async (conversationId) => {
    try {
      const response = await apiService.getConversation(conversationId)
      if (response.success) {
        setSelectedConversation(response.conversation)
      }
    } catch (error) {
      console.error('Failed to load conversation details:', error)
      alert('Failed to load conversation details')
    }
  }

  const closeDetails = () => {
    setSelectedConversation(null)
  }

  // Filter conversations
  const filteredConversations = conversations.filter(conv => {
    const matchesSearch = searchTerm === '' || 
      (conv.title && conv.title.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (conv.summary && conv.summary.toLowerCase().includes(searchTerm.toLowerCase()))
    
    const matchesStatus = statusFilter === 'all' || conv.status === statusFilter

    return matchesSearch && matchesStatus
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Conversations Dashboard
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          View and manage all your conversations
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
        <div className="flex gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search conversations..."
              className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
            />
          </div>

          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-gray-900 dark:text-white"
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="ended">Ended</option>
          </select>
        </div>
      </div>

      {/* Conversations List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {loading ? (
          <div className="col-span-full text-center py-12 text-gray-500 dark:text-gray-400">
            Loading conversations...
          </div>
        ) : filteredConversations.length === 0 ? (
          <div className="col-span-full text-center py-12 text-gray-500 dark:text-gray-400">
            No conversations found
          </div>
        ) : (
          filteredConversations.map((conversation) => (
            <div
              key={conversation.id}
              onClick={() => viewConversationDetails(conversation.id)}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-5 hover:shadow-md transition-shadow cursor-pointer"
            >
              {/* Header */}
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-semibold text-gray-900 dark:text-white text-lg truncate flex-1">
                  {conversation.title || 'Untitled Conversation'}
                </h3>
                <span
                  className={`px-2 py-1 rounded-full text-xs font-medium ml-2 ${
                    conversation.status === 'active'
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                  }`}
                >
                  {conversation.status}
                </span>
              </div>

              {/* Metadata */}
              <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <div className="flex items-center">
                  <FiCalendar className="mr-2" />
                  {format(new Date(conversation.start_timestamp), 'MMM dd, yyyy HH:mm')}
                </div>
                <div className="flex items-center">
                  <FiMessageSquare className="mr-2" />
                  {conversation.message_count || 0} messages
                </div>
                {conversation.duration && (
                  <div className="flex items-center">
                    <FiClock className="mr-2" />
                    {Math.round(conversation.duration / 60)} minutes
                  </div>
                )}
              </div>

              {/* Topics */}
              {conversation.topics && conversation.topics.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
                  {conversation.topics.slice(0, 3).map((topic, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-primary-50 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded text-xs"
                    >
                      <FiTag className="inline mr-1" size={10} />
                      {topic}
                    </span>
                  ))}
                </div>
              )}

              {/* Last Message Preview */}
              {conversation.last_message && (
                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                  <p className="text-sm text-gray-600 dark:text-gray-400 truncate">
                    {conversation.last_message.content}
                  </p>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Conversation Detail Modal */}
      {selectedConversation && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
            {/* Modal Header */}
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                    {selectedConversation.title || 'Conversation Details'}
                  </h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    {format(new Date(selectedConversation.start_timestamp), 'MMM dd, yyyy HH:mm')}
                  </p>
                </div>
                <button
                  onClick={closeDetails}
                  className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 text-2xl"
                >
                  ×
                </button>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-6 overflow-y-auto custom-scrollbar" style={{ maxHeight: 'calc(90vh - 200px)' }}>
              {/* Summary */}
              {selectedConversation.summary && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    Summary
                  </h3>
                  <p className="text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                    {selectedConversation.summary}
                  </p>
                </div>
              )}

              {/* Key Points */}
              {selectedConversation.key_points && selectedConversation.key_points.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    Key Points
                  </h3>
                  <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
                    {selectedConversation.key_points.map((point, index) => (
                      <li key={index}>{point}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Topics & Sentiment */}
              <div className="mb-6 flex gap-4">
                {selectedConversation.topics && selectedConversation.topics.length > 0 && (
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      Topics
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {selectedConversation.topics.map((topic, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 rounded-full text-sm"
                        >
                          {topic}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {selectedConversation.sentiment && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      Sentiment
                    </h3>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        selectedConversation.sentiment === 'positive'
                          ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                          : selectedConversation.sentiment === 'negative'
                          ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                          : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                      }`}
                    >
                      {selectedConversation.sentiment}
                    </span>
                  </div>
                )}
              </div>

              {/* Messages */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                  Messages ({selectedConversation.messages?.length || 0})
                </h3>
                <div className="space-y-4">
                  {selectedConversation.messages?.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg px-4 py-3 ${
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
                          {format(new Date(message.timestamp), 'HH:mm:ss')}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ConversationsDashboard

