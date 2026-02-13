import { useEffect, useState } from "react";
import GlassCard from "../ui/GlassCard.jsx";
import StatusBadge from "../ui/StatusBadge.jsx";
import { getIncidents } from "../../services/api.js";

export default function IncidentBoard({ title = "Incident Board", params, onUpdateStatus }) {
  const [incidents, setIncidents] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const paramsKey = JSON.stringify(params || {});

  useEffect(() => {
    let isMounted = true;
    getIncidents(params)
      .then((data) => {
        if (isMounted) setIncidents(data || []);
      })
      .catch((err) => {
        if (isMounted) setError(err?.message || "Unable to load incidents");
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [paramsKey]);

  return (
    <GlassCard className="flex flex-col gap-4">
      <div>
        <p className="text-sm font-semibold">{title}</p>
        <p className="text-xs text-[var(--color-text-muted)]">Live incident tracking</p>
      </div>
      {error ? <p className="text-sm text-red-200">{error}</p> : null}
      <div className="space-y-3">
        {loading ? (
          <div className="h-16 w-full rounded-2xl skeleton" />
        ) : incidents.length === 0 ? (
          <p className="text-sm text-[var(--color-text-muted)]">No incidents available.</p>
        ) : (
          incidents.map((incident) => (
            <div key={incident.id} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
              <div className="flex items-center justify-between">
                <p className="text-sm">{incident.title || "Incident"}</p>
                <StatusBadge status={incident.status === "resolved" ? "operational" : "warning"} label={incident.status} />
              </div>
              <p className="text-xs text-[var(--color-text-muted)]">{incident.created_at || incident.createdAt}</p>
              {onUpdateStatus ? (
                <div className="mt-3 flex flex-wrap gap-2">
                  <button
                    className="rounded-full border border-white/10 px-3 py-1 text-xs"
                    type="button"
                    onClick={() => onUpdateStatus(incident.id, "investigating")}
                  >
                    Investigate
                  </button>
                  <button
                    className="rounded-full border border-white/10 px-3 py-1 text-xs"
                    type="button"
                    onClick={() => onUpdateStatus(incident.id, "contained")}
                  >
                    Contain
                  </button>
                  <button
                    className="rounded-full border border-white/10 px-3 py-1 text-xs"
                    type="button"
                    onClick={() => onUpdateStatus(incident.id, "resolved")}
                  >
                    Resolve
                  </button>
                </div>
              ) : null}
            </div>
          ))
        )}
      </div>
    </GlassCard>
  );
}
