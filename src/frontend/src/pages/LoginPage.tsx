/**
 * Login Page
 * OAuth login flow with GitHub
 */

import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks';
import { LoginForm } from '../components/auth';
import { ROUTES } from '../constants';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      navigate(ROUTES.WORKSPACE, { replace: true });
    }
  }, [isAuthenticated, navigate]);

  return <LoginForm />;
};
