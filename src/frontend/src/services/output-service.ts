/**
 * Output Service
 * Handles generated output artifact API calls
 */

import { ApiClient } from './api-client';

export interface OutputManifest {
  id: string;
  session_id: string;
  artifacts: OutputArtifact[];
  generated_at: string;
}

export interface OutputArtifact {
  id: string;
  name: string;
  type: string;
  url: string;
  size: number;
  created_at: string;
}

export interface OutputFile {
  id: string;
  name: string;
  content: string;
  mimeType: string;
}

export class OutputService {
  constructor(private client: ApiClient) {}

  async getOutputManifest(sessionId: string): Promise<OutputManifest> {
    const response = await this.client.get<OutputManifest>(
      `/sessions/${sessionId}/outputs/manifest`
    );
    return response.data;
  }

  async getOutputFile(sessionId: string, artifactId: string): Promise<OutputFile> {
    const response = await this.client.get<OutputFile>(
      `/sessions/${sessionId}/outputs/${artifactId}`
    );
    return response.data;
  }

  async downloadOutput(sessionId: string, artifactId: string, format: string): Promise<Blob> {
    // This would need custom handling in ApiClient to return Blob
    const response = await this.client.get<Blob>(
      `/sessions/${sessionId}/outputs/${artifactId}/download?format=${format}`
    );
    return response.data;
  }

  async triggerRegeneration(sessionId: string, options?: Record<string, unknown>): Promise<OutputManifest> {
    const response = await this.client.post<OutputManifest>(
      `/sessions/${sessionId}/outputs/regenerate`,
      options || {}
    );
    return response.data;
  }

  async getRegenerationProgress(sessionId: string): Promise<{
    status: 'pending' | 'in_progress' | 'completed' | 'failed';
    progress: number;
  }> {
    const response = await this.client.get<{
      status: 'pending' | 'in_progress' | 'completed' | 'failed';
      progress: number;
    }>(`/sessions/${sessionId}/outputs/progress`);
    return response.data;
  }
}
