import React from 'react';
import { Session } from '../../types/session.types';
import { SessionCard } from './SessionCard';
import { SessionSearch } from './SessionSearch';
import { Button } from '../shared/Button';
import styles from './SessionSidebar.module.css';

interface SessionSidebarProps {
  sessions: Session[];
  activeSessionId?: string;
  onSessionSelect: (sessionId: string) => void;
  onSessionCreate: () => void;
  onSessionRename: (sessionId: string) => void;
  onSessionDelete: (sessionId: string) => void;
  onSearch: (query: string) => void;
  isLoading?: boolean;
}

/**
 * SessionSidebar - Left panel showing list of sessions
 */
export const SessionSidebar: React.FC<SessionSidebarProps> = ({
  sessions,
  activeSessionId,
  onSessionSelect,
  onSessionCreate,
  onSessionRename,
  onSessionDelete,
  onSearch,
  isLoading = false,
}) => {
  return (
    <div className={styles.sidebar}>
      <div className={styles.header}>
        <h2 className={styles.title}>Sessions</h2>
        <Button
          variant="primary"
          size="sm"
          onClick={onSessionCreate}
          disabled={isLoading}
        >
          New
        </Button>
      </div>

      <SessionSearch onSearch={onSearch} />

      <div className={styles.list}>
        {sessions.map((session) => (
          <SessionCard
            key={session.id}
            session={session}
            isActive={session.id === activeSessionId}
            onSelect={onSessionSelect}
            onRename={onSessionRename}
            onDelete={onSessionDelete}
          />
        ))}
      </div>
    </div>
  );
};

export default SessionSidebar;
