import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  timeout: 15000
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;
    const message = error?.response?.data?.detail || error.message || "Request failed";
    return Promise.reject({ status, message });
  }
);

export const getPublicStatus = async () => {
  const { data } = await api.get("/api/public/status");
  return data;
};

export const getLatestCves = async () => {
  try {
    const { data } = await api.get("/api/public/latest-cves");
    return data;
  } catch (error) {
    if (error?.status === 404) {
      const fallback = await getPublicStatus();
      return fallback?.latestCriticalCves || [];
    }
    throw error;
  }
};

export const getSystemHealth = async () => {
  const { data } = await api.get("/api/internal/system-health");
  return data;
};

export const getAuditLogs = async (params) => {
  const { data } = await api.get("/api/internal/audit-logs", { params });
  return data;
};

export const getThreatIntel = async (params) => {
  const { data } = await api.get("/api/internal/threat-intel", { params });
  return data;
};

export const getIocs = async (params) => {
  const { data } = await api.get("/api/internal/iocs", { params });
  return data;
};

export const getAlerts = async (params) => {
  const { data } = await api.get("/api/internal/alerts", { params });
  return data;
};

export const acknowledgeAlert = async (alertId) => {
  const { data } = await api.post(`/api/internal/alerts/${alertId}/ack`);
  return data;
};

export const escalateAlert = async (alertId) => {
  const { data } = await api.post(`/api/internal/alerts/${alertId}/escalate`);
  return data;
};

export const resolveAlert = async (alertId) => {
  const { data } = await api.post(`/api/internal/alerts/${alertId}/resolve`);
  return data;
};

export const getIncidents = async (params) => {
  const { data } = await api.get("/api/internal/incidents", { params });
  return data;
};

export const updateIncidentStatus = async (incidentId, payload) => {
  const { data } = await api.post(`/api/internal/incidents/${incidentId}/status`, payload);
  return data;
};

export const getRiskScore = async () => {
  const { data } = await api.get("/api/internal/risk-score");
  return data;
};

export const getDashboardConfig = async () => {
  const { data } = await api.get("/api/internal/dashboard/config");
  return data;
};

export const getMetricsScrape = async () => {
  const { data } = await api.get("/metrics", { responseType: "text" });
  return data;
};

export default api;

// Role-based documentation fetcher
export const fetchRoleDocs = async (role) => {
  const { data } = await api.get(`/docs-panel/${role}`);
  return data;
};
