/**
 * Route Configuration
 * Defines all application routes and their properties
 */

import { ROUTES } from '../constants';

export interface RouteConfig {
  path: string;
  name: string;
  requiresAuth: boolean;
  layout?: 'auth' | 'main';
}

export const routeConfigs: RouteConfig[] = [
  // Auth routes
  {
    path: ROUTES.LOGIN,
    name: 'Login',
    requiresAuth: false,
    layout: 'auth',
  },
  {
    path: ROUTES.LOGIN_CALLBACK,
    name: 'Login Callback',
    requiresAuth: false,
    layout: 'auth',
  },
  {
    path: ROUTES.LOGOUT,
    name: 'Logout',
    requiresAuth: true,
  },

  // Main routes
  {
    path: ROUTES.HOME,
    name: 'Home',
    requiresAuth: true,
    layout: 'main',
  },
  {
    path: ROUTES.WORKSPACE,
    name: 'Workspace',
    requiresAuth: true,
    layout: 'main',
  },
  {
    path: ROUTES.WORKSPACE_DETAIL,
    name: 'Session',
    requiresAuth: true,
    layout: 'main',
  },
  {
    path: ROUTES.HISTORY,
    name: 'History',
    requiresAuth: true,
    layout: 'main',
  },
  {
    path: ROUTES.SETTINGS,
    name: 'Settings',
    requiresAuth: true,
    layout: 'main',
  },

  // Error routes
  {
    path: ROUTES.NOT_FOUND,
    name: 'Not Found',
    requiresAuth: false,
  },
  {
    path: ROUTES.ERROR,
    name: 'Error',
    requiresAuth: false,
  },
];

export const getRouteConfig = (path: string): RouteConfig | undefined => {
  return routeConfigs.find((config) => config.path === path);
};
