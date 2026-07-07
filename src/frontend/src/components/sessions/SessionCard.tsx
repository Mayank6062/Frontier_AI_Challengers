import React from 'react';
import { Session } from '../../types/session.types';
import { Button } from '../shared/Button';
import { Card } from '../shared/Card';
import styles from './SessionCard.module.css';

interface SessionCardProps {
  session: Session;
  isActive?: boolean;
  onSelect: (sessionId: string) => void;
  onRename?: (sessionId: string) => void;
  onDelete?: (sessionId: string) => void;
}

/**
 * SessionCard - Displays a single session in the session list
 */
export const SessionCard: React.FC<SessionCardProps> = ({
  session,
  isActive = false,
  onSelect,
  onRename,
  onDelete,
}) => {
  return (
    <Card
      className={`${styles.card} ${isActive ? styles.active : ''}`}
      onClick={() => onSelect(session.id)}
    >
      <div className={styles.header}>
        <h3 className={styles.name}>{session.name}</h3>
        <span className={styles.status}>{session.status}</span>
      </div>

      <div className={styles.meta}>
        <time className={styles.date}>
          {session.created_at ? new Date(session.created_at).toLocaleDateString() : 'N/A'}
        </time>
        <span className={styles.accessed}>
          Accessed:{' '}
          {session.last_accessed ? new Date(session.last_accessed).toLocaleDateString() : 'N/A'}
        </span>
      </div>

      <div className={styles.actions}>
        {onRename && (
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onRename(session.id);
            }}
          >
            Rename
          </Button>
        )}
        {onDelete && (
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onDelete(session.id);
            }}
          >
            Delete
          </Button>
        )}
      </div>
    </Card>
  );
};

export default SessionCard;
