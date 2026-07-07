import React from 'react';
import { useChat } from '../../hooks/useChat';
import { chatService } from '../../services';
import { ChatRequest } from '../../types/engagement.types';
import { ChatHistory } from './ChatHistory';
import { ChatInput } from './ChatInput';
import styles from './ChatPanel.module.css';

interface ChatPanelProps {
  sessionId?: string;
}

/**
 * ChatPanel - Main chat interface component
 */
export const ChatPanel: React.FC<ChatPanelProps> = ({ sessionId }) => {
  const {
    messages,
    inputText,
    isSubmitting,
    streamingMessage,
    addMessage,
  } = useChat();

  const handleSubmit = async (message: string) => {
    if (!sessionId) {
      console.error('No session ID available');
      return;
    }

    try {
      console.log('Submitting message:', message, 'sessionId:', sessionId);
      const request: ChatRequest = {
        content: message,
      };

      const response = await chatService.submitMessage(sessionId, request);
      console.log('Received response:', response);
      
      // Add the received message to the store
      if (response && response.message) {
        console.log('Adding message to store:', response.message);
        addMessage(response.message);
        console.log('Message added to store');
      } else {
        console.warn('Response missing message field:', response);
      }
    } catch (error) {
      const msg =
        error instanceof Error ? error.message : 'Failed to send message';
      console.error('Message submission error:', error);
      throw new Error(msg);
    }
  };

  return (
    <div className={styles.panel}>
      <ChatHistory
        messages={messages}
        isLoading={isSubmitting}
      />
      <ChatInput
        onSubmit={handleSubmit}
        isLoading={isSubmitting}
      />
    </div>
  );
};

export default ChatPanel;
