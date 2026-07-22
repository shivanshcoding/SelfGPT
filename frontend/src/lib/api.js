/**
 * SelfGPT — Axios API Client
 *
 * Centralized HTTP client with JWT interceptors, token refresh,
 * and error handling.
 */

import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// ── Request Interceptor — Attach JWT ──────────────────────────────
api.interceptors.request.use(
  (config) => {
    if (typeof window !== "undefined") {
      try {
        const stored = JSON.parse(localStorage.getItem("selfgpt-auth") || "{}");
        const token = stored?.state?.accessToken;
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
      } catch {
        // Invalid localStorage state — skip
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ── Response Interceptor — Handle 401 + Token Refresh ──────────────
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and not already retried, attempt token refresh
    if (
      error.response?.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        const stored = JSON.parse(localStorage.getItem("selfgpt-auth") || "{}");
        const refreshToken = stored?.state?.refreshToken;

        if (refreshToken) {
          const { data } = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {
            refresh_token: refreshToken,
          });

          // Update stored tokens
          stored.state.accessToken = data.access_token;
          stored.state.refreshToken = data.refresh_token;
          localStorage.setItem("selfgpt-auth", JSON.stringify(stored));

          // Retry original request
          originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed — clear auth and redirect to login
        localStorage.removeItem("selfgpt-auth");
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
      }
    }

    return Promise.reject(error);
  }
);

export default api;

// ── Convenience exports ───────────────────────────────────────────
export const authApi = {
  register: (data) => api.post("/api/auth/register", data),
  login: (data) => api.post("/api/auth/login", data),
  refresh: (data) => api.post("/api/auth/refresh", data),
  me: () => api.get("/api/auth/me"),
  googleAuth: (data) => api.post("/api/auth/google", data),
};

export const chatApi = {
  list: (params) => api.get("/api/chats", { params }),
  create: (data) => api.post("/api/chats", data),
  get: (id) => api.get(`/api/chats/${id}`),
  update: (id, data) => api.patch(`/api/chats/${id}`, data),
  delete: (id) => api.delete(`/api/chats/${id}`),
  restore: (id) => api.post(`/api/chats/${id}/restore`),
  permanentDelete: (id) => api.delete(`/api/chats/${id}/permanent`),
};

export const messageApi = {
  list: (chatId, params) => api.get(`/api/chats/${chatId}/messages`, { params }),
  send: (chatId, data) => api.post(`/api/chats/${chatId}/messages`, data),
  feedback: (chatId, msgId, data) =>
    api.patch(`/api/chats/${chatId}/messages/${msgId}/feedback`, data),
  edit: (chatId, msgId, data) =>
    api.patch(`/api/chats/${chatId}/messages/${msgId}/edit`, data),
  regenerate: (chatId, msgId) =>
    api.post(`/api/chats/${chatId}/messages/${msgId}/regenerate`),
};

export const identityApi = {
  list: (params) => api.get("/api/identities", { params }),
  get: (slug) => api.get(`/api/identities/${slug}`),
  createCustom: (data) => api.post("/api/identities/custom", data),
  updateCustom: (data) => api.patch("/api/identities/custom", data),
  getMyCustom: () => api.get("/api/identities/custom/mine"),
};

export const memoryApi = {
  list: (params) => api.get("/api/memories", { params }),
  update: (id, data) => api.patch(`/api/memories/${id}`, data),
  forget: (id) => api.delete(`/api/memories/${id}`),
};

export const adminApi = {
  users: (params) => api.get("/api/admin/users", { params }),
  analytics: () => api.get("/api/admin/analytics"),
  health: () => api.get("/api/admin/health"),
  trainingExport: (params) => api.get("/api/training/export", { params }),
  trainingStats: () => api.get("/api/training/stats"),
};
