import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { authService } from '../../services';
import { Button } from '../shared/Button';
import { Card } from '../shared/Card';
import styles from './LoginForm.module.css';

/**
 * GitHub OAuth login form component
 * Handles OAuth flow initiation and callback processing
 */
export const LoginForm: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { setAuthenticated } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Process OAuth callback
  useEffect(() => {
    const processCallback = async () => {
      const code = searchParams.get('code');
      if (!code) return;

      setIsLoading(true);
      setError(null);

      try {
        const tokenResponse = await authService.handleOAuthCallback(code);
        // Fetch identity after successful token exchange
        const identity = await authService.getCurrentIdentity();
        // Persist access token for ApiClient
        try {
          if (tokenResponse && (tokenResponse as any).access_token) {
            localStorage.setItem('auth_token', (tokenResponse as any).access_token);
          }
        } catch (e) {
          // ignore localStorage errors
        }
        // Set expiration to 24 hours from now (can be customized based on backend response)
        const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
        setAuthenticated(identity, expiresAt);
        navigate('/workspace', { replace: true });
      } catch (err) {
        const message =
          err instanceof Error ? err.message : 'OAuth callback failed';
        setError(message);
        setIsLoading(false);
      }
    };

    processCallback();
  }, [searchParams, setAuthenticated, navigate]);

  // Initiate OAuth flow
  const handleGitHubLogin = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const oauthResponse = await authService.getOAuthUrl();
      window.location.href = oauthResponse.url;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Login failed';
      setError(message);
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Card className={styles.card}>
        <div className={styles.content}>
          <h1 className={styles.title}>ArchitectIQ</h1>
          <p className={styles.subtitle}>
            AI-Powered Architecture Design Platform
          </p>

          {error && <div className={styles.error}>{error}</div>}

          <Button
            onClick={handleGitHubLogin}
            disabled={isLoading}
            variant="primary"
            size="lg"
            className={styles.button}
          >
            {isLoading ? 'Connecting...' : 'Sign in with GitHub'}
          </Button>

          <p className={styles.disclaimer}>
            By signing in, you agree to our Terms of Service and Privacy
            Policy
          </p>
        </div>
      </Card>
    </div>
  );
};

export default LoginForm;
