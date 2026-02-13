import { useEffect, useState } from "react";
import SectionHeader from "../../components/ui/SectionHeader.jsx";
import DataTable from "../../components/ui/DataTable.jsx";
import StatusBadge from "../../components/ui/StatusBadge.jsx";
import { getPublicStatus } from "../../services/api.js";

export default function PublicStatus() {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;
    getPublicStatus()
      .then((data) => {
        if (isMounted) setStatus(data);
      })
      .catch((err) => {
        if (isMounted) setError(err?.message || "Unable to load service status");
      });
    return () => {
      isMounted = false;
    };
  }, []);

  const columns = [
    { key: "name", label: "Service" },
    {
      key: "status",
      label: "Status",
      render: (row) => <StatusBadge status={row.status} label={row.status} />
    }
  ];

  return (
    <div className="space-y-8">
      <SectionHeader
        eyebrow="Availability"
        title="Service Status"
        description="Operational state for key platform services and compliance posture."
      />
      {error ? <p className="text-sm text-red-200">{error}</p> : null}
      <DataTable columns={columns} rows={status?.services || []} emptyMessage="No service status available." />
      <SectionHeader eyebrow="Compliance" title="Compliance Posture" />
      <DataTable
        columns={[
          { key: "framework", label: "Framework" },
          { key: "status", label: "Status" },
          { key: "lastAudit", label: "Last Audit" }
        ]}
        rows={status?.compliance || []}
        emptyMessage="No compliance records available."
      />
    </div>
  );
}
