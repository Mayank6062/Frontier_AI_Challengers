/**
 * Engagement Service
 * Handles engagement state and pipeline management API calls
 */

import { ApiClient } from './api-client';
import { Engagement, PipelineStatus, PipelineStage } from '../types';

export interface EngagementDecision {
  stage_id: string;
  decision: 'approved' | 'rejected' | 'needs_revision';
  feedback?: string;
}

export interface EngagementOverride {
  stage_id: string;
  override_reason: string;
  overridden_decision: 'approved' | 'rejected';
}

export class EngagementService {
  constructor(private client: ApiClient) {}

  async getEngagementState(sessionId: string): Promise<Engagement> {
    const response = await this.client.get<Engagement>(
      `/sessions/${sessionId}/engagement/state`
    );
    return response.data;
  }

  async getPipelineStatus(sessionId: string): Promise<PipelineStatus> {
    const response = await this.client.get<PipelineStatus>(
      `/sessions/${sessionId}/engagement/pipeline`
    );
    return response.data;
  }

  async submitReviewDecision(
    sessionId: string,
    decision: EngagementDecision
  ): Promise<Engagement> {
    const response = await this.client.post<Engagement>(
      `/sessions/${sessionId}/engagement/review/decision`,
      decision
    );
    return response.data;
  }

  async submitOverride(sessionId: string, override: EngagementOverride): Promise<Engagement> {
    const response = await this.client.post<Engagement>(
      `/sessions/${sessionId}/engagement/review/override`,
      override
    );
    return response.data;
  }

  async getVersionHistory(sessionId: string): Promise<PipelineStage[]> {
    const response = await this.client.get<PipelineStage[]>(
      `/sessions/${sessionId}/engagement/versions`
    );
    return response.data;
  }

  async retryStage(sessionId: string, stageId: string): Promise<PipelineStatus> {
    const response = await this.client.post<PipelineStatus>(
      `/sessions/${sessionId}/engagement/stages/${stageId}/retry`,
      {}
    );
    return response.data;
  }
}
