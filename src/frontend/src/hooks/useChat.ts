/**
 * useChat Hook
 * Provides access to chat state and actions
 */

import { useCallback } from 'react';
import { useChatStore } from '../stores';
import { ChatMessage } from '../types';

export const useChat = () => {
  const messages = useChatStore((state) => state.messages);
  const streamingMessage = useChatStore((state) => state.streamingMessage);
  const inputText = useChatStore((state) => state.inputText);
  const attachments = useChatStore((state) => state.attachments);
  const isSubmitting = useChatStore((state) => state.isSubmitting);
  const scrollPosition = useChatStore((state) => state.scrollPosition);

  const addMessage = useCallback((message: ChatMessage) => {
    useChatStore.getState().addMessage(message);
  }, []);

  const addMessages = useCallback((messages: ChatMessage[]) => {
    useChatStore.getState().addMessages(messages);
  }, []);

  const startStreaming = useCallback((messageId: string) => {
    useChatStore.getState().startStreaming(messageId);
  }, []);

  const appendStreamChunk = useCallback((chunk: string) => {
    useChatStore.getState().appendStreamChunk(chunk);
  }, []);

  const finalizeStreaming = useCallback(() => {
    useChatStore.getState().finalizeStreaming();
  }, []);

  const setInputText = useCallback((text: string) => {
    useChatStore.getState().setInputText(text);
  }, []);

  const addAttachment = useCallback((file: File) => {
    useChatStore.getState().addAttachment(file);
  }, []);

  const removeAttachment = useCallback((fileId: string) => {
    useChatStore.getState().removeAttachment(fileId);
  }, []);

  const clearInput = useCallback(() => {
    useChatStore.getState().clearInput();
  }, []);

  const setIsSubmitting = useCallback((isSubmitting: boolean) => {
    useChatStore.getState().setIsSubmitting(isSubmitting);
  }, []);

  const setScrollPosition = useCallback((position: 'bottom' | 'scrolled-up') => {
    useChatStore.getState().setScrollPosition(position);
  }, []);

  const resetChat = useCallback(() => {
    useChatStore.getState().resetChat();
  }, []);

  return {
    messages,
    streamingMessage,
    inputText,
    attachments,
    isSubmitting,
    scrollPosition,
    addMessage,
    addMessages,
    startStreaming,
    appendStreamChunk,
    finalizeStreaming,
    setInputText,
    addAttachment,
    removeAttachment,
    clearInput,
    setIsSubmitting,
    setScrollPosition,
    resetChat,
  };
};
