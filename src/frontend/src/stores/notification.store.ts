/**
 * Notification Store
 * Manages toast notifications and notification history
 */

import { create } from 'zustand';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface Toast {
  id: string;
  type: NotificationType;
  message: string;
  duration?: number;
}

export interface NotificationRecord {
  id: string;
  type: NotificationType;
  message: string;
  timestamp: string;
  read: boolean;
}

interface NotificationStore {
  toasts: Toast[];
  history: NotificationRecord[];
  unreadCount: number;

  // Actions
  showToast: (notification: Omit<Toast, 'id'>) => void;
  dismissToast: (id: string) => void;
  addToHistory: (record: Omit<NotificationRecord, 'id' | 'timestamp'>) => void;
  markAsRead: (id: string) => void;
  markAllRead: () => void;
  clearHistory: () => void;
  clearToasts: () => void;
}

export const useNotificationStore = create<NotificationStore>((set) => ({
  toasts: [],
  history: [],
  unreadCount: 0,

  showToast: (notification) =>
    set((state) => ({
      toasts: [
        ...state.toasts,
        {
          ...notification,
          id: `${Date.now()}-${Math.random()}`,
        },
      ],
    })),

  dismissToast: (id) =>
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    })),

  addToHistory: (notification) =>
    set((state) => ({
      history: [
        {
          ...notification,
          id: `${Date.now()}-${Math.random()}`,
          timestamp: new Date().toISOString(),
        },
        ...state.history,
      ],
      unreadCount: state.unreadCount + 1,
    })),

  markAsRead: (id) =>
    set((state) => ({
      history: state.history.map((r) =>
        r.id === id ? { ...r, read: true } : r
      ),
      unreadCount: Math.max(0, state.unreadCount - 1),
    })),

  markAllRead: () =>
    set((state) => ({
      history: state.history.map((r) => ({ ...r, read: true })),
      unreadCount: 0,
    })),

  clearHistory: () =>
    set({
      history: [],
      unreadCount: 0,
    }),

  clearToasts: () =>
    set({
      toasts: [],
    }),
}));
