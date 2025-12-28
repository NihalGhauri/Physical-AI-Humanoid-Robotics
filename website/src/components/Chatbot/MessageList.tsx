import React from 'react';
import styles from './ChatbotStyles.module.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  sources?: string[];
}

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
}

const MessageList: React.FC<MessageListProps> = ({ messages, isLoading, error }) => {
  return (
    <div className={styles.messageList}>
      {messages.length === 0 ? (
        <div className={styles.botMessage + ' ' + styles.message}>
          Hello! I'm your AI assistant. Ask me anything about the Physical AI & Humanoid Robotics textbook.
        </div>
      ) : (
        messages.map((message) => (
          <div
            key={message.id}
            className={`${styles.message} ${
              message.sender === 'user' ? styles.userMessage : styles.botMessage
            }`}
          >
            {message.text}
            {message.sources && message.sources.length > 0 && (
              <div className={styles.sources}>
                <h4>SOURCES:</h4>
                <ul className={styles.sourcesList}>
                  {message.sources.map((source, index) => (
                    <li key={index}>
                      <a href={source} target="_blank" rel="noopener noreferrer">
                        {source}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))
      )}

      {error && (
        <div className={styles.botMessage + ' ' + styles.message}>
          {error}
        </div>
      )}

      {isLoading && (
        <div className={styles.botMessage + ' ' + styles.message}>
          <div className={styles.loadingIndicator}>
            <span>Thinking</span>
            <div className={styles.loadingDots}>
              <div className={styles.loadingDot}></div>
              <div className={styles.loadingDot}></div>
              <div className={styles.loadingDot}></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageList;