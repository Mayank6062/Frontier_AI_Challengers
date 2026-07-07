/**
 * App Router
 * Main router component with all route definitions
 */

import React, { Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ROUTES } from '../constants';
import { ProtectedRoute } from './ProtectedRoute';

// Lazy load pages
const LoginPage = React.lazy(() => import('../pages/LoginPage').then((m) => ({ default: m.LoginPage })));
const WorkspacePage = React.lazy(() =>
  import('../pages/WorkspacePage').then((m) => ({ default: m.WorkspacePage }))
);
const HistoryPage = React.lazy(() =>
  import('../pages/HistoryPage').then((m) => ({ default: m.HistoryPage }))
);
const NotFoundPage = React.lazy(() =>
  import('../pages/NotFoundPage').then((m) => ({ default: m.NotFoundPage }))
);

const LoadingFallback = () => (
  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
    <p>Loading...</p>
  </div>
);

export const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingFallback />}>
        <Routes>
          {/* Auth routes */}
          <Route path={ROUTES.LOGIN} element={<LoginPage />} />

          {/* Main routes */}
          <Route
            path={ROUTES.HOME}
            element={
              <ProtectedRoute>
                <Navigate to={ROUTES.WORKSPACE} replace />
              </ProtectedRoute>
            }
          />
          <Route
            path={ROUTES.WORKSPACE}
            element={
              <ProtectedRoute>
                <WorkspacePage />
              </ProtectedRoute>
            }
          />
          <Route
            path={ROUTES.WORKSPACE_DETAIL}
            element={
              <ProtectedRoute>
                <WorkspacePage />
              </ProtectedRoute>
            }
          />
          <Route
            path={ROUTES.HISTORY}
            element={
              <ProtectedRoute>
                <HistoryPage />
              </ProtectedRoute>
            }
          />

          {/* Error routes */}
          <Route path={ROUTES.NOT_FOUND} element={<NotFoundPage />} />
          <Route path="*" element={<Navigate to={ROUTES.NOT_FOUND} replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
};
