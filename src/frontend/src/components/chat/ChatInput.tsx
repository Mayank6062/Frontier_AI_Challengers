import React, { useState, useRef } from 'react';
import { Button } from '../shared/Button';
import styles from './ChatInput.module.css';

interface ChatInputProps {
  onSubmit: (message: string) => Promise<void>;
  isLoading?: boolean;
  placeholder?: string;
  maxLength?: number;
}

/**
 * ChatInput - User message input component with send button
 */
export const ChatInput: React.FC<ChatInputProps> = ({
  onSubmit,
  isLoading = false,
  placeholder = 'Type your message...',
  maxLength = 2000,
}) => {
  const [message, setMessage] = useState('');
  const [error, setError] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value.slice(0, maxLength);
    setMessage(value);
    setError(null);

    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        200
      )}px`;
    }
  };

  const handleSubmit = async () => {
    const trimmed = message.trim();

    if (!trimmed) {
      setError('Message cannot be empty');
      return;
    }

    if (trimmed.length > maxLength) {
      setError(`Message exceeds ${maxLength} character limit`);
      return;
    }

    try {
      await onSubmit(trimmed);
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    } catch (err) {
      const msg =
        err instanceof Error ? err.message : 'Failed to send message';
      setError(msg);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className={styles.container}>
      {error && <div className={styles.error}>{error}</div>}

      <div className={styles.inputGroup}>
        <textarea
          ref={textareaRef}
          className={styles.textarea}
          placeholder={placeholder}
          value={message}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          rows={1}
        />

        <Button
          variant="primary"
          size="md"
          onClick={handleSubmit}
          disabled={isLoading || !message.trim()}
          className={styles.button}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </Button>
      </div>

      <p className={styles.hint}>
        {message.length}/{maxLength} characters • Ctrl+Enter to send
      </p>
    </div>
  );
};

export default ChatInput;
