/**
 * Session Types
 * Aligned with backend session_schemas.py
 */

export interface SessionCreateRequest {
  user_id: string;
  ttl_seconds?: number;
  data?: Record<string, unknown>;
}

export interface SessionResponse {
  id: string;
  user_id: string;
  created_at?: string;
  last_accessed?: string;
  expires_at?: string;
  data?: Record<string, unknown>;
}

export interface Session extends SessionResponse {
  name?: string;
  status: 'active' | 'expired' | 'terminated';
}

export interface SessionListResponse {
  sessions: Session[];
  total: number;
  limit: number;
  offset: number;
}

export interface SessionLoadingState {
  isLoading: boolean;
  error: string | null;
}
