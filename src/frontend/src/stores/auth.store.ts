/**
 * Auth Store
 * Manages authentication state: token, identity, expiry
 */

import { create } from 'zustand';
import { AuthState, Identity } from '../types';

interface AuthStore {
  status: 'loading' | 'authenticated' | 'unauthenticated' | 'expired';
  identity: Identity | null;
  tokenExpiresAt: string | null;

  // Actions
  setAuthenticated: (identity: Identity, expiresAt: string) => void;
  setUnauthenticated: () => void;
  setExpired: () => void;
  setLoading: (isLoading: boolean) => void;
  refreshToken: (expiresAt: string) => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  status: 'loading',
  identity: null,
  tokenExpiresAt: null,

  setAuthenticated: (identity, expiresAt) =>
    set({
      status: 'authenticated',
      identity,
      tokenExpiresAt: expiresAt,
    }),

  setUnauthenticated: () =>
    set({
      status: 'unauthenticated',
      identity: null,
      tokenExpiresAt: null,
    }),

  setExpired: () =>
    set({
      status: 'expired',
      identity: null,
      tokenExpiresAt: null,
    }),

  setLoading: (isLoading) =>
    set({
      status: isLoading ? 'loading' : 'unauthenticated',
    }),

  refreshToken: (expiresAt) =>
    set({
      tokenExpiresAt: expiresAt,
    }),
}));
