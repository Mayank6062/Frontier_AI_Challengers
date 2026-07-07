/**
 * Streaming Service
 * Manages WebSocket/SSE connections for real-time streaming
 */

import { ApiClient } from './api-client';

export interface StreamingEvent {
  id: string;
  type: string;
  data: unknown;
  timestamp: string;
}

export type StreamEventHandler = (event: StreamingEvent) => void;

export class StreamingService {
  private websocket: WebSocket | null = null;
  private eventSource: EventSource | null = null;
  private handlers: Map<string, StreamEventHandler[]> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  constructor(
    private baseUrl: string,
    private getToken: () => string | null,
    private onConnectionChange?: (connected: boolean) => void
  ) {}

  async connectWebSocket(sessionId: string, correlationId: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const wsUrl = `${this.baseUrl.replace(/^http/, 'ws')}/sessions/${sessionId}/stream?correlation_id=${correlationId}`;
      const token = this.getToken();

      this.websocket = new WebSocket(wsUrl);

      this.websocket.onopen = () => {
        if (token) {
          this.websocket!.send(JSON.stringify({ type: 'auth', token }));
        }
        this.reconnectAttempts = 0;
        this.onConnectionChange?.(true);
        resolve();
      };

      this.websocket.onmessage = (event) => {
        try {
          const streamEvent = JSON.parse(event.data) as StreamingEvent;
          this.dispatch(streamEvent.type, streamEvent);
        } catch (error) {
          console.error('Failed to parse stream event:', error);
        }
      };

      this.websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.onConnectionChange?.(false);
        reject(error);
      };

      this.websocket.onclose = () => {
        this.onConnectionChange?.(false);
        this.attemptReconnect(sessionId, correlationId);
      };
    });
  }

  /**
   * Connect via Server-Sent Events
   */
  async connectSSE(sessionId: string, correlationId: string): Promise<void> {
    const token = this.getToken();
    const headers: Record<string, string> = {
      'X-Correlation-ID': correlationId,
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    const url = `${this.baseUrl}/sessions/${sessionId}/stream/events?correlation_id=${correlationId}`;

    this.eventSource = new EventSource(url);

    this.eventSource.onopen = () => {
      this.reconnectAttempts = 0;
      this.onConnectionChange?.(true);
    };

    this.eventSource.onmessage = (event) => {
      try {
        const streamEvent = JSON.parse(event.data) as StreamingEvent;
        this.dispatch(streamEvent.type, streamEvent);
      } catch (error) {
        console.error('Failed to parse SSE event:', error);
      }
    };

    this.eventSource.onerror = () => {
      this.onConnectionChange?.(false);
      this.attemptReconnect(sessionId, correlationId);
    };
  }

  /**
   * Register event handler
   */
  on(eventType: string, handler: StreamEventHandler): void {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, []);
    }
    this.handlers.get(eventType)!.push(handler);
  }

  /**
   * Unregister event handler
   */
  off(eventType: string, handler: StreamEventHandler): void {
    const handlers = this.handlers.get(eventType);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
  }

  /**
   * Send message through WebSocket
   */
  send(message: Record<string, unknown>): void {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      this.websocket.send(JSON.stringify(message));
    }
  }

  /**
   * Close connection
   */
  close(): void {
    if (this.websocket) {
      this.websocket.close();
      this.websocket = null;
    }
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
    this.onConnectionChange?.(false);
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return (
      (this.websocket !== null && this.websocket.readyState === WebSocket.OPEN) ||
      (this.eventSource !== null && this.eventSource.readyState === EventSource.OPEN)
    );
  }

  /**
   * Dispatch event to handlers
   */
  private dispatch(eventType: string, event: StreamingEvent): void {
    const handlers = this.handlers.get(eventType);
    if (handlers) {
      handlers.forEach((handler) => {
        try {
          handler(event);
        } catch (error) {
          console.error(`Error in event handler for ${eventType}:`, error);
        }
      });
    }
  }

  /**
   * Attempt to reconnect
   */
  private attemptReconnect(sessionId: string, correlationId: string): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
      console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
      setTimeout(() => {
        this.connectWebSocket(sessionId, correlationId).catch((error) => {
          console.error('Reconnection failed:', error);
        });
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }
}
