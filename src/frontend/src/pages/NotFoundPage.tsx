/**
 * Not Found Page (404)
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/shared/Button';
import { ROUTES } from '../constants';
import styles from './NotFoundPage.module.css';

export const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.page}>
      <div className={styles.container}>
        <h1 className={styles.code}>404</h1>
        <h2 className={styles.title}>Page Not Found</h2>
        <p className={styles.message}>
          The page you are looking for does not exist or has been
          moved.
        </p>
        <Button
          variant="primary"
          onClick={() => navigate(ROUTES.WORKSPACE)}
          size="lg"
        >
          Go to Workspace
        </Button>
      </div>
    </div>
  );
};

