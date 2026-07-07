/**
 * Error Handler Utility
 * Extracts user-friendly messages from API errors
 */

import { FrontendError, ValidationError, AuthError, NotFoundError, RateLimitError, ServiceError } from '../services';

export interface ParsedError {
  message: string;
  code: string;
  isRetryable: boolean;
  details?: Record<string, unknown>;
}

export const parseError = (error: unknown): ParsedError => {
  if (error instanceof ValidationError) {
    return {
      message: error.message || 'The provided data is invalid. Please check your input and try again.',
      code: error.code,
      isRetryable: false,
      details: error.details,
    };
  }

  if (error instanceof AuthError) {
    return {
      message: error.message || 'You are not authorized to perform this action. Please log in again.',
      code: error.code,
      isRetryable: false,
      details: error.details,
    };
  }

  if (error instanceof NotFoundError) {
    return {
      message: error.message || 'The requested resource was not found.',
      code: error.code,
      isRetryable: false,
      details: error.details,
    };
  }

  if (error instanceof RateLimitError) {
    return {
      message: error.message || 'Too many requests. Please wait a moment before trying again.',
      code: error.code,
      isRetryable: true,
      details: error.details,
    };
  }

  if (error instanceof ServiceError) {
    return {
      message:
        error.message ||
        'A server error occurred. Please try again later. If the problem persists, contact support.',
      code: error.code,
      isRetryable: true,
      details: error.details,
    };
  }

  if (error instanceof FrontendError) {
    return {
      message: error.message || 'An error occurred. Please try again.',
      code: error.code,
      isRetryable: false,
      details: error.details,
    };
  }

  if (error instanceof Error) {
    return {
      message: error.message || 'An unexpected error occurred. Please try again.',
      code: 'UNKNOWN_ERROR',
      isRetryable: true,
    };
  }

  return {
    message: 'An unexpected error occurred. Please try again.',
    code: 'UNKNOWN_ERROR',
    isRetryable: true,
  };
};

export const getErrorMessage = (error: unknown): string => {
  const parsed = parseError(error);
  return parsed.message;
};

export const isRetryableError = (error: unknown): boolean => {
  const parsed = parseError(error);
  return parsed.isRetryable;
};

export const isAuthError = (error: unknown): boolean => {
  return error instanceof AuthError;
};

export const isValidationError = (error: unknown): boolean => {
  return error instanceof ValidationError;
};
