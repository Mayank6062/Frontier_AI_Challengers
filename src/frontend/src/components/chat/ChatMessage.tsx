import React from 'react';
import { ChatMessage as ChatMessageType } from '../../types/engagement.types';
import { Badge } from '../shared/Badge';
import { CitationTag } from '../shared/CitationTag';
import styles from './ChatMessage.module.css';

interface ChatMessageProps {
  message: ChatMessageType;
}

/**
 * ChatMessage - Renders a single chat message with markdown and citations
 */
export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`${styles.message} ${styles[message.role]}`}>
      <div className={styles.avatar}>
        {isUser ? 'U' : 'AI'}
      </div>

      <div className={styles.content}>
        <div className={styles.header}>
          <span className={styles.role}>
            {isUser ? 'You' : 'ArchitectIQ'}
          </span>
          <time className={styles.timestamp}>
            {message.timestamp ? new Date(message.timestamp).toLocaleTimeString() : 'N/A'}
          </time>
        </div>

        <div
          className={styles.text}
          dangerouslySetInnerHTML={{
            __html: message.content,
          }}
        />

        {message.metadata && typeof message.metadata === 'object' && 'citations' in message.metadata && Array.isArray((message.metadata as any).citations) && (
          <div className={styles.citations}>
            {((message.metadata as any).citations as Array<{ source: string; confidence?: number }>).map((citation) => (
              <CitationTag
                key={citation.source}
                source={citation.source}
                confidence={citation.confidence}
              />
            ))}
          </div>
        )}

        {message.metadata && typeof message.metadata === 'object' && 'agent_name' in message.metadata && (
          <Badge>{String((message.metadata as any).agent_name)}</Badge>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
