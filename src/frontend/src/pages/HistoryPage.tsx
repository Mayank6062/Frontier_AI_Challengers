/**
 * History Page
 * View past sessions and engagement history
 */

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSession } from '../hooks';
import { SessionSearch } from '../components/sessions/SessionSearch';
import { SessionCard } from '../components/sessions/SessionCard';
import { Button } from '../components/shared/Button';
import { sessionService } from '../services';
import { ROUTES } from '../constants';
import styles from './HistoryPage.module.css';

export const HistoryPage: React.FC = () => {
  const navigate = useNavigate();
  const { sessions, isLoading } = useSession();
  const [searchQuery, setSearchQuery] = useState('');

  // Load sessions on mount
  useEffect(() => {
    const loadSessions = async () => {
      try {
        await sessionService.listSessions();
      } catch (err) {
        console.error('Failed to load sessions:', err);
      }
    };

    loadSessions();
  }, []);

  const filteredSessions = sessions.filter((session) =>
    (session.name || '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSessionSelect = (sessionId: string) => {
    navigate(`${ROUTES.WORKSPACE}/${sessionId}`);
  };

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Session History</h1>
          <p className={styles.subtitle}>
            View and restore your past sessions
          </p>
        </div>
        <Button
          variant="primary"
          onClick={() => navigate(ROUTES.WORKSPACE)}
        >
          New Session
        </Button>
      </div>

      <SessionSearch
        onSearch={setSearchQuery}
        placeholder="Search sessions by name..."
      />

      <div className={styles.sessions}>
        {isLoading ? (
          <div className={styles.loading}>Loading sessions...</div>
        ) : filteredSessions.length === 0 ? (
          <div className={styles.empty}>
            No sessions found
            {searchQuery && ` matching "${searchQuery}"`}
          </div>
        ) : (
          filteredSessions.map((session) => (
            <SessionCard
              key={session.id}
              session={session}
              onSelect={handleSessionSelect}
            />
          ))
        )}
      </div>
    </div>
  );
};
