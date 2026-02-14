import { useEffect, useState } from "react";
import SectionHeader from "../../../components/ui/SectionHeader.jsx";
import MetricCard from "../../../components/ui/MetricCard.jsx";
import GlassCard from "../../../components/ui/GlassCard.jsx";
import RiskGauge from "../../../components/charts/RiskGauge.jsx";
import DataTable from "../../../components/ui/DataTable.jsx";
import DocumentationPanel from "../DocumentationPanel.jsx";
import { getAuditLogs, getPublicStatus, getRiskScore, getSystemHealth } from "../../../services/api.js";

export default function ComplianceDashboard() {
  const [risk, setRisk] = useState(null);
  const [status, setStatus] = useState(null);
  const [logs, setLogs] = useState([]);
  const [health, setHealth] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;
    Promise.all([getRiskScore(), getPublicStatus(), getAuditLogs({ limit: 10 }), getSystemHealth()])
      .then(([riskData, publicStatus, auditLogs, systemHealth]) => {
        if (isMounted) {
          setRisk(riskData);
          setStatus(publicStatus);
          setLogs(auditLogs || []);
          setHealth(systemHealth);
        }
      })
      .catch((err) => {
        if (isMounted) setError(err?.message || "Unable to load compliance data");
      });
    return () => {
      isMounted = false;
    };
  }, []);

  const compliantCount = status?.compliance?.filter((item) =>
    ["compliant", "certified"].includes(String(item.status || "").toLowerCase())
  ).length || 0;
  const compliancePercent = status?.compliance?.length
    ? Math.round((compliantCount / status.compliance.length) * 100)
    : 0;

  return (
    <>
      <div className="space-y-[var(--spacing-xxl)]">
        <SectionHeader
          eyebrow="Compliance"
          title="Risk & Audit Oversight"
          description="Audit logs, compliance mapping, and report generation coverage."
        />
        <div className="grid gap-[var(--spacing-lg)] lg:grid-cols-3">
          <MetricCard label="Risk Score" value={risk?.riskScore} unit="/100" accent="red" isLoading={!risk && !error} error={error} />
          <MetricCard label="Compliance %" value={compliancePercent} unit="%" accent="emerald" isLoading={!status && !error} error={error} />
          <MetricCard label="Open Findings" value={risk?.factors?.criticalCveCount} unit="" accent="amber" isLoading={!risk && !error} error={error} />
        </div>
        <div className="grid gap-[var(--spacing-lg)] lg:grid-cols-2">
          <GlassCard>
            <p className="text-sm font-semibold">Audit Log Viewer</p>
            <DataTable
              columns={[
                { key: "action", label: "Action" },
                { key: "resource_type", label: "Resource" },
                { key: "timestamp", label: "Timestamp" }
              ]}
              rows={logs}
              emptyMessage="Audit logs unavailable."
            />
          </GlassCard>
          <GlassCard>
            <p className="text-sm font-semibold">Risk Score Gauge</p>
            <RiskGauge value={risk?.riskScore || 0} />
          </GlassCard>
        </div>
        <div className="grid gap-[var(--spacing-lg)] lg:grid-cols-2">
          <GlassCard>
            <p className="text-sm font-semibold">Incident Reports</p>
            <DataTable
              columns={[
                { key: "title", label: "Report" },
                { key: "date", label: "Date" },
                { key: "type", label: "Type" }
              ]}
              rows={status?.recentUpdates || []}
              emptyMessage="No incident reports available."
            />
          </GlassCard>
          <GlassCard>
            <p className="text-sm font-semibold">Risk Trend</p>
            <p className="text-sm text-[var(--color-text-muted)]">System uptime: {health?.uptimePercent ?? "-"}%</p>
          </GlassCard>
        </div>
      </div>
      <GlassCard>
        <DocumentationPanel />
      </GlassCard>
    </>
  );
}
