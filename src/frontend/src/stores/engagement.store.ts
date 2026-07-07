/**
 * Engagement Store
 * Manages active engagement state, pipeline status, lifecycle
 */

import { create } from 'zustand';
import { Engagement, PipelineStatus, PipelineStage } from '../types';

interface EngagementStore {
  engagement: Engagement | null;
  pipelineStatus: PipelineStatus | null;
  isAwaitingReview: boolean;
  isCompleted: boolean;
  isFailed: boolean;
  error: string | null;

  // Actions
  setEngagement: (engagement: Engagement) => void;
  updatePipelineStatus: (status: PipelineStatus) => void;
  updatePipelineStage: (stageId: string, stage: Partial<PipelineStage>) => void;
  setAwaitingReview: (awaiting: boolean) => void;
  setCompleted: (completed: boolean) => void;
  setFailed: (failed: boolean, error?: string) => void;
  clearEngagement: () => void;
}

export const useEngagementStore = create<EngagementStore>((set) => ({
  engagement: null,
  pipelineStatus: null,
  isAwaitingReview: false,
  isCompleted: false,
  isFailed: false,
  error: null,

  setEngagement: (engagement) =>
    set({
      engagement,
      isCompleted: engagement.state === 'COMPLETED',
      isFailed: engagement.state === 'FAILED',
    }),

  updatePipelineStatus: (status) =>
    set({
      pipelineStatus: status,
    }),

  updatePipelineStage: (stageId, stage) =>
    set((state) => {
      if (!state.pipelineStatus) return state;
      return {
        pipelineStatus: {
          ...state.pipelineStatus,
          current_stage:
            state.pipelineStatus.current_stage.id === stageId
              ? { ...state.pipelineStatus.current_stage, ...stage }
              : state.pipelineStatus.current_stage,
        },
      };
    }),

  setAwaitingReview: (awaiting) =>
    set({
      isAwaitingReview: awaiting,
    }),

  setCompleted: (completed) =>
    set({
      isCompleted: completed,
    }),

  setFailed: (failed, error) =>
    set({
      isFailed: failed,
      error: error || null,
    }),

  clearEngagement: () =>
    set({
      engagement: null,
      pipelineStatus: null,
      isAwaitingReview: false,
      isCompleted: false,
      isFailed: false,
      error: null,
    }),
}));
