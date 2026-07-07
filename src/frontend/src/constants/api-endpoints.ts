/**
 * API endpoint constants
 */

export const API_ENDPOINTS = {
  // Auth
  AUTH_GITHUB_URL: '/auth/github/url',
  AUTH_GITHUB_CALLBACK: '/auth/github/callback',
  AUTH_TOKEN: '/auth/token',
  AUTH_REFRESH: '/auth/refresh',
  AUTH_LOGOUT: '/auth/logout',
  AUTH_ME: '/auth/me',

  // Sessions
  SESSIONS_LIST: '/sessions',
  SESSIONS_CREATE: '/sessions',
  SESSIONS_GET: (sessionId: string) => `/sessions/${sessionId}`,
  SESSIONS_UPDATE: (sessionId: string) => `/sessions/${sessionId}`,
  SESSIONS_DELETE: (sessionId: string) => `/sessions/${sessionId}`,
  SESSIONS_ACTIVITY: (sessionId: string) => `/sessions/${sessionId}/activity`,

  // Chat
  CHAT_SUBMIT: (sessionId: string) => `/sessions/${sessionId}/chat/message`,
  CHAT_HISTORY: (sessionId: string) => `/sessions/${sessionId}/chat/history`,
  CHAT_MESSAGE: (sessionId: string, messageId: string) => `/sessions/${sessionId}/chat/message/${messageId}`,

  // Engagement
  ENGAGEMENT_STATE: (sessionId: string) => `/sessions/${sessionId}/engagement/state`,
  ENGAGEMENT_PIPELINE: (sessionId: string) => `/sessions/${sessionId}/engagement/pipeline`,
  ENGAGEMENT_DECISION: (sessionId: string) => `/sessions/${sessionId}/engagement/review/decision`,
  ENGAGEMENT_OVERRIDE: (sessionId: string) => `/sessions/${sessionId}/engagement/review/override`,
  ENGAGEMENT_VERSIONS: (sessionId: string) => `/sessions/${sessionId}/engagement/versions`,
  ENGAGEMENT_RETRY_STAGE: (sessionId: string, stageId: string) =>
    `/sessions/${sessionId}/engagement/stages/${stageId}/retry`,

  // Outputs
  OUTPUTS_MANIFEST: (sessionId: string) => `/sessions/${sessionId}/outputs/manifest`,
  OUTPUTS_FILE: (sessionId: string, artifactId: string) => `/sessions/${sessionId}/outputs/${artifactId}`,
  OUTPUTS_DOWNLOAD: (sessionId: string, artifactId: string, format: string) =>
    `/sessions/${sessionId}/outputs/${artifactId}/download?format=${format}`,
  OUTPUTS_REGENERATE: (sessionId: string) => `/sessions/${sessionId}/outputs/regenerate`,
  OUTPUTS_PROGRESS: (sessionId: string) => `/sessions/${sessionId}/outputs/progress`,

  // Knowledge
  KNOWLEDGE_CITATIONS: (citationId: string) => `/knowledge/citations/${citationId}`,
  KNOWLEDGE_SEARCH: '/knowledge/search',
  KNOWLEDGE_ENTRIES: (entryId: string) => `/knowledge/entries/${entryId}`,
  KNOWLEDGE_DOMAINS: '/knowledge/domains',
  KNOWLEDGE_CATEGORIES: (domain: string) => `/knowledge/domains/${domain}/categories`,

  // Ledger
  LEDGER_ENTRIES: '/ledger/entries',
  LEDGER_ENTRY: (entryId: string) => `/ledger/entries/${entryId}`,
  LEDGER_SESSION: (sessionId: string) => `/sessions/${sessionId}/ledger`,
  LEDGER_EXPORT: (sessionId: string, format: string) => `/sessions/${sessionId}/ledger/export?format=${format}`,

  // Streaming
  STREAM_WEBSOCKET: (sessionId: string) => `/sessions/${sessionId}/stream`,
  STREAM_EVENTS: (sessionId: string) => `/sessions/${sessionId}/stream/events`,
} as const;
