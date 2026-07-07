/**
 * Route constants
 */

export const ROUTES = {
  // Auth routes
  LOGIN: '/login',
  LOGIN_CALLBACK: '/login/callback',
  LOGOUT: '/logout',

  // Main routes
  WORKSPACE: '/workspace',
  WORKSPACE_DETAIL: '/workspace/:sessionId',

  // Secondary routes
  HISTORY: '/history',
  SETTINGS: '/settings',
  HELP: '/help',

  // Error routes
  NOT_FOUND: '/404',
  ERROR: '/error',

  // Redirect target
  HOME: '/',
} as const;

export const getRouteParams = {
  workspaceDetail: (sessionId: string) => `/workspace/${sessionId}`,
} as const;
