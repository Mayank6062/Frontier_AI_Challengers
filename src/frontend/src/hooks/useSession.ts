/**
 * useSession Hook
 * Provides access to session state and actions
 */

import { useCallback } from 'react';
import { useSessionStore } from '../stores';
import { Session } from '../types';

export const useSession = () => {
  const sessions = useSessionStore((state) => state.sessions);
  const activeSessionId = useSessionStore((state) => state.activeSessionId);
  const isLoading = useSessionStore((state) => state.isLoading);
  const error = useSessionStore((state) => state.error);
  const searchQuery = useSessionStore((state) => state.searchQuery);

  const activeSession = sessions.find((s) => s.id === activeSessionId);
  const filteredSessions = searchQuery
    ? sessions.filter((s) =>
        (s.name || '').toLowerCase().includes(searchQuery.toLowerCase())
      )
    : sessions;

  const setSessions = useCallback((sessions: Session[]) => {
    useSessionStore.getState().setSessions(sessions);
  }, []);

  const setActiveSession = useCallback((sessionId: string) => {
    useSessionStore.getState().setActiveSession(sessionId);
  }, []);

  const addSession = useCallback((session: Session) => {
    useSessionStore.getState().addSession(session);
  }, []);

  const updateSession = useCallback((sessionId: string, updates: Partial<Session>) => {
    useSessionStore.getState().updateSession(sessionId, updates);
  }, []);

  const deleteSession = useCallback((sessionId: string) => {
    useSessionStore.getState().deleteSession(sessionId);
  }, []);

  const setLoading = useCallback((isLoading: boolean) => {
    useSessionStore.getState().setLoading(isLoading);
  }, []);

  const setError = useCallback((error: string | null) => {
    useSessionStore.getState().setError(error);
  }, []);

  const setSearchQuery = useCallback((query: string) => {
    useSessionStore.getState().setSearchQuery(query);
  }, []);

  return {
    sessions,
    activeSession,
    activeSessionId,
    filteredSessions,
    isLoading,
    error,
    searchQuery,
    setSessions,
    setActiveSession,
    addSession,
    updateSession,
    deleteSession,
    setLoading,
    setError,
    setSearchQuery,
  };
};
