/**
 * This file serves as a Docusaurus page that also acts as a global component
 * The ChatbotPanel will be rendered on all pages by including it in the layout
 */

import React from 'react';
import ChatbotPanel from '../components/Chatbot/ChatbotPanel';

// This component will render the chatbot panel which will be fixed positioned
// and accessible from all pages
const ChatbotPage: React.FC = () => {
  return <ChatbotPanel />;
};

export default ChatbotPage;