/**
 * useEngagement Hook
 * Provides access to engagement state and actions
 */

import { useCallback } from 'react';
import { useEngagementStore } from '../stores';
import { Engagement, PipelineStatus, PipelineStage } from '../types';

export const useEngagement = () => {
  const engagement = useEngagementStore((state) => state.engagement);
  const pipelineStatus = useEngagementStore((state) => state.pipelineStatus);
  const isAwaitingReview = useEngagementStore((state) => state.isAwaitingReview);
  const isCompleted = useEngagementStore((state) => state.isCompleted);
  const isFailed = useEngagementStore((state) => state.isFailed);
  const error = useEngagementStore((state) => state.error);

  const setEngagement = useCallback((engagement: Engagement) => {
    useEngagementStore.getState().setEngagement(engagement);
  }, []);

  const updatePipelineStatus = useCallback((status: PipelineStatus) => {
    useEngagementStore.getState().updatePipelineStatus(status);
  }, []);

  const updatePipelineStage = useCallback((stageId: string, stage: Partial<PipelineStage>) => {
    useEngagementStore.getState().updatePipelineStage(stageId, stage);
  }, []);

  const setAwaitingReview = useCallback((awaiting: boolean) => {
    useEngagementStore.getState().setAwaitingReview(awaiting);
  }, []);

  const setCompleted = useCallback((completed: boolean) => {
    useEngagementStore.getState().setCompleted(completed);
  }, []);

  const setFailed = useCallback((failed: boolean, error?: string) => {
    useEngagementStore.getState().setFailed(failed, error);
  }, []);

  const clearEngagement = useCallback(() => {
    useEngagementStore.getState().clearEngagement();
  }, []);

  return {
    engagement,
    pipelineStatus,
    isAwaitingReview,
    isCompleted,
    isFailed,
    error,
    setEngagement,
    updatePipelineStatus,
    updatePipelineStage,
    setAwaitingReview,
    setCompleted,
    setFailed,
    clearEngagement,
  };
};
