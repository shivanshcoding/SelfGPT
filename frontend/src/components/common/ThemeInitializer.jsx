"use client";

import { useEffect } from "react";
import useThemeStore from "@/stores/themeStore";

/**
 * ThemeInitializer — runs on mount to apply persisted theme.
 * Renders nothing visible.
 */
export function ThemeInitializer() {
  const initTheme = useThemeStore((s) => s.initTheme);

  useEffect(() => {
    initTheme();
  }, [initTheme]);

  return null;
}
