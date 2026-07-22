"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

/**
 * Theme store — manages light/dark/system theme preference.
 * Persisted to localStorage so it survives page refreshes.
 */
const useThemeStore = create(
  persist(
    (set, get) => ({
      theme: "system", // "light" | "dark" | "system"

      setTheme: (theme) => {
        set({ theme });
        applyTheme(theme);
      },

      initTheme: () => {
        applyTheme(get().theme);
      },
    }),
    {
      name: "selfgpt-theme",
    }
  )
);

function applyTheme(theme) {
  if (typeof window === "undefined") return;

  const root = document.documentElement;
  root.removeAttribute("data-theme");

  if (theme === "dark") {
    root.setAttribute("data-theme", "dark");
  } else if (theme === "light") {
    root.setAttribute("data-theme", "light");
  }
  // "system" → let CSS @media handle it (no data-theme attribute)
}

export default useThemeStore;
