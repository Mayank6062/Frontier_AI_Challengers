/**
 * Base API Client
 * Handles authentication, correlation IDs, error normalization, retries
 */

import axios, { AxiosInstance, AxiosError, AxiosResponse } from 'axios';
import { ApiResponse, ApiError } from '../types';

class FrontendError extends Error {
  constructor(
    public code: string,
    message: string,
    public details?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'FrontendError';
  }
}

class ValidationError extends FrontendError {
  constructor(message: string, details?: Record<string, unknown>) {
    super('VALIDATION_ERROR', message, details);
    this.name = 'ValidationError';
  }
}

class AuthError extends FrontendError {
  constructor(message: string, details?: Record<string, unknown>) {
    super('AUTH_ERROR', message, details);
    this.name = 'AuthError';
  }
}

class NotFoundError extends FrontendError {
  constructor(message: string, details?: Record<string, unknown>) {
    super('NOT_FOUND', message, details);
    this.name = 'NotFoundError';
  }
}

class RateLimitError extends FrontendError {
  constructor(message: string, details?: Record<string, unknown>) {
    super('RATE_LIMIT', message, details);
    this.name = 'RateLimitError';
  }
}

class ServiceError extends FrontendError {
  constructor(message: string, details?: Record<string, unknown>) {
    super('SERVICE_ERROR', message, details);
    this.name = 'ServiceError';
  }
}

export class ApiClient {
  private client: AxiosInstance;
  private tokenRefreshPromise: Promise<string> | null = null;

  constructor(baseURL: string, private getToken: () => string | null, private onTokenRefresh?: (token: string) => void) {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor: add auth and correlation ID
    this.client.interceptors.request.use((config) => {
      const token = this.getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      config.headers['X-Correlation-ID'] = this.generateCorrelationId();
      return config;
    });

    // Response interceptor: normalize and handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => this.handleError(error)
    );
  }

  async get<T>(path: string, params?: Record<string, unknown>): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.get<T>(path, { params });
      return { data: response.data, error: null, status: response.status };
    } catch (error) {
      throw this.normalizeError(error);
    }
  }

  async post<T>(path: string, payload: unknown): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.post<T>(path, payload);
      return { data: response.data, error: null, status: response.status };
    } catch (error) {
      throw this.normalizeError(error);
    }
  }

  async put<T>(path: string, payload: unknown): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.put<T>(path, payload);
      return { data: response.data, error: null, status: response.status };
    } catch (error) {
      throw this.normalizeError(error);
    }
  }

  async delete<T>(path: string): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.delete<T>(path);
      return { data: response.data, error: null, status: response.status };
    } catch (error) {
      throw this.normalizeError(error);
    }
  }

  private generateCorrelationId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private async handleError(error: AxiosError) {
    if (!error.response) {
      throw new ServiceError('Network error. Please check your connection.');
    }

    const status = error.response.status;
    const data = error.response.data as Record<string, unknown>;

    switch (status) {
      case 400:
        throw new ValidationError(data.detail as string || 'Validation failed', data);
      case 401:
        throw new AuthError(data.detail as string || 'Authentication required', data);
      case 403:
        throw new AuthError('Access forbidden', data);
      case 404:
        throw new NotFoundError(data.detail as string || 'Resource not found', data);
      case 429:
        throw new RateLimitError('Too many requests. Please try again later.', data);
      case 500:
      case 502:
      case 503:
      case 504:
        throw new ServiceError(
          data.detail as string || 'Server error. Please try again later.',
          data
        );
      default:
        throw new ServiceError(`Error ${status}: ${data.detail || 'Unknown error'}`, data);
    }
  }

  private normalizeError(error: unknown): FrontendError {
    if (error instanceof FrontendError) {
      return error;
    }
    if (error instanceof AxiosError) {
      return this.handleError(error) as any;
    }
    return new ServiceError('An unexpected error occurred');
  }
}

export { FrontendError, ValidationError, AuthError, NotFoundError, RateLimitError, ServiceError };
