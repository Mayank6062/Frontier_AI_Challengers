/**
 * useWorkspace Hook
 * Provides access to workspace state and actions
 */

import { useCallback } from 'react';
import { useWorkspaceStore, type WorkspaceTab } from '../stores';

export const useWorkspace = () => {
  const activeTab = useWorkspaceStore((state) => state.activeTab);
  const sections = useWorkspaceStore((state) => state.sections);
  const panelWidth = useWorkspaceStore((state) => state.panelWidth);
  const isCollapsed = useWorkspaceStore((state) => state.isCollapsed);

  const setActiveTab = useCallback((tab: WorkspaceTab) => {
    useWorkspaceStore.getState().setActiveTab(tab);
  }, []);

  const updateSection = useCallback((tab: WorkspaceTab, content: unknown, status: any) => {
    useWorkspaceStore.getState().updateSection(tab, content, status);
  }, []);

  const setLoading = useCallback((tab: WorkspaceTab) => {
    useWorkspaceStore.getState().setLoading(tab);
  }, []);

  const setError = useCallback((tab: WorkspaceTab) => {
    useWorkspaceStore.getState().setError(tab);
  }, []);

  const markSectionReviewed = useCallback((tab: WorkspaceTab) => {
    useWorkspaceStore.getState().markSectionReviewed(tab);
  }, []);

  const setPanelWidth = useCallback((width: number) => {
    useWorkspaceStore.getState().setPanelWidth(width);
  }, []);

  const setCollapsed = useCallback((isCollapsed: boolean) => {
    useWorkspaceStore.getState().setCollapsed(isCollapsed);
  }, []);

  const resetWorkspace = useCallback(() => {
    useWorkspaceStore.getState().resetWorkspace();
  }, []);

  const activeSectionState = sections[activeTab];

  return {
    activeTab,
    sections,
    activeSectionState,
    panelWidth,
    isCollapsed,
    setActiveTab,
    updateSection,
    setLoading,
    setError,
    markSectionReviewed,
    setPanelWidth,
    setCollapsed,
    resetWorkspace,
  };
};
