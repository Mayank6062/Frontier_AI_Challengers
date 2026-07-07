/**
 * Session Store
 * Manages sessions list, active session, session state
 */

import { create } from 'zustand';
import { Session } from '../types';

interface SessionStore {
  sessions: Session[];
  activeSessionId: string | null;
  isLoading: boolean;
  error: string | null;
  searchQuery: string;

  // Actions
  setSessions: (sessions: Session[]) => void;
  setActiveSession: (sessionId: string) => void;
  addSession: (session: Session) => void;
  updateSession: (sessionId: string, session: Partial<Session>) => void;
  deleteSession: (sessionId: string) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  setSearchQuery: (query: string) => void;
  resetSessions: () => void;
}

export const useSessionStore = create<SessionStore>((set) => ({
  sessions: [],
  activeSessionId: null,
  isLoading: false,
  error: null,
  searchQuery: '',

  setSessions: (sessions) => set({ sessions, isLoading: false }),

  setActiveSession: (sessionId) => set({ activeSessionId: sessionId }),

  addSession: (session) =>
    set((state) => ({
      sessions: [session, ...state.sessions],
      activeSessionId: session.id,
    })),

  updateSession: (sessionId, updates) =>
    set((state) => ({
      sessions: state.sessions.map((s) =>
        s.id === sessionId ? { ...s, ...updates } : s
      ),
    })),

  deleteSession: (sessionId) =>
    set((state) => ({
      sessions: state.sessions.filter((s) => s.id !== sessionId),
      activeSessionId:
        state.activeSessionId === sessionId ? null : state.activeSessionId,
    })),

  setLoading: (isLoading) => set({ isLoading }),

  setError: (error) => set({ error }),

  setSearchQuery: (query) => set({ searchQuery: query }),

  resetSessions: () =>
    set({
      sessions: [],
      activeSessionId: null,
      isLoading: false,
      error: null,
    }),
}));
