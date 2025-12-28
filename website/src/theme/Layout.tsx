import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatbotPanel from '../components/Chatbot/ChatbotPanel';

type LayoutProps = {
  children: React.ReactNode;
};

const Layout = (props: LayoutProps): JSX.Element => {
  return (
    <>
      <OriginalLayout {...props} />
      <ChatbotPanel />
    </>
  );
};

export default Layout;