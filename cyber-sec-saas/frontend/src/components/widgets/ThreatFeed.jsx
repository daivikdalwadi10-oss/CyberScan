import { useEffect, useState } from "react";
import GlassCard from "../ui/GlassCard.jsx";
import StatusBadge from "../ui/StatusBadge.jsx";
import { getLatestCves } from "../../services/api.js";

export default function ThreatFeed() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    getLatestCves()
      .then((data) => {
        if (isMounted) setItems(data || []);
      })
      .catch((err) => {
        if (isMounted) setError(err?.message || "Unable to load CVE feed");
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <GlassCard className="flex flex-col gap-4">
      <div>
        <p className="text-sm font-semibold">Critical CVE Feed</p>
        <p className="text-xs text-[var(--color-text-muted)]">Sourced from NVD enrichment</p>
      </div>
      {loading ? <div className="h-20 w-full rounded-2xl skeleton" /> : null}
      {error ? <p className="text-sm text-red-200">{error}</p> : null}
      <div className="space-y-3">
        {items.length === 0 && !loading ? (
          <p className="text-sm text-[var(--color-text-muted)]">No critical CVEs found.</p>
        ) : (
          items.map((cve) => (
            <div key={cve.cve_id} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium">{cve.cve_id}</p>
                <StatusBadge status="critical" label={cve.severity || "CRITICAL"} />
              </div>
              <p className="mt-1 text-xs text-[var(--color-text-muted)]">{cve.title}</p>
            </div>
          ))
        )}
      </div>
    </GlassCard>
  );
}
