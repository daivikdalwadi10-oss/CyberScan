import { useEffect, useState, useRef } from "react";
import GlassCard from "../../components/ui/GlassCard.jsx";
import MetricCard from "../../components/ui/MetricCard.jsx";
import SectionHeader from "../../components/ui/SectionHeader.jsx";
import StatusBadge from "../../components/ui/StatusBadge.jsx";
import UptimeWidget from "../../components/widgets/UptimeWidget.jsx";
import CloudStatusPanel from "../../components/widgets/CloudStatusPanel.jsx";
import ThreatFeed from "../../components/widgets/ThreatFeed.jsx";
import { getPublicStatus } from "../../services/api.js";

  const [status, setStatus] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState("");
  const intervalRef = useRef(null);

  // Polling every 10s
  const fetchStatus = async () => {
    setLoading(true);
    try {
      const data = await getPublicStatus();
      setStatus(data);
      setLastUpdated(new Date().toLocaleTimeString());
      setError("");
    } catch (err) {
      setError(err?.message || "Unable to load public status");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    intervalRef.current = setInterval(fetchStatus, 10000);
    return () => {
      clearInterval(intervalRef.current);
    };
  }, []);

  return (
    <div className="space-y-10">
      <SectionHeader
        eyebrow="Transparency"
        title="Public Security Overview"
        description="Real-time status updates and transparency metrics from the security operations platform."
        action={
          <button
            className="glass-btn px-4 py-2 rounded-lg text-sm font-semibold"
            onClick={fetchStatus}
            disabled={loading}
            title="Manual refresh"
          >
            {loading ? "Refreshing..." : "Manual Refresh"}
          </button>
        }
      />
      <div className="grid gap-6 lg:grid-cols-4">
        <MetricCard label="Risk Score" value={status?.riskScore} unit="/100" accent="red" isLoading={loading} error={error} />
        <MetricCard label="Uptime" value={status?.uptime} unit="%" accent="emerald" isLoading={loading} error={error} />
        <MetricCard label="Incidents Resolved" value={status?.incidentsResolved} unit="" accent="blue" isLoading={loading} error={error} />
        <GlassCard className="flex flex-col justify-between">
          <p className="text-xs uppercase tracking-[0.3em] text-[var(--color-text-muted)]">System Status</p>
          <div className="flex items-center justify-between">
            <p className="text-2xl font-display capitalize" title={status?.systemStatus || "Unknown"}>{status?.systemStatus || "Unknown"}</p>
            <StatusBadge status={status?.systemStatus || "info"} />
          </div>
          <p className="text-xs text-[var(--color-text-muted)]">Last updated: {lastUpdated || "-"}</p>
        </GlassCard>
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <UptimeWidget />
        <CloudStatusPanel />
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <ThreatFeed />
        <GlassCard className="flex flex-col gap-4">
          <p className="text-sm font-semibold">Recent Updates</p>
          {loading ? (
            <div className="h-20 w-full rounded-2xl skeleton" />
          ) : error ? (
            <p className="text-sm text-red-200">{error}</p>
          ) : status?.recentUpdates?.length ? (
            status.recentUpdates.map((update) => (
              <div key={update.date} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 hover:bg-white/10 transition-all">
                <p className="text-sm">{update.title}</p>
                <p className="text-xs text-[var(--color-text-muted)]">{update.date}</p>
              </div>
            ))
          ) : (
            <p className="text-sm text-[var(--color-text-muted)]">No recent updates.</p>
          )}
        </GlassCard>
      </div>
    </div>
  );
}
