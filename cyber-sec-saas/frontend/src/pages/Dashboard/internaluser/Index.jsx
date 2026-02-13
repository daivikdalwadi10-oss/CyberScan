import { useEffect, useState } from "react";
import SectionHeader from "../../../components/ui/SectionHeader.jsx";
import MetricCard from "../../../components/ui/MetricCard.jsx";
import GlassCard from "../../../components/ui/GlassCard.jsx";
import DataTable from "../../../components/ui/DataTable.jsx";
import DocumentationPanel from "../DocumentationPanel.jsx";
import { getPublicStatus } from "../../../services/api.js";

export default function InternalUserDashboard() {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;
    getPublicStatus()
      .then((data) => {
        if (isMounted) setStatus(data);
      })
      .catch((err) => {
        if (isMounted) setError(err?.message || "Unable to load availability data");
      });
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <>
      <div className="space-y-10">
        <SectionHeader
          eyebrow="Internal User"
          title="Service Availability"
          description="Availability overview and personal activity logs."
        />
        <div className="grid gap-6 lg:grid-cols-3">
          <MetricCard label="Uptime" value={status?.uptime} unit="%" accent="emerald" isLoading={!status && !error} error={error} />
          <MetricCard label="Risk Score" value={status?.riskScore} unit="/100" accent="red" isLoading={!status && !error} error={error} />
          <MetricCard label="Incidents Resolved" value={status?.incidentsResolved} unit="" accent="blue" isLoading={!status && !error} error={error} />
        </div>
        <GlassCard>
          <p className="text-sm font-semibold">Personal Activity Log</p>
          <DataTable
            columns={[
              { key: "date", label: "Date" },
              { key: "title", label: "Activity" },
              { key: "type", label: "Type" }
            ]}
            rows={status?.recentUpdates || []}
            emptyMessage="No activity logged."
          />
        </GlassCard>
      </div>
      <GlassCard>
        <DocumentationPanel />
      </GlassCard>
    </>
  );
}
