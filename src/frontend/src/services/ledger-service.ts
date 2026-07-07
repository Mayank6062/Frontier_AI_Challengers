/**
 * Ledger Service
 * Handles decision ledger queries (read-only)
 */

import { ApiClient } from './api-client';

export interface LedgerEntry {
  id: string;
  session_id: string;
  decision_id: string;
  timestamp: string;
  decision_type: string;
  decision_content: Record<string, unknown>;
  rationale?: string;
  metadata?: Record<string, unknown>;
}

export interface LedgerFilter {
  sessionId?: string;
  decisionType?: string;
  startDate?: string;
  endDate?: string;
  limit?: number;
  offset?: number;
}

export class LedgerService {
  constructor(private client: ApiClient) {}

  async listLedgerEntries(filter: LedgerFilter): Promise<LedgerEntry[]> {
    const response = await this.client.get<LedgerEntry[]>(
      '/ledger/entries',
      filter as Record<string, unknown>
    );
    return response.data;
  }

  async getLedgerEntry(entryId: string): Promise<LedgerEntry> {
    const response = await this.client.get<LedgerEntry>(
      `/ledger/entries/${entryId}`
    );
    return response.data;
  }

  async getSessionLedger(sessionId: string): Promise<LedgerEntry[]> {
    const response = await this.client.get<LedgerEntry[]>(
      `/sessions/${sessionId}/ledger`
    );
    return response.data;
  }

  async exportLedger(sessionId: string, format: 'json' | 'csv'): Promise<Blob> {
    const response = await this.client.get<Blob>(
      `/sessions/${sessionId}/ledger/export?format=${format}`
    );
    return response.data;
  }
}
