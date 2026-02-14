import { useEffect, useState } from "react";
import SectionHeader from "../../../components/ui/SectionHeader.jsx";
import MetricCard from "../../../components/ui/MetricCard.jsx";
import ThreatFeed from "../../../components/widgets/ThreatFeed.jsx";
import GlassCard from "../../../components/ui/GlassCard.jsx";
import DataTable from "../../../components/ui/DataTable.jsx";
import DocumentationPanel from "../DocumentationPanel.jsx";
import { getIocs, getPublicStatus, getRiskScore, getThreatIntel } from "../../../services/api.js";

export default function SecurityAdminDashboard() {
  const [status, setStatus] = useState(null);
  const [risk, setRisk] = useState(null);
  const [intel, setIntel] = useState([]);
  const [iocs, setIocs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;
    Promise.all([getPublicStatus(), getRiskScore(), getThreatIntel({ limit: 6 }), getIocs({ limit: 6 })])
      .then(([publicStatus, riskData, intelData, iocData]) => {
        if (isMounted) {
          setStatus(publicStatus);
          setRisk(riskData);
          setIntel(intelData || []);
          setIocs(iocData || []);
        }
      })
      .catch((err) => {
        if (isMounted) setError(err?.message || "Unable to load threat intelligence");
      });
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <>
      <div className="space-y-[var(--spacing-xxl)]">
        <SectionHeader
          eyebrow="Security Admin"
          title="Threat Intelligence Command"
          description="CVE enrichment, IOC management, and escalation rule tuning."
        />
        <div className="grid gap-[var(--spacing-lg)] lg:grid-cols-4">
          <MetricCard label="Risk Score" value={risk?.riskScore} unit="/100" accent="red" isLoading={!risk && !error} error={error} />
          <GlassCard className="flex flex-col justify-between">
            <p className="text-xs uppercase tracking-[0.3em] text-[var(--color-text-muted)]">Threat Level</p>
            <p className="text-2xl font-display capitalize">{risk?.threatLevel || "unknown"}</p>
            <p className="text-xs text-[var(--color-text-muted)]">Calculated {risk?.calculatedAt || "-"}</p>
          </GlassCard>
          <MetricCard label="Critical CVEs" value={status?.latestCriticalCves?.length} unit="" accent="blue" isLoading={!status && !error} error={error} />
          <MetricCard label="Incident Timeline" value={status?.incidentTimeline?.length} unit="" accent="emerald" isLoading={!status && !error} error={error} />
        </div>
        <div className="grid gap-[var(--spacing-lg)] lg:grid-cols-2">
          <ThreatFeed />
          <GlassCard>
            <p className="text-sm font-semibold">Alert Escalation Rules</p>
            <DataTable
              columns={[
                { key: "framework", label: "Rule" },
                { key: "status", label: "Status" },
                { key: "lastAudit", label: "Last Review" }
              ]}
              rows={status?.compliance || []}
              emptyMessage="No escalation rules configured."
            />
          </GlassCard>
        </div>
        <div className="grid gap-[var(--spacing-lg)] lg:grid-cols-2">
          <GlassCard>
            <p className="text-sm font-semibold">Threat Intelligence Feed</p>
            <DataTable
              columns={[
                { key: "cve_id", label: "CVE" },
                { key: "severity", label: "Severity" },
                { key: "cvss_score", label: "CVSS" }
              ]}
              rows={intel}
              emptyMessage="No threat intel records available."
            />
          </GlassCard>
          <GlassCard>
            <p className="text-sm font-semibold">IOC Management</p>
            <DataTable
              columns={[
                { key: "title", label: "Indicator" },
                { key: "severity", label: "Severity" },
                { key: "status", label: "Status" }
              ]}
              rows={iocs}
              emptyMessage="No IOCs detected."
            />
          </GlassCard>
        </div>
        <GlassCard>
          <SectionHeader title="IOC Management" description="Indicators of compromise managed by Security Admin." />
          <p className="text-sm text-[var(--color-text-muted)]">IOC list is refreshed from alert stream data.</p>
        </GlassCard>
      </div>
      <GlassCard>
        <DocumentationPanel />
      </GlassCard>
    </>
  );
}
