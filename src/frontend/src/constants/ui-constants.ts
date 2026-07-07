/**
 * UI Constants
 */

export const UI_CONSTANTS = {
  // Z-index layers
  ZINDEX: {
    BASE: 0,
    DROPDOWN: 1000,
    STICKY: 1020,
    FIXED: 1030,
    MODAL_BACKDROP: 1040,
    MODAL: 1050,
    POPOVER: 1060,
    TOOLTIP: 1070,
  },

  // Animation durations (ms)
  ANIMATION: {
    FAST: 150,
    NORMAL: 300,
    SLOW: 500,
  },

  // Breakpoints
  BREAKPOINTS: {
    XS: 0,
    SM: 640,
    MD: 768,
    LG: 1024,
    XL: 1280,
    '2XL': 1536,
  },

  // Layout
  LAYOUT: {
    SIDEBAR_WIDTH: 280,
    SIDEBAR_COLLAPSED_WIDTH: 64,
    WORKSPACE_PANEL_WIDTH: 480,
    WORKSPACE_PANEL_MIN_WIDTH: 300,
    WORKSPACE_PANEL_MAX_WIDTH: 600,
    MAIN_HEADER_HEIGHT: 64,
    TOPBAR_HEIGHT: 56,
  },

  // Pagination
  PAGINATION: {
    DEFAULT_PAGE_SIZE: 20,
    MAX_PAGE_SIZE: 100,
  },

  // Toast
  TOAST: {
    DEFAULT_DURATION: 5000,
    ERROR_DURATION: 7000,
    SUCCESS_DURATION: 3000,
    INFO_DURATION: 4000,
    WARNING_DURATION: 5000,
  },

  // Input
  INPUT: {
    DEBOUNCE_DELAY: 300,
    AUTOCOMPLETE_MIN_CHARS: 2,
    AUTOCOMPLETE_MAX_RESULTS: 10,
  },

  // Chat
  CHAT: {
    MESSAGE_BATCH_SIZE: 50,
    STREAMING_TIMEOUT: 60000, // 60s
    RECONNECT_INTERVAL: 3000,
    MAX_RECONNECT_ATTEMPTS: 5,
  },

  // File upload
  FILE_UPLOAD: {
    MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
    ALLOWED_TYPES: ['application/pdf', 'text/plain', 'application/json'],
  },
} as const;

// Responsive breakpoint queries
export const MEDIA_QUERIES = {
  SM: `(min-width: ${UI_CONSTANTS.BREAKPOINTS.SM}px)`,
  MD: `(min-width: ${UI_CONSTANTS.BREAKPOINTS.MD}px)`,
  LG: `(min-width: ${UI_CONSTANTS.BREAKPOINTS.LG}px)`,
  XL: `(min-width: ${UI_CONSTANTS.BREAKPOINTS.XL}px)`,
  '2XL': `(min-width: ${UI_CONSTANTS.BREAKPOINTS['2XL']}px)`,
} as const;
