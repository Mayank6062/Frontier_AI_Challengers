/**
 * App Component
 * Main application shell with router, theme provider, and error handling
 */

import React, { useEffect, useCallback } from 'react';
import { AppRouter } from './router';
import { useAuthStore } from './stores';
import { useNotificationStore } from './stores';
import { getErrorMessage } from './utils';
import { authService } from './services';

class ErrorBoundary extends React.Component<{ children: React.ReactNode }, { hasError: boolean }> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
          <div style={{ textAlign: 'center' }}>
            <h1>Something went wrong</h1>
            <button
              onClick={() => window.location.reload()}
              style={{
                padding: '12px 24px',
                fontSize: '16px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              Reload page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

const ToastContainer: React.FC = () => {
  const toasts = useNotificationStore((state) => state.toasts);
  const dismissToast = useNotificationStore((state) => state.dismissToast);

  return (
    <div
      style={{
        position: 'fixed',
        top: '16px',
        right: '16px',
        zIndex: 1070,
        pointerEvents: 'none',
      }}
    >
      {toasts.map((toast) => (
        <div
          key={toast.id}
          style={{
            padding: '16px',
            marginBottom: '8px',
            borderRadius: '4px',
            backgroundColor:
              toast.type === 'success'
                ? '#28a745'
                : toast.type === 'error'
                  ? '#dc3545'
                  : toast.type === 'warning'
                    ? '#ffc107'
                    : '#17a2b8',
            color: 'white',
            pointerEvents: 'auto',
            cursor: 'pointer',
          }}
          onClick={() => dismissToast(toast.id)}
        >
          {toast.message}
        </div>
      ))}
    </div>
  );
};

export const App: React.FC = () => {
  const getToken = useCallback(() => {
    // This will be implemented in Phase 1 when auth is fully set up
    return localStorage.getItem('auth_token');
  }, []);

  // Initialize theme from user preference or system
  useEffect(() => {
    const theme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', theme);
  }, []);

  // Initialize authentication state on app load
  useEffect(() => {
    let mounted = true;

    const initializeAuth = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        
        if (token) {
          // Try to get current identity if we have a token
          try {
            const identity = await authService.getCurrentIdentity();
            if (mounted) {
              const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
              useAuthStore.getState().setAuthenticated(identity, expiresAt);
            }
          } catch (err) {
            // Token is invalid or expired
            if (mounted) {
              localStorage.removeItem('auth_token');
              useAuthStore.getState().setUnauthenticated();
            }
          }
        } else {
          // No token in storage, set as unauthenticated
          if (mounted) {
            useAuthStore.getState().setUnauthenticated();
          }
        }
      } catch (err) {
        // On any error, default to unauthenticated
        if (mounted) {
          useAuthStore.getState().setUnauthenticated();
        }
      }
    };

    void initializeAuth();

    return () => {
      mounted = false;
    };
  }, []);

  // Handle token refresh logic (will be enhanced in Phase 1)
  useEffect(() => {
    let mounted = true;
    const refreshInterval = 60 * 1000; // check every minute

    const checkAndRefresh = async () => {
      try {
        const { tokenExpiresAt, refreshToken, setExpired, setAuthenticated } = useAuthStore.getState() as any;
        if (!tokenExpiresAt) return;
        const expires = Date.parse(tokenExpiresAt);
        const now = Date.now();
        const threshold = 5 * 60 * 1000; // 5 minutes
        if (isNaN(expires)) return;
        if (expires - now < threshold) {
          // attempt refresh
          try {
            const resp = await authService.refreshToken();
            if (resp && (resp as any).access_token) {
              localStorage.setItem('auth_token', (resp as any).access_token);
            }
            const identity = await authService.getCurrentIdentity();
            const newExpires = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
            // update store
            useAuthStore.getState().setAuthenticated(identity, newExpires);
          } catch (err) {
            console.warn('Token refresh failed', err);
            useAuthStore.getState().setExpired();
          }
        }
      } catch (e) {
        // swallow errors
      }
    };

    const id = setInterval(() => {
      if (!mounted) return;
      void checkAndRefresh();
    }, refreshInterval);

    // initial check
    void checkAndRefresh();

    return () => {
      mounted = false;
      clearInterval(id);
    };
  }, []);

  return (
    <ErrorBoundary>
      <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
        <AppRouter />
        <ToastContainer />
      </div>
    </ErrorBoundary>
  );
};
