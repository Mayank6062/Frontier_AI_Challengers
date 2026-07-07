/**
 * Engagement & Chat Types
 * Aligned with backend schemas
 */

export interface ChatMessage {
  id: string;
  session_id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface ChatRequest {
  content: string;
  attachments?: File[];
}

export interface ChatResponse {
  message: ChatMessage;
}

export type EngagementState = 'PENDING' | 'ACTIVE' | 'PENDING_HUMAN_REVIEW' | 'COMPLETED' | 'REJECTED' | 'FAILED';

export interface Engagement {
  id: string;
  session_id: string;
  state: string;
  created_at: string;
  updated_at: string;
  version: number;
  metadata?: Record<string, unknown>;
}

export interface PipelineStage {
  id: string;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress?: number;
  output?: unknown;
  error?: string;
}

export interface PipelineStatus {
  engagement_id: string;
  current_stage: PipelineStage;
  completed_stages: PipelineStage[];
  remaining_stages: PipelineStage[];
  overall_progress: number;
}
