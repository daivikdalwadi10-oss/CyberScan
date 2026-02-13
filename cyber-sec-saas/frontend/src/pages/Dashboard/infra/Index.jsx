import { useCallback, useState } from "react";
import SectionHeader from "../../../components/ui/SectionHeader.jsx";
import MetricCard from "../../../components/ui/MetricCard.jsx";
import GlassCard from "../../../components/ui/GlassCard.jsx";
import LineChart from "../../../components/charts/LineChart.jsx";
import CloudStatusPanel from "../../../components/widgets/CloudStatusPanel.jsx";
import DocumentationPanel from "../DocumentationPanel.jsx";
import { usePolling } from "../../../hooks/usePolling.js";
import { getMetricsScrape, getSystemHealth } from "../../../services/api.js";

const parseMetric = (text, metricName) => {
  if (!text) return null;
  const match = text.match(new RegExp(`^${metricName}\\s+([0-9.]+)$`, "m"));
  return match ? Number(match[1]) : null;
};

export default function InfraDashboard() {
  const [metrics, setMetrics] = useState({ cpu: 0, memory: 0 });
  const [disk, setDisk] = useState(null);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);

  const fetchMetrics = useCallback(async () => {
    try {
      const [text, health] = await Promise.all([getMetricsScrape(), getSystemHealth()]);
      const cpu = parseMetric(text, "system_cpu_percent") || 0;
      const memory = parseMetric(text, "system_memory_percent") || 0;
      setDisk(health?.disk ?? null);
      setMetrics({ cpu, memory });
      setHistory((prev) => [...prev.slice(-9), { time: new Date().toLocaleTimeString(), cpu, memory }]);
      setError("");
    } catch (err) {
      setError(err?.message || "Unable to load infrastructure metrics");
    }
  }, []);

  usePolling(fetchMetrics, 30000);

  return (
    <>
      <div className="space-y-10">
        <SectionHeader
          eyebrow="Infrastructure"
          title="Live Systems Telemetry"
          description="CPU, memory, and service dependencies with cloud provider visibility."
        />
        <div className="grid gap-6 lg:grid-cols-4">
          <MetricCard label="CPU" value={metrics.cpu} unit="%" accent="amber" isLoading={!history.length && !error} error={error} />
          <MetricCard label="Memory" value={metrics.memory} unit="%" accent="blue" isLoading={!history.length && !error} error={error} />
          <MetricCard label="Disk" value={disk} unit="%" accent="emerald" isLoading={!history.length && !error} error={disk === null ? "Disk metrics unavailable" : ""} />
          <MetricCard label="Service Status" value={100 - metrics.cpu} unit="%" accent="emerald" isLoading={!history.length && !error} error={error} />
        </div>
        <div className="grid gap-6 lg:grid-cols-2">
          <GlassCard>
            <p className="text-sm font-semibold">CPU Trend</p>
            <LineChart data={history} xKey="time" yKey="cpu" />
          </GlassCard>
          <GlassCard>
            <p className="text-sm font-semibold">Memory Trend</p>
            <LineChart data={history} xKey="time" yKey="memory" stroke="#10b981" />
          </GlassCard>
        </div>
        <div className="grid gap-6 lg:grid-cols-1">
          <GlassCard>
            <p className="text-sm font-semibold">Service Dependency Map</p>
            <div className="mt-4 h-40 rounded-2xl border border-white/10 bg-white/5 flex items-center justify-center text-sm text-[var(--color-text-muted)]">
              Dependency data unavailable.
            </div>
          </GlassCard>
        </div>
        <CloudStatusPanel />
      </div>
      <GlassCard>
        <DocumentationPanel />
      </GlassCard>
    </>
  );
}
