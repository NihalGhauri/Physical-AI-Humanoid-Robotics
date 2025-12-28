import React from 'react';
import ChatbotPanel from './Chatbot/ChatbotPanel';

interface LayoutWrapperProps {
  children: React.ReactNode;
}

const LayoutWrapper: React.FC<LayoutWrapperProps> = ({ children }) => {
  return (
    <>
      {children}
      <ChatbotPanel />
    </>
  );
};

export default LayoutWrapper;