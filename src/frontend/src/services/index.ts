export { ApiClient, FrontendError, ValidationError, AuthError, NotFoundError, RateLimitError, ServiceError } from './api-client';
export { AuthService } from './auth-service';
export { SessionService } from './session-service';
export { ChatService } from './chat-service';
export { EngagementService, type EngagementDecision, type EngagementOverride } from './engagement-service';
export { OutputService, type OutputManifest, type OutputArtifact, type OutputFile } from './output-service';
export { KnowledgeService, type Citation, type KnowledgeEntry, type KnowledgeSearch } from './knowledge-service';
export { LedgerService, type LedgerEntry, type LedgerFilter } from './ledger-service';
export { StreamingService, type StreamingEvent, type StreamEventHandler } from './streaming-service';

// Singleton instances for convenience
import { ApiClient } from './api-client';
import { AuthService } from './auth-service';
import { SessionService } from './session-service';
import { ChatService } from './chat-service';
import { EngagementService } from './engagement-service';
import { OutputService } from './output-service';
import { KnowledgeService } from './knowledge-service';
import { LedgerService } from './ledger-service';
import { StreamingService } from './streaming-service';
import { useAuthStore } from '../stores';

// Get API base URL from environment or use default
const API_BASE_URL = (import.meta as any).env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

// Get token function from auth store
const getToken = () => {
  const token = localStorage.getItem('auth_token');
  return token;
};

// Create singleton API client
const apiClient = new ApiClient(API_BASE_URL, getToken);

// Export service singletons
export const authService = new AuthService(apiClient);
export const sessionService = new SessionService(apiClient);
export const chatService = new ChatService(apiClient);
export const engagementService = new EngagementService(apiClient);
export const outputService = new OutputService(apiClient);
export const knowledgeService = new KnowledgeService(apiClient);
export const ledgerService = new LedgerService(apiClient);
export const streamingService = new StreamingService(API_BASE_URL, getToken);



