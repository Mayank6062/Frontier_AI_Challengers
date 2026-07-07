/**
 * Chat Store
 * Manages chat messages, streaming state, input area state
 */

import { create } from 'zustand';
import { ChatMessage } from '../types';

interface StreamingMessage {
  id: string;
  content: string;
  isComplete: boolean;
}

interface ChatStore {
  messages: ChatMessage[];
  streamingMessage: StreamingMessage | null;
  inputText: string;
  attachments: File[];
  isSubmitting: boolean;
  hasMore: boolean;
  scrollPosition: 'bottom' | 'scrolled-up';

  // Actions
  addMessage: (message: ChatMessage) => void;
  addMessages: (messages: ChatMessage[]) => void;
  startStreaming: (messageId: string) => void;
  appendStreamChunk: (chunk: string) => void;
  finalizeStreaming: () => void;
  setInputText: (text: string) => void;
  addAttachment: (file: File) => void;
  removeAttachment: (fileId: string) => void;
  clearInput: () => void;
  setIsSubmitting: (isSubmitting: boolean) => void;
  setScrollPosition: (position: 'bottom' | 'scrolled-up') => void;
  resetChat: () => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  streamingMessage: null,
  inputText: '',
  attachments: [],
  isSubmitting: false,
  hasMore: false,
  scrollPosition: 'bottom',

  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  addMessages: (messages) =>
    set((state) => ({
      messages: [...state.messages, ...messages],
    })),

  startStreaming: (messageId) =>
    set({
      streamingMessage: {
        id: messageId,
        content: '',
        isComplete: false,
      },
    }),

  appendStreamChunk: (chunk) =>
    set((state) => {
      if (!state.streamingMessage) return state;
      return {
        streamingMessage: {
          ...state.streamingMessage,
          content: state.streamingMessage.content + chunk,
        },
      };
    }),

  finalizeStreaming: () =>
    set((state) => {
      if (!state.streamingMessage) return state;
      const finalMessage: ChatMessage = {
        id: state.streamingMessage.id,
        session_id: '', // Should be set by caller
        role: 'assistant',
        content: state.streamingMessage.content,
        timestamp: new Date().toISOString(),
      };
      return {
        messages: [...state.messages, finalMessage],
        streamingMessage: null,
      };
    }),

  setInputText: (text) => set({ inputText: text }),

  addAttachment: (file) =>
    set((state) => ({
      attachments: [...state.attachments, file],
    })),

  removeAttachment: (fileId) =>
    set((state) => ({
      attachments: state.attachments.filter((f) => f.name !== fileId),
    })),

  clearInput: () =>
    set({
      inputText: '',
      attachments: [],
    }),

  setIsSubmitting: (isSubmitting) => set({ isSubmitting }),

  setScrollPosition: (position) => set({ scrollPosition: position }),

  resetChat: () =>
    set({
      messages: [],
      streamingMessage: null,
      inputText: '',
      attachments: [],
      isSubmitting: false,
    }),
}));
