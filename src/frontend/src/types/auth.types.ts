/**
 * Authentication Types
 * Aligned with backend auth_schemas.py
 */

export interface TokenRequest {
  username: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface Identity {
  id: string;
  username: string;
  email?: string;
  avatar_url?: string;
}

export interface AuthState {
  status: 'loading' | 'authenticated' | 'unauthenticated' | 'expired';
  identity: Identity | null;
  tokenExpiresAt: string | null;
}

export interface AuthError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}
