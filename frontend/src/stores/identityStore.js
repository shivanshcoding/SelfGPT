"use client";

import { create } from "zustand";

/**
 * Identity store — manages available identities and selected identity.
 */
const useIdentityStore = create((set) => ({
  identities: [],
  selectedIdentity: null,
  customIdentity: null,

  setIdentities: (identities) => set({ identities }),

  setSelectedIdentity: (identity) => set({ selectedIdentity: identity }),

  setCustomIdentity: (identity) => set({ customIdentity: identity }),

  updateCustomIdentity: (updates) =>
    set((state) => ({
      customIdentity: state.customIdentity
        ? { ...state.customIdentity, ...updates }
        : null,
    })),
}));

export default useIdentityStore;
