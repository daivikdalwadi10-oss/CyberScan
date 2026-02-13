import { useEffect, useState } from "react";
import SectionHeader from "../../../components/ui/SectionHeader.jsx";
import MetricCard from "../../../components/ui/MetricCard.jsx";
import AlertsFeed from "../../../components/widgets/AlertsFeed.jsx";
import IncidentBoard from "../../../components/widgets/IncidentBoard.jsx";
import HeatMap from "../../../components/charts/HeatMap.jsx";
import GlassCard from "../../../components/ui/GlassCard.jsx";
import ThreatFeed from "../../../components/widgets/ThreatFeed.jsx";
import DocumentationPanel from "../DocumentationPanel.jsx";
import { getAlerts, getIncidents, getRiskScore, updateIncidentStatus } from "../../../services/api.js";

export default function SocDashboard() {
  const [alerts, setAlerts] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [risk, setRisk] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;
    Promise.all([getAlerts({ limit: 10 }), getIncidents({ limit: 10 }), getRiskScore()])
      .then(([alertsData, incidentsData, riskData]) => {
        if (isMounted) {
          setAlerts(alertsData || []);
          setIncidents(incidentsData || []);
          setRisk(riskData);
        }
      })
      .catch((err) => {
        if (isMounted) setError(err?.message || "Unable to load SOC telemetry");
      });
    return () => {
      isMounted = false;
    };
  }, []);

  const severityBuckets = ["CRITICAL", "HIGH", "MEDIUM", "LOW"];
  const heatmapData = severityBuckets.map((severity) => {
    const filtered = alerts.filter((alert) => alert.severity === severity).slice(0, 8);
    return Array.from({ length: 8 }).map((_, index) => (filtered[index] ? 6 : 0));
  });

  return (
    <>
      <div className="space-y-10">
        <SectionHeader
          eyebrow="SOC Analyst"
          title="Real-Time Alert Board"
          description="Live alerts, incident triage, and lifecycle control with WebSocket streaming."
        />
        <div className="grid gap-6 lg:grid-cols-4">
          <MetricCard label="Active Alerts" value={alerts.length} unit="" accent="red" isLoading={!alerts && !error} error={error} />
          <MetricCard label="Critical Alerts" value={alerts.filter((alert) => alert.severity === "CRITICAL").length} unit="" accent="amber" isLoading={!alerts && !error} error={error} />
          <MetricCard label="Open Incidents" value={incidents.length} unit="" accent="blue" isLoading={!incidents && !error} error={error} />
          <GlassCard className="flex flex-col justify-between">
            <p className="text-xs uppercase tracking-[0.3em] text-[var(--color-text-muted)]">Threat Level</p>
            <p className="text-2xl font-display capitalize">{risk?.threatLevel || "unknown"}</p>
            <p className="text-xs text-[var(--color-text-muted)]">Risk score {risk?.riskScore || 0}/100</p>
          </GlassCard>
        </div>
        <div className="grid gap-6 lg:grid-cols-[2fr,1fr]">
          <AlertsFeed />
          <IncidentBoard
            title="Incident Summary"
            params={{ limit: 5 }}
            onUpdateStatus={(id, status) =>
              updateIncidentStatus(id, { status }).catch(() => {})
            }
          />
        </div>
        <div className="grid gap-6 lg:grid-cols-2">
          <GlassCard>
            <p className="text-sm font-semibold">Threat Heatmap</p>
            <HeatMap data={heatmapData} />
          </GlassCard>
          <ThreatFeed />
        </div>
      </div>
      <GlassCard>
        <DocumentationPanel />
      </GlassCard>
    </>
  );
}
