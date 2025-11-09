import React, { useState } from 'react'
import { FiSearch, FiMessageSquare, FiCalendar, FiTag } from 'react-icons/fi'
import { format } from 'date-fns'
import apiService from '../services/api'

function ConversationIntelligence() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')

  const handleQuery = async (e) => {
    e.preventDefault()
    
    if (!query.trim()) {
      alert('Please enter a question')
      return
    }

    try {
      setLoading(true)
      setResult(null)

      const filters = {}
      if (dateFrom) filters.date_from = new Date(dateFrom).toISOString()
      if (dateTo) filters.date_to = new Date(dateTo).toISOString()

      const response = await apiService.queryConversations(query, filters)
      
      if (response.success) {
        setResult(response)
      } else {
        alert('Failed to query conversations')
      }
    } catch (error) {
      console.error('Failed to query:', error)
      alert('Failed to query conversations. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const clearSearch = () => {
    setQuery('')
    setResult(null)
    setDateFrom('')
    setDateTo('')
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Conversation Intelligence
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Ask questions about your past conversations and get intelligent insights
        </p>
      </div>

      {/* Query Interface */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <form onSubmit={handleQuery} className="space-y-4">
          {/* Main Query Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Ask a Question
            </label>
            <div className="relative">
              <FiSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., What did I discuss about travel last week?"
                className="w-full pl-12 pr-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
              />
            </div>
          </div>

          {/* Date Filters */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                From Date (Optional)
              </label>
              <input
                type="date"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-gray-900 dark:text-white"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                To Date (Optional)
              </label>
              <input
                type="date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-gray-900 dark:text-white"
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3">
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="flex-1 px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                  Searching...
                </>
              ) : (
                <>
                  <FiSearch className="mr-2" />
                  Search Conversations
                </>
              )}
            </button>
            {result && (
              <button
                type="button"
                onClick={clearSearch}
                className="px-6 py-3 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-900 dark:text-white rounded-lg transition-colors"
              >
                Clear
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Example Queries */}
      {!result && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Example Questions
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {[
              'What topics have I discussed recently?',
              'Show me conversations about technology',
              'What decisions did I make last week?',
              'Find discussions about travel plans',
              'What were my recent project conversations?',
              'Show me positive conversations',
            ].map((example, index) => (
              <button
                key={index}
                onClick={() => setQuery(example)}
                className="text-left px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg text-sm text-gray-700 dark:text-gray-300 transition-colors"
              >
                "{example}"
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* AI Answer */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Answer
            </h3>
            <div className="bg-primary-50 dark:bg-primary-900 border border-primary-200 dark:border-primary-700 rounded-lg p-4">
              <p className="text-gray-900 dark:text-white whitespace-pre-wrap">
                {result.answer}
              </p>
            </div>
          </div>

          {/* Relevant Conversations */}
          {result.relevant_conversations && result.relevant_conversations.length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Relevant Conversations ({result.count})
              </h3>
              <div className="space-y-4">
                {result.relevant_conversations.map((conversation) => (
                  <div
                    key={conversation.id}
                    className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 border border-gray-200 dark:border-gray-600"
                  >
                    <div className="flex justify-between items-start mb-3">
                      <h4 className="font-semibold text-gray-900 dark:text-white">
                        {conversation.title || 'Untitled Conversation'}
                      </h4>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        ID: {conversation.id}
                      </span>
                    </div>

                    <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400 mb-3">
                      <div className="flex items-center">
                        <FiCalendar className="mr-2" />
                        {format(new Date(conversation.start_timestamp), 'MMM dd, yyyy HH:mm')}
                      </div>
                      <div className="flex items-center">
                        <FiMessageSquare className="mr-2" />
                        {conversation.message_count || conversation.messages?.length || 0} messages
                      </div>
                    </div>

                    {/* Topics */}
                    {conversation.topics && conversation.topics.length > 0 && (
                      <div className="mb-3">
                        <div className="flex flex-wrap gap-2">
                          {conversation.topics.map((topic, index) => (
                            <span
                              key={index}
                              className="px-2 py-1 bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 rounded text-xs"
                            >
                              <FiTag className="inline mr-1" size={10} />
                              {topic}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Summary */}
                    {conversation.summary && (
                      <div className="bg-white dark:bg-gray-800 rounded p-3 text-sm text-gray-700 dark:text-gray-300">
                        <strong className="block mb-1">Summary:</strong>
                        {conversation.summary}
                      </div>
                    )}

                    {/* Message Preview */}
                    {conversation.messages && conversation.messages.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-300 dark:border-gray-600">
                        <strong className="block text-xs text-gray-600 dark:text-gray-400 mb-2">
                          Message excerpts:
                        </strong>
                        <div className="space-y-2">
                          {conversation.messages.slice(0, 2).map((message, idx) => (
                            <div
                              key={idx}
                              className={`text-xs p-2 rounded ${
                                message.sender === 'user'
                                  ? 'bg-primary-100 dark:bg-primary-900 text-primary-900 dark:text-primary-100'
                                  : 'bg-gray-200 dark:bg-gray-600 text-gray-900 dark:text-gray-100'
                              }`}
                            >
                              <span className="font-medium">{message.sender}:</span>{' '}
                              {message.content.substring(0, 150)}
                              {message.content.length > 150 ? '...' : ''}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* No Results */}
          {result.count === 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-8 text-center">
              <p className="text-gray-600 dark:text-gray-400">
                No relevant conversations found for your query.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ConversationIntelligence

