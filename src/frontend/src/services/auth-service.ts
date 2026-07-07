/**
 * Auth Service
 * Handles authentication API calls
 */

import { ApiClient, AuthError } from './api-client';
import { TokenRequest, TokenResponse, Identity } from '../types';

export class AuthService {
  constructor(private client: ApiClient) {}

  async getOAuthUrl(): Promise<{ url: string }> {
    const response = await this.client.get<{ url: string }>('/auth/github/url');
    return response.data;
  }

  async handleOAuthCallback(code: string): Promise<TokenResponse> {
    const response = await this.client.post<TokenResponse>('/auth/github/callback', { code });
    return response.data;
  }

  async issueToken(request: TokenRequest): Promise<TokenResponse> {
    const response = await this.client.post<TokenResponse>('/auth/token', request);
    return response.data;
  }

  async refreshToken(): Promise<TokenResponse> {
    const response = await this.client.post<TokenResponse>('/auth/refresh', {});
    return response.data;
  }

  async logout(): Promise<void> {
    await this.client.post<void>('/auth/logout', {});
  }

  async getCurrentIdentity(): Promise<Identity> {
    const response = await this.client.get<Identity>('/auth/me');
    return response.data;
  }
}
