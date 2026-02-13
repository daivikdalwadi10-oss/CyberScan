import { useEffect, useState } from "react";
import SectionHeader from "../../components/ui/SectionHeader.jsx";
import DataTable from "../../components/ui/DataTable.jsx";
import StatusBadge from "../../components/ui/StatusBadge.jsx";
import { getPublicStatus } from "../../services/api.js";

export default function PublicIncidents() {
  const [timeline, setTimeline] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;
    getPublicStatus()
      .then((data) => {
        if (isMounted) setTimeline(data?.incidentTimeline || []);
      })
      .catch((err) => {
        if (isMounted) setError(err?.message || "Unable to load incident timeline");
      });
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="space-y-8">
      <SectionHeader
        eyebrow="Transparency"
        title="Public Incident Timeline"
        description="Read-only view of historical incidents and resolution status."
      />
      {error ? <p className="text-sm text-red-200">{error}</p> : null}
      <DataTable
        columns={[
          { key: "title", label: "Incident" },
          { key: "severity", label: "Severity" },
          {
            key: "status",
            label: "Status",
            render: (row) => <StatusBadge status={row.status === "RESOLVED" ? "operational" : "warning"} label={row.status} />
          },
          { key: "created_at", label: "Created" }
        ]}
        rows={timeline}
        emptyMessage="No incidents published."
      />
    </div>
  );
}
