import { useEffect, useState } from "react";
import SectionHeader from "../../../components/ui/SectionHeader.jsx";
import GlassCard from "../../../components/ui/GlassCard.jsx";
import DataTable from "../../../components/ui/DataTable.jsx";
import DocumentationPanel from "../DocumentationPanel.jsx";
import RiskGauge from "../../../components/charts/RiskGauge.jsx";
import { getAuditLogs, getPublicStatus, getRiskScore } from "../../../services/api.js";

export default function AuditorDashboard() {
  const [status, setStatus] = useState(null);
  const [risk, setRisk] = useState(null);
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;
    Promise.all([getPublicStatus(), getRiskScore(), getAuditLogs({ limit: 10 })])
      .then(([publicStatus, riskData, auditLogs]) => {
        if (isMounted) {
          setStatus(publicStatus);
          setRisk(riskData);
          setLogs(auditLogs || []);
        }
      })
      .catch((err) => {
        if (isMounted) setError(err?.message || "Unable to load audit data");
      });
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <>
      <div className="space-y-10">
        <SectionHeader
          eyebrow="Auditor"
          title="Read-only Audit Explorer"
          description="Historical risk comparison and incident replay for compliance review."
        />
        {error ? <p className="text-sm text-red-200">{error}</p> : null}
        <div className="grid gap-6 lg:grid-cols-2">
          <GlassCard>
            <p className="text-sm font-semibold">Audit Explorer</p>
            <DataTable
              columns={[
                { key: "action", label: "Action" },
                { key: "resource_type", label: "Resource" },
                { key: "timestamp", label: "Timestamp" }
              ]}
              rows={logs}
              emptyMessage="No audit records available."
            />
          </GlassCard>
          <GlassCard>
            <p className="text-sm font-semibold">Risk Comparison</p>
            <RiskGauge value={risk?.riskScore || 0} />
          </GlassCard>
        </div>
        <GlassCard>
          <p className="text-sm font-semibold">Incident Replay</p>
          <p className="text-sm text-[var(--color-text-muted)]">Incident replay data is available via audit export.</p>
        </GlassCard>
      </div>
      <GlassCard>
        <DocumentationPanel />
      </GlassCard>
    </>
  );
}
