/**
 * Chat Service
 * Handles chat message API calls
 */

import { ApiClient } from './api-client';
import { ChatMessage, ChatRequest, ChatResponse, PaginationParams } from '../types';

export class ChatService {
  constructor(private client: ApiClient) {}

  async submitMessage(sessionId: string, request: ChatRequest): Promise<ChatResponse> {
    const response = await this.client.post<ChatResponse>(
      `/sessions/${sessionId}/chat/message`,
      request
    );
    return response.data;
  }

  async loadMessageHistory(sessionId: string, params?: PaginationParams): Promise<ChatMessage[]> {
    const response = await this.client.get<ChatMessage[]>(
      `/sessions/${sessionId}/chat/history`,
      params as Record<string, unknown>
    );
    return response.data;
  }

  async getSpecificMessage(sessionId: string, messageId: string): Promise<ChatMessage> {
    const response = await this.client.get<ChatMessage>(
      `/sessions/${sessionId}/chat/message/${messageId}`
    );
    return response.data;
  }

  async streamMessage(
    sessionId: string,
    request: ChatRequest,
    onChunk: (chunk: string) => void,
    onComplete: () => void,
    onError: (error: Error) => void
  ): Promise<void> {
    try {
      // This will be handled by StreamingService instead
      // For now, just delegate to standard submit
      await this.submitMessage(sessionId, request);
      onComplete();
    } catch (error) {
      onError(error instanceof Error ? error : new Error('Streaming failed'));
    }
  }
}
