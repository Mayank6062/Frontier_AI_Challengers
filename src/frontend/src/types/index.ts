export * from './auth.types';
export * from './session.types';
export * from './engagement.types';

// Common types
export interface ApiResponse<T> {
  data: T;
  error: null;
  status: number;
}

export interface ApiError {
  data: null;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
  status: number;
}

export interface PaginationParams {
  limit?: number;
  offset?: number;
}

export interface LoadingState {
  isLoading: boolean;
  error: string | null;
}
