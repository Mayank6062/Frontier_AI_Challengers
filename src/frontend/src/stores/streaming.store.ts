/**
 * Streaming Store
 * Manages WebSocket/SSE connection state and event handling
 */

import { create } from 'zustand';

interface StreamEvent {
  id: string;
  type: string;
  data: unknown;
  timestamp: string;
}

interface StreamingStore {
  connectionStatus: 'connected' | 'connecting' | 'disconnected' | 'error';
  activeStreamId: string | null;
  pendingEvents: StreamEvent[];
  lastEventId: string | null;
  error: string | null;

  // Actions
  setConnected: () => void;
  setConnecting: () => void;
  setDisconnected: () => void;
  setError: (error: string) => void;
  setActiveStream: (streamId: string) => void;
  queueEvent: (event: StreamEvent) => void;
  processEvent: (eventId: string) => void;
  setLastEventId: (eventId: string) => void;
  clearPendingEvents: () => void;
}

export const useStreamingStore = create<StreamingStore>((set) => ({
  connectionStatus: 'disconnected',
  activeStreamId: null,
  pendingEvents: [],
  lastEventId: null,
  error: null,

  setConnected: () =>
    set({
      connectionStatus: 'connected',
      error: null,
    }),

  setConnecting: () =>
    set({
      connectionStatus: 'connecting',
    }),

  setDisconnected: () =>
    set({
      connectionStatus: 'disconnected',
    }),

  setError: (error) =>
    set({
      connectionStatus: 'error',
      error,
    }),

  setActiveStream: (streamId) =>
    set({
      activeStreamId: streamId,
    }),

  queueEvent: (event) =>
    set((state) => ({
      pendingEvents: [...state.pendingEvents, event],
    })),

  processEvent: (eventId) =>
    set((state) => ({
      pendingEvents: state.pendingEvents.filter((e) => e.id !== eventId),
      lastEventId: eventId,
    })),

  setLastEventId: (eventId) =>
    set({
      lastEventId: eventId,
    }),

  clearPendingEvents: () =>
    set({
      pendingEvents: [],
    }),
}));
