/**
 * Session Service
 * Handles session management API calls
 */

import { ApiClient } from './api-client';
import { Session, SessionCreateRequest, SessionResponse, SessionListResponse, PaginationParams } from '../types';

export class SessionService {
  constructor(private client: ApiClient) {}

  async listSessions(params?: PaginationParams): Promise<SessionListResponse> {
    const response = await this.client.get<SessionListResponse>('/sessions', params as Record<string, unknown>);
    return response.data;
  }

  async getSession(sessionId: string): Promise<Session> {
    const response = await this.client.get<Session>(`/sessions/${sessionId}`);
    return response.data;
  }

  async createSession(request: SessionCreateRequest): Promise<SessionResponse> {
    const response = await this.client.post<SessionResponse>('/sessions', request);
    return response.data;
  }

  async updateSession(sessionId: string, updates: Partial<Session>): Promise<Session> {
    const response = await this.client.put<Session>(`/sessions/${sessionId}`, updates);
    return response.data;
  }

  async deleteSession(sessionId: string): Promise<void> {
    await this.client.delete<void>(`/sessions/${sessionId}`);
  }

  async renameSession(sessionId: string, name: string): Promise<Session> {
    const response = await this.client.put<Session>(`/sessions/${sessionId}`, { name });
    return response.data;
  }

  async updateSessionActivity(sessionId: string): Promise<Session> {
    const response = await this.client.put<Session>(`/sessions/${sessionId}/activity`, {
      last_accessed_at: new Date().toISOString(),
    });
    return response.data;
  }
}
