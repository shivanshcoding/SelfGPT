"use client";

import { create } from "zustand";

/**
 * Chat store — manages active chat state, message list, and streaming.
 */
const useChatStore = create((set, get) => ({
  // Chat list
  chats: [],
  activeChat: null,
  activeChatId: null,

  // Messages for the active chat
  messages: [],
  isStreaming: false,
  streamingContent: "",

  // Sidebar state
  searchQuery: "",

  // Actions
  setChats: (chats) => set({ chats }),

  setActiveChat: (chat) =>
    set({
      activeChat: chat,
      activeChatId: chat?.id || null,
    }),

  setMessages: (messages) => set({ messages }),

  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  updateMessage: (messageId, updates) =>
    set((state) => ({
      messages: state.messages.map((m) =>
        m.id === messageId ? { ...m, ...updates } : m
      ),
    })),

  removeMessage: (messageId) =>
    set((state) => ({
      messages: state.messages.filter((m) => m.id !== messageId),
    })),

  // Streaming
  setStreaming: (isStreaming) => set({ isStreaming }),
  setStreamingContent: (content) => set({ streamingContent: content }),
  appendStreamingContent: (token) =>
    set((state) => ({
      streamingContent: state.streamingContent + token,
    })),

  // Search
  setSearchQuery: (query) => set({ searchQuery: query }),

  // Reset
  resetChat: () =>
    set({
      activeChat: null,
      activeChatId: null,
      messages: [],
      isStreaming: false,
      streamingContent: "",
    }),
}));

export default useChatStore;
