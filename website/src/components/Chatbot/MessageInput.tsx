import React, { useState, useRef, useEffect } from 'react';
import styles from './ChatbotStyles.module.css';

interface MessageInputProps {
  onSend: (text: string) => void;
  isLoading: boolean;
  onCancel?: () => void; // Optional cancel callback
}

const MessageInput: React.FC<MessageInputProps> = ({ onSend, isLoading, onCancel }) => {
  const [text, setText] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 100)}px`;
    }
  }, [text]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim() && !isLoading) {
      onSend(text.trim());
      setText('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Submit on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (text.trim() && !isLoading) {
        onSend(text.trim());
        setText('');
      }
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
  };

  const handleCancel = () => {
    if (isLoading && onCancel) {
      onCancel();
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.messageInputArea} role="form" aria-label="Chat message input form">
      <textarea
        ref={textareaRef}
        className={styles.messageInput}
        value={text}
        onChange={handleInput}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question about the book..."
        aria-label="Type your message"
        aria-required="true"
        disabled={isLoading}
        rows={1}
        maxLength={1000}
      />
      {isLoading ? (
        <button
          type="button"
          className={styles.cancelButton}
          onClick={handleCancel}
          aria-label="Cancel request"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M6 18L18 6M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </button>
      ) : (
        <button
          type="submit"
          className={styles.sendButton}
          disabled={text.trim() === '' || isLoading}
          aria-label="Send message"
          aria-disabled={text.trim() === '' || isLoading}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </button>
      )}
    </form>
  );
};

export default MessageInput;