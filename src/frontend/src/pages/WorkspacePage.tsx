/**
 * Workspace Page
 * Main workspace with chat, engagement pipeline, and outputs
 */

import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useSession, useChat, useWorkspace, useEngagement, useAuth } from '../hooks';
import { useSessionStore } from '../stores';
import { useChatStore } from '../stores/chat.store';
import { SessionSidebar } from '../components/sessions';
import { ChatPanel } from '../components/chat';
import { WorkspacePanel } from '../components/workspace';
import { ThreePanelLayout } from '../components/layouts';
import { sessionService } from '../services';

export const WorkspacePage: React.FC = () => {
  const { sessionId } = useParams<{ sessionId?: string }>();
  const { identity } = useAuth();
  const {
    sessions,
    activeSessionId,
    isLoading,
    error,
  } = useSession();
  const { engagement } = useEngagement();
  
  const currentSessionId = sessionId || activeSessionId || undefined;
  
  console.log('WorkspacePage: sessionId from URL:', sessionId, 'activeSessionId from store:', activeSessionId, 'final currentSessionId:', currentSessionId);

  // Load sessions on mount
  useEffect(() => {
    const loadSessions = async () => {
      try {
        useSessionStore.getState().setLoading(true);
        const response = await sessionService.listSessions();
        const sessions = response.sessions || [];
        useSessionStore.getState().setSessions(sessions);
        
        // Set the first session as active
        if (sessions.length > 0) {
          useSessionStore.getState().setActiveSession(sessions[0].id);
        }
        
        useSessionStore.getState().setError(null);
        useSessionStore.getState().setLoading(false);
      } catch (err) {
        console.error('Failed to load sessions:', err);
        useSessionStore.getState().setError(err instanceof Error ? err.message : 'Failed to load sessions');
        useSessionStore.getState().setLoading(false);
      }
    };

    loadSessions();
  }, []);

  // Load messages when session changes
  useEffect(() => {
    const loadMessagesForSession = async () => {
      if (!currentSessionId) return;
      
      try {
        // Clear existing messages
        useChatStore.getState().resetChat();
        
        // Try to load message history
        try {
          const messages = await sessionService.loadMessageHistory(currentSessionId);
          if (messages && messages.length > 0) {
            useChatStore.getState().addMessages(messages);
          }
        } catch (err) {
          // Message history endpoint may not be implemented yet
          console.debug('Could not load message history:', err);
        }
      } catch (err) {
        console.error('Failed to load messages:', err);
      }
    };

    loadMessagesForSession();
  }, [currentSessionId]);

  const handleSessionSelect = async (id: string) => {
    try {
      // Clear chat history for old session
      useChatStore.getState().resetChat();
      
      // Set the active session
      useSessionStore.getState().setActiveSession(id);
      
      // Load messages for this session
      try {
        const messages = await sessionService.loadMessageHistory(id);
        useChatStore.getState().addMessages(messages || []);
      } catch (err) {
        // Message history endpoint may not be implemented yet
        console.debug('Could not load message history:', err);
      }
    } catch (err) {
      console.error('Failed to select session:', err);
    }
  };

  const handleSessionCreate = async () => {
    try {
      const request = {
        user_id: identity?.id || 'unknown',
        name: `Session ${new Date().toLocaleString()}`,
      };
      const newSession = await sessionService.createSession(request);
      // Update store with new session
      useSessionStore.getState().addSession({
        ...newSession,
        name: request.name,
        status: 'active' as const,
      });
      // Clear chat for the new session
      useChatStore.getState().resetChat();
      // Automatically select the new session
      useSessionStore.getState().setActiveSession(newSession.id);
    } catch (err) {
      console.error('Failed to create session:', err);
    }
  };

  const handleSessionRename = async (id: string) => {
    const newName = prompt('New session name:');
    if (newName) {
      try {
        await sessionService.updateSession(id, { name: newName });
      } catch (err) {
        console.error('Failed to rename session:', err);
      }
    }
  };

  const handleSessionDelete = async (id: string) => {
    if (
      confirm(
        'Are you sure you want to delete this session?'
      )
    ) {
      try {
        await sessionService.deleteSession(id);
      } catch (err) {
        console.error('Failed to delete session:', err);
      }
    }
  };

  const handleSearch = (query: string) => {
    // Filter sessions based on search query
    // This will be handled by the store
  };

  return (
    <ThreePanelLayout
      leftPanel={
        <SessionSidebar
          sessions={sessions}
          activeSessionId={currentSessionId}
          onSessionSelect={handleSessionSelect}
          onSessionCreate={handleSessionCreate}
          onSessionRename={handleSessionRename}
          onSessionDelete={handleSessionDelete}
          onSearch={handleSearch}
          isLoading={isLoading}
        />
      }
      centerPanel={
        <ChatPanel sessionId={currentSessionId} />
      }
      rightPanel={
        <WorkspacePanel />
      }
      leftWidth={20}
      rightWidth={30}
    />
  );
};

