import { useCallback, useState } from "react";
import SectionHeader from "../../../components/ui/SectionHeader.jsx";
import MetricCard from "../../../components/ui/MetricCard.jsx";
import GlassCard from "../../../components/ui/GlassCard.jsx";
import DocumentationPanel from "../DocumentationPanel.jsx";
import DataTable from "../../../components/ui/DataTable.jsx";
import LineChart from "../../../components/charts/LineChart.jsx";
import AreaChart from "../../../components/charts/AreaChart.jsx";
import { usePolling } from "../../../hooks/usePolling.js";
import { getDashboardConfig, getMetricsScrape, getPublicStatus, getRiskScore } from "../../../services/api.js";

const parseMetric = (text, metricName) => {
  if (!text) return null;
  const match = text.match(new RegExp(`^${metricName}\\s+([0-9.]+)$`, "m"));
  return match ? Number(match[1]) : null;
};

export default function SuperAdminDashboard() {
  const [risk, setRisk] = useState(null);
  const [metrics, setMetrics] = useState({ alerts: 0, cpu: 0, memory: 0 });
  const [config, setConfig] = useState(null);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState("");
  const [lastUpdated, setLastUpdated] = useState("");

  const fetchData = useCallback(async () => {
    try {
      const [riskData, metricsText, configData, publicStatus] = await Promise.all([
        getRiskScore(),
        getMetricsScrape(),
        getDashboardConfig(),
        getPublicStatus()
      ]);
      setRisk(riskData);
      setMetrics({
        alerts: parseMetric(metricsText, "active_alerts") || 0,
        cpu: parseMetric(metricsText, "system_cpu_percent") || 0,
        memory: parseMetric(metricsText, "system_memory_percent") || 0
      });
      setConfig(configData);
      setStatus(publicStatus);
      setError("");
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (err) {
      setError(err?.message || "Unable to load admin telemetry");
    }
  }, []);

  usePolling(fetchData, 30000);

  const infraTrend = status?.uptimeHistory || [];
  const vulnTrend = (status?.latestCriticalCves || []).map((cve) => ({
    name: cve.cve_id,
    value: Number(cve.cvss_score || 0)
  }));

    return (
      <>
        <div className="space-y-[var(--spacing-xxl)]">
          <SectionHeader
            eyebrow="Super Admin"
            title="Global Command Overview"
            description="System configuration, integration health, and enterprise risk alignment."
          />
          <div className="grid gap-[var(--spacing-lg)] lg:grid-cols-4">
            <MetricCard label="Global Risk" value={risk?.riskScore} unit="/100" accent="red" isLoading={!risk && !error} error={error} />
            <MetricCard label="Threat Index" value={risk?.factors?.criticalCveCount} unit="" accent="amber" isLoading={!risk && !error} error={error} />
            <MetricCard label="Active Alerts" value={metrics.alerts} unit="" accent="blue" isLoading={!lastUpdated && !error} error={error} />
            <MetricCard label="System Health" value={100 - metrics.cpu} unit="%" accent="emerald" isLoading={!lastUpdated && !error} error={error} />
          </div>
          <div className="grid gap-[var(--spacing-lg)] lg:grid-cols-2">
            <GlassCard>
              <p className="text-sm font-semibold">Infrastructure Trend</p>
              <LineChart data={infraTrend} xKey="month" yKey="uptime" />
            </GlassCard>
            <GlassCard>
              <p className="text-sm font-semibold">Vulnerability Trend</p>
              <AreaChart data={vulnTrend} xKey="name" yKey="value" />
            </GlassCard>
          </div>
          <div className="grid gap-[var(--spacing-lg)] lg:grid-cols-3">
            <GlassCard className="lg:col-span-2">
              <SectionHeader title="User Management" description="Manage enterprise users, roles, and access boundaries." />
              {config?.menu_items ? (
                <DataTable
                  columns={[
                    { key: "label", label: "Menu Item" },
                    { key: "path", label: "Path" }
                  ]}
                  rows={config.menu_items}
                  emptyMessage="No user management data available."
                />
              ) : (
                <p className="text-sm text-[var(--color-text-muted)]">{error || "User management endpoint unavailable."}</p>
              )}
            </GlassCard>
            <GlassCard>
              <p className="text-sm font-semibold">Integration Status</p>
              <p className="text-xs text-[var(--color-text-muted)]">Last updated {lastUpdated || "-"}</p>
              <div className="mt-4 space-y-2">
                {(config?.quick_actions || []).map((action) => (
                  <div key={action.id} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm">
                    {action.label}
                  </div>
                ))}
                {config?.quick_actions?.length ? null : (
                  <p className="text-sm text-[var(--color-text-muted)]">No integrations configured.</p>
                )}
              </div>
            </GlassCard>
          </div>
          <GlassCard>
            <p className="text-sm font-semibold">Audit Timeline</p>
            <p className="text-xs text-[var(--color-text-muted)]">Latest configuration changes across the enterprise.</p>
            <div className="mt-4 text-sm text-[var(--color-text-muted)]">Audit logs are available via backend audit services.</div>
          </GlassCard>
        </div>
        <GlassCard>
          <DocumentationPanel />
        </GlassCard>
      </>
  );
}
