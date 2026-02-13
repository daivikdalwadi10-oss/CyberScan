import { useEffect, useMemo, useState } from "react";
import GlassCard from "../ui/GlassCard.jsx";
import StatusBadge from "../ui/StatusBadge.jsx";
import { acknowledgeAlert, escalateAlert, getAlerts, resolveAlert } from "../../services/api.js";
import { useWebSocket } from "../../hooks/useWebSocket.js";

const mapStatus = (status) => {
  if (!status) return "info";
  const key = status.toLowerCase();
  if (key === "new" || key === "in_progress") return "warning";
  if (key === "acknowledged") return "info";
  if (key === "resolved") return "operational";
  return "critical";
};

export default function AlertsFeed() {
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const { messages, status, send } = useWebSocket();

  useEffect(() => {
    let isMounted = true;
    getAlerts({ limit: 8 })
      .then((data) => {
        if (isMounted) setAlerts(data || []);
      })
      .catch((err) => {
        if (isMounted) setError(err?.message || "Unable to load alerts");
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });
    return () => {
      isMounted = false;
    };
  }, []);

  const liveAlerts = useMemo(() => {
    const incoming = messages.filter((msg) => msg.type === "alert" || msg.type === "alert_update");
    if (incoming.length === 0) return alerts;
    const merged = [...incoming.map((msg) => msg.payload || msg), ...alerts];
    return merged.slice(0, 10);
  }, [alerts, messages]);

  const handleAcknowledge = (alertId) => {
    if (!alertId) return;
    setAlerts((prev) =>
      prev.map((alert) => (alert.id === alertId ? { ...alert, status: "ACKNOWLEDGED" } : alert))
    );
    send({ type: "ack", alert_id: alertId });
    acknowledgeAlert(alertId).catch(() => {});
  };

  const handleEscalate = (alertId) => {
    if (!alertId) return;
    setAlerts((prev) =>
      prev.map((alert) => (alert.id === alertId ? { ...alert, status: "IN_PROGRESS" } : alert))
    );
    escalateAlert(alertId).catch(() => {});
  };

  const handleResolve = (alertId) => {
    if (!alertId) return;
    setAlerts((prev) =>
      prev.map((alert) => (alert.id === alertId ? { ...alert, status: "RESOLVED" } : alert))
    );
    resolveAlert(alertId).catch(() => {});
  };

  return (
    <GlassCard className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold">Real-time Alerts</p>
          <p className="text-xs text-[var(--color-text-muted)]">WebSocket: {status}</p>
        </div>
        <StatusBadge status={status === "connected" ? "operational" : "warning"} label={status} />
      </div>
      {error ? <p className="text-sm text-red-200">{error}</p> : null}
      <div className="space-y-3">
        {loading ? (
          <div className="h-16 w-full rounded-2xl skeleton" />
        ) : liveAlerts.length === 0 ? (
          <p className="text-sm text-[var(--color-text-muted)]">No active alerts.</p>
        ) : (
          liveAlerts.map((alert) => (
            <div key={alert.id || alert.alert_id} className="flex flex-col gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm">{alert.title || alert.summary || "Alert"}</p>
                  <p className="text-xs text-[var(--color-text-muted)]">{alert.source || "Alert Engine"}</p>
                </div>
                <StatusBadge status={mapStatus(alert.status)} label={alert.status || "new"} />
              </div>
              <div className="flex flex-wrap gap-2">
                <button
                  className="rounded-full border border-white/10 px-3 py-1 text-xs"
                  type="button"
                  onClick={() => handleAcknowledge(alert.id || alert.alert_id)}
                >
                  Acknowledge
                </button>
                <button
                  className="rounded-full border border-white/10 px-3 py-1 text-xs"
                  type="button"
                  onClick={() => handleEscalate(alert.id || alert.alert_id)}
                >
                  Escalate
                </button>
                <button
                  className="rounded-full border border-white/10 px-3 py-1 text-xs"
                  type="button"
                  onClick={() => handleResolve(alert.id || alert.alert_id)}
                >
                  Resolve
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </GlassCard>
  );
}
