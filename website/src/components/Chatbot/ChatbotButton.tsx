import React, { useState, useEffect } from 'react';
import styles from './ChatbotStyles.module.css';

interface ChatbotButtonProps {
  onClick: () => void;
  isOpen: boolean;
}

const ChatbotButton: React.FC<ChatbotButtonProps> = ({ onClick, isOpen }) => {
  const [isVisible, setIsVisible] = useState(true);

  // Handle scroll to hide/show button appropriately
  useEffect(() => {
    const handleScroll = () => {
      // Hide button when scrolling down, show when scrolling up
      const currentScrollY = window.scrollY;
      if (currentScrollY > 100) {
        setIsVisible(false);
      } else {
        setIsVisible(true);
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <button
      className={`${styles.chatbotButton} ${isOpen ? styles.open : ''} ${!isVisible ? styles.hidden : ''}`}
      onClick={onClick}
      aria-label={isOpen ? 'Close chatbot' : 'Open chatbot'}
      title={isOpen ? 'Close chatbot' : 'Open chatbot'}
      aria-expanded={isOpen}
      role="button"
    >
      {isOpen ? (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <title>Close chat</title>
          <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        </svg>
      ) : (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <title>Open chat</title>
          <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M12 8V8.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M8 12V12.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M16 12V12.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      )}
    </button>
  );
};

export default ChatbotButton;