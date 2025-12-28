import React, { useState, useEffect, useRef } from 'react';
import ChatbotButton from './ChatbotButton';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { sendQueryWithRetry, checkHealth } from './api';
import styles from './ChatbotStyles.module.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  sources?: string[];
}

const ChatbotPanel: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || isLoading) return;

    // Create an AbortController for request cancellation and store it in ref
    const abortController = new AbortController();
    abortControllerRef.current = abortController;

    // Add user message to the conversation
    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Send query to backend with retry logic
      const response = await sendQueryWithRetry({
        question: text,
      }, 3, abortController.signal);

      // Add bot response to the conversation
      const botMessage: Message = {
        id: Date.now().toString(),
        text: response.content,
        sender: 'bot',
        timestamp: new Date(),
        sources: response.sources,
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      const errorMessageText = err instanceof Error ? err.message : 'An error occurred while processing your request';

      // Handle specific error messages as requested
      let displayMessage = '';
      if (errorMessageText === 'Request interrupted by user') {
        displayMessage = 'Request interrupted by user';
      } else if (errorMessageText === 'API request failed: 422') {
        displayMessage = 'Sorry, I encountered an error while processing your request. API request failed: 422';
      } else {
        displayMessage = `Sorry, I encountered an error while processing your request. ${errorMessageText}`;
      }

      setError(displayMessage);

      // Add error message to the conversation
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: displayMessage,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      // Clear the abort controller reference after request completes
      abortControllerRef.current = null;
    }
  };

  const handleCancel = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      // Clear the abort controller reference after aborting
      abortControllerRef.current = null;
      setIsLoading(false);

      // Add user-interrupted message to the conversation
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: 'Request interrupted by user',
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    }
  };

  // Check backend health on component mount
  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        await checkHealth();
      } catch (err) {
        setError('Backend service is not available. Some features may not work properly.');
      }
    };

    checkBackendHealth();
  }, []);

  return (
    <>
      <ChatbotButton onClick={handleToggle} isOpen={isOpen} />
      {isOpen && (
        <div className={styles.chatbotPanel}>
          <div className={styles.chatHeader}>
            <h3>AI Assistant</h3>
            <button onClick={handleToggle} aria-label="Close chat">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              </svg>
            </button>
          </div>
          <MessageList
            messages={messages}
            isLoading={isLoading}
            error={error}
          />
          <MessageInput onSend={handleSendMessage} isLoading={isLoading} onCancel={handleCancel} />
          <div ref={messagesEndRef} />
        </div>
      )}
    </>
  );
};

export default ChatbotPanel;