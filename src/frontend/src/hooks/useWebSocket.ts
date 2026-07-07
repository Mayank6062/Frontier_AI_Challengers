/**
 * useWebSocket Hook
 * Provides access to streaming state and WebSocket management
 */

import { useCallback } from 'react';
import { useStreamingStore } from '../stores';
import { StreamingService, StreamEventHandler } from '../services';

export const useWebSocket = (streamingService: StreamingService | null) => {
  const connectionStatus = useStreamingStore((state) => state.connectionStatus);
  const activeStreamId = useStreamingStore((state) => state.activeStreamId);
  const pendingEvents = useStreamingStore((state) => state.pendingEvents);
  const lastEventId = useStreamingStore((state) => state.lastEventId);
  const error = useStreamingStore((state) => state.error);

  const connect = useCallback(async (sessionId: string, correlationId: string) => {
    if (!streamingService) return;
    useStreamingStore.getState().setConnecting();
    try {
      await streamingService.connectWebSocket(sessionId, correlationId);
      useStreamingStore.getState().setConnected();
    } catch (err) {
      useStreamingStore.getState().setError(err instanceof Error ? err.message : 'Connection failed');
    }
  }, [streamingService]);

  const disconnect = useCallback(() => {
    if (streamingService) {
      streamingService.close();
      useStreamingStore.getState().setDisconnected();
    }
  }, [streamingService]);

  const on = useCallback(
    (eventType: string, handler: StreamEventHandler) => {
      if (streamingService) {
        streamingService.on(eventType, handler);
      }
    },
    [streamingService]
  );

  const off = useCallback(
    (eventType: string, handler: StreamEventHandler) => {
      if (streamingService) {
        streamingService.off(eventType, handler);
      }
    },
    [streamingService]
  );

  const send = useCallback(
    (message: Record<string, unknown>) => {
      if (streamingService) {
        streamingService.send(message);
      }
    },
    [streamingService]
  );

  const isConnected = connectionStatus === 'connected';
  const isConnecting = connectionStatus === 'connecting';

  return {
    connectionStatus,
    activeStreamId,
    pendingEvents,
    lastEventId,
    error,
    isConnected,
    isConnecting,
    connect,
    disconnect,
    on,
    off,
    send,
  };
};
