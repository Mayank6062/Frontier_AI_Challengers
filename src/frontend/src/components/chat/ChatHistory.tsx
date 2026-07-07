import React, { useEffect, useRef } from 'react';
import { ChatMessage as ChatMessageType } from '../../types/engagement.types';
import { ChatMessage } from './ChatMessage';
import styles from './ChatHistory.module.css';

interface ChatHistoryProps {
  messages: ChatMessageType[];
  isLoading?: boolean;
}

/**
 * ChatHistory - Displays chat message history
 */
export const ChatHistory: React.FC<ChatHistoryProps> = ({
  messages,
  isLoading = false,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop =
        containerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className={styles.container} ref={containerRef}>
      {messages.length === 0 ? (
        <div className={styles.empty}>
          <p>No messages yet. Start a conversation!</p>
        </div>
      ) : (
        messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
          />
        ))
      )}
      {isLoading && (
        <div className={styles.loading}>
          <div className={styles.spinner} />
          <p>Generating response...</p>
        </div>
      )}
    </div>
  );
};

export default ChatHistory;
