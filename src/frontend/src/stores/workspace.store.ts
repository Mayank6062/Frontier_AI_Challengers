/**
 * Workspace Store
 * Manages workspace panel state, tabs, sections, content
 */

import { create } from 'zustand';

export type WorkspaceTab = 'requirements' | 'architecture' | 'validation' | 'review' | 'outputs' | 'ledger';

interface SectionState {
  status: 'empty' | 'loading' | 'partial' | 'complete' | 'error';
  content: unknown;
  lastUpdated: string | null;
  reviewedByUser: boolean;
}

interface WorkspaceStore {
  activeTab: WorkspaceTab;
  sections: Record<WorkspaceTab, SectionState>;
  panelWidth: number;
  isCollapsed: boolean;

  // Actions
  setActiveTab: (tab: WorkspaceTab) => void;
  updateSection: (tab: WorkspaceTab, content: unknown, status: SectionState['status']) => void;
  setLoading: (tab: WorkspaceTab) => void;
  setError: (tab: WorkspaceTab) => void;
  markSectionReviewed: (tab: WorkspaceTab) => void;
  setPanelWidth: (width: number) => void;
  setCollapsed: (isCollapsed: boolean) => void;
  resetWorkspace: () => void;
}

const initialSections: Record<WorkspaceTab, SectionState> = {
  requirements: { status: 'empty', content: null, lastUpdated: null, reviewedByUser: false },
  architecture: { status: 'empty', content: null, lastUpdated: null, reviewedByUser: false },
  validation: { status: 'empty', content: null, lastUpdated: null, reviewedByUser: false },
  review: { status: 'empty', content: null, lastUpdated: null, reviewedByUser: false },
  outputs: { status: 'empty', content: null, lastUpdated: null, reviewedByUser: false },
  ledger: { status: 'empty', content: null, lastUpdated: null, reviewedByUser: false },
};

export const useWorkspaceStore = create<WorkspaceStore>((set) => ({
  activeTab: 'requirements',
  sections: initialSections,
  panelWidth: 480,
  isCollapsed: false,

  setActiveTab: (tab) => set({ activeTab: tab }),

  updateSection: (tab, content, status) =>
    set((state) => ({
      sections: {
        ...state.sections,
        [tab]: {
          ...state.sections[tab],
          content,
          status,
          lastUpdated: new Date().toISOString(),
        },
      },
    })),

  setLoading: (tab) =>
    set((state) => ({
      sections: {
        ...state.sections,
        [tab]: {
          ...state.sections[tab],
          status: 'loading',
        },
      },
    })),

  setError: (tab) =>
    set((state) => ({
      sections: {
        ...state.sections,
        [tab]: {
          ...state.sections[tab],
          status: 'error',
        },
      },
    })),

  markSectionReviewed: (tab) =>
    set((state) => ({
      sections: {
        ...state.sections,
        [tab]: {
          ...state.sections[tab],
          reviewedByUser: true,
        },
      },
    })),

  setPanelWidth: (width) => set({ panelWidth: width }),

  setCollapsed: (isCollapsed) => set({ isCollapsed }),

  resetWorkspace: () =>
    set({
      activeTab: 'requirements',
      sections: initialSections,
      panelWidth: 480,
    }),
}));
