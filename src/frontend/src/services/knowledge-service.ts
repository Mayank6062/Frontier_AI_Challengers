/**
 * Knowledge Service
 * Handles knowledge base and citation queries (read-only)
 */

import { ApiClient } from './api-client';

export interface Citation {
  id: string;
  title: string;
  source: string;
  url?: string;
  content: string;
  relevance_score: number;
}

export interface KnowledgeEntry {
  id: string;
  domain: string;
  category: string;
  title: string;
  content: string;
  metadata?: Record<string, unknown>;
}

export interface KnowledgeSearch {
  query: string;
  domain?: string;
  limit?: number;
}

export class KnowledgeService {
  constructor(private client: ApiClient) {}

  async getCitationDetails(citationId: string): Promise<Citation> {
    const response = await this.client.get<Citation>(
      `/knowledge/citations/${citationId}`
    );
    return response.data;
  }

  async searchKnowledgeBase(search: KnowledgeSearch): Promise<KnowledgeEntry[]> {
    const response = await this.client.get<KnowledgeEntry[]>(
      '/knowledge/search',
      search as unknown as Record<string, unknown>
    );
    return response.data;
  }

  async getKnowledgeEntry(entryId: string): Promise<KnowledgeEntry> {
    const response = await this.client.get<KnowledgeEntry>(
      `/knowledge/entries/${entryId}`
    );
    return response.data;
  }

  async listDomains(): Promise<string[]> {
    const response = await this.client.get<string[]>('/knowledge/domains');
    return response.data;
  }

  async listCategories(domain: string): Promise<string[]> {
    const response = await this.client.get<string[]>(
      `/knowledge/domains/${domain}/categories`
    );
    return response.data;
  }
}
