/**
 * useAuth Hook
 * Provides access to auth state and actions
 */

import { useCallback } from 'react';
import { useAuthStore } from '../stores';

export const useAuth = () => {
  const status = useAuthStore((state) => state.status);
  const identity = useAuthStore((state) => state.identity);
  const tokenExpiresAt = useAuthStore((state) => state.tokenExpiresAt);

  const setAuthenticated = useCallback(
    (identity: any, expiresAt: string) => {
      useAuthStore.getState().setAuthenticated(identity, expiresAt);
    },
    []
  );

  const setUnauthenticated = useCallback(() => {
    useAuthStore.getState().setUnauthenticated();
  }, []);

  const setExpired = useCallback(() => {
    useAuthStore.getState().setExpired();
  }, []);

  const isAuthenticated = status === 'authenticated';
  const isLoading = status === 'loading';

  return {
    status,
    identity,
    tokenExpiresAt,
    isAuthenticated,
    isLoading,
    setAuthenticated,
    setUnauthenticated,
    setExpired,
  };
};
